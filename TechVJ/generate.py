import config
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from TechVJ.db import db
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid,
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError, PhoneNumberInvalidError, PhoneCodeInvalidError,
    PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError
)

# ——— Questions & Buttons ———————————————————
ask_ques = "**▶️ Pick the session type you’d like to generate:**"
buttons_ques = [
    [
        InlineKeyboardButton("📲 Telethon", callback_data="telethon"),
        InlineKeyboardButton("🤖 Pyrogram", callback_data="pyrogram")
    ],
    [
        InlineKeyboardButton("📲 Telethon Bot", callback_data="telethon_bot"),
        InlineKeyboardButton("🤖 Pyrogram Bot", callback_data="pyrogram_bot")
    ]
]
gen_button = [[InlineKeyboardButton("⚡ START AGAIN", callback_data="generate")]]

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate","gen","string","str"]))
async def main(_, msg: Message):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    # — track user
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)

    # — enforce update-channel subscription
    if config.F_SUB:
        try:
            await bot.get_chat_member(int(config.F_SUB), msg.from_user.id)
        except:
            try:
                link = await bot.create_chat_invite_link(int(config.F_SUB))
            except:
                await msg.reply("⚠️ Make sure I have admin rights in your channel!")
                return
            kb = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔔 Join Updates", url=link.invite_link),
                InlineKeyboardButton("✅ Verify", callback_data="chk")
            ]])
            await msg.reply("**🚫 Access restricted!**\nJoin the updates channel, then tap Verify.", reply_markup=kb)
            return

    # — decide label
    label = "TELETHON" if telethon else "PYROGRAM"
    if is_bot:
        label += " BOT"

    await msg.reply(f"⌛ Initializing **{label}** session…")

    user_id = msg.chat.id
    # — ask for API_ID
    api_id_msg = await bot.ask(
        user_id,
        "🆔 Send your **API_ID**, or /skip to use the bot’s default:",
        filters=filters.text
    )
    if await cancelled(api_id_msg): return

    if api_id_msg.text == "/skip":
        api_id, api_hash = config.API_ID, config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("API_ID must be a number.", reply_markup=InlineKeyboardMarkup(gen_button), quote=True)
            return
        hash_msg = await bot.ask(user_id, "🔑 Now send your **API_HASH**:", filters=filters.text)
        if await cancelled(hash_msg): return
        api_hash = hash_msg.text

    # — ask for phone or bot-token
    if not is_bot:
        prompt = "📱 Send the phone number (+country code) to generate the session:"
    else:
        prompt = "🤖 Send your **bot token** to proceed:"

    pn_msg = await bot.ask(user_id, prompt, filters=filters.text)
    if await cancelled(pn_msg): return
    phone = pn_msg.text

    await msg.reply("📨 Sending code…") if not is_bot else await msg.reply("🔑 Logging in with bot token…")

    # — init client
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)

    await client.connect()

    # — handle 2FA for user accounts
    try:
        if not is_bot:
            code_req = await (client.send_code_request(phone) if telethon else client.send_code(phone))
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("❌ Incorrect API_ID/API_HASH pair.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except PhoneNumberInvalidError:
        await msg.reply("❌ That phone number isn’t linked to Telegram.", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    # — get OTP
    if not is_bot:
        try:
            otp_msg = await bot.ask(
                user_id,
                "📩 Enter the **code** you just received:",
                filters=filters.text,
                timeout=600
            )
            if await cancelled(otp_msg): return
            otp = otp_msg.text.replace(" ", "")
            if telethon:
                await client.sign_in(phone, otp)
            else:
                await client.sign_in(phone, code_req.phone_code_hash, otp)
        except TimeoutError:
            await msg.reply("⏰ Time’s up! Please restart.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("❌ Invalid code. Try again.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("❌ Code expired. Try again.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except SessionPasswordNeededError:
            pswd_msg = await bot.ask(user_id, "🔒 Enter your 2FA password:", filters=filters.text, timeout=300)
            if await cancelled(pswd_msg): return
            try:
                if telethon:
                    await client.sign_in(password=pswd_msg.text)
                else:
                    await client.check_password(password=pswd_msg.text)
            except PasswordHashInvalidError:
                await pswd_msg.reply("❌ Wrong 2FA password.", reply_markup=InlineKeyboardMarkup(gen_button), quote=True)
                return
    else:
        if telethon:
            await client.start(bot_token=phone)
        else:
            await client.sign_in_bot(phone)

    # — export session
    session_str = client.session.save() if telethon else await client.export_session_string()
    save_text = (
        f"**📝 Your {label} session string:**\n\n`{session_str}`\n\n"
        "🔐 Keep this safe! Others can hijack your account with it.\n\n"
        "💡 Join our Support → @Frozensupport1\n"
        "📢 Updates → @vibeshiftbots"
    )

    # — deliver and clean up
    try:
        dest = "me" if not is_bot else msg.chat.id
        await client.send_message(dest, save_text)
    except KeyError:
        pass

    await client.disconnect()
    await bot.send_message(
        msg.chat.id,
        f"✅ Done! Check your saved messages for the string session."
    )


async def cancelled(msg: Message) -> bool:
    text = msg.text.lower()
    if "/cancel" in text:
        await msg.reply("❎ Generation cancelled.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    if "/restart" in text:
        await msg.reply("🔄 Restarting…", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    return False

