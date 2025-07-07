from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID, F_SUB
from TechVJ.db import db

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)
    if F_SUB:
        try:
            await bot.get_chat_member(int(F_SUB), msg.from_user.id)
        except:
            try:
                invite_link = await bot.create_chat_invite_link(int(F_SUB))
            except:
                await msg.reply("⚠️ Please ensure I have admin rights in your channel!")
                return 
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🔔 Join Update Channel", url=invite_link.invite_link),
                    InlineKeyboardButton("✅ Check Again", callback_data="chk")
                ]]
            )
        await msg.reply_text(
            "**🚫 Access Denied! 🚫\n\nTo use this bot, please join the update channel. Once joined, tap 'Check Again' to continue.**", 
            reply_markup=key
        )
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""<b>👋 Hello {msg.from_user.mention}!\n\nI am {me},\nyour trusted <u>String Session Generator Bot</u> — secure, fast, and reliable.\n\n✨ Enjoy hassle-free session generation with complete safety.\n\nPowered by: [Frozen Bots](https://t.me/vibeshiftbots)</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="⚡ Create String Session ⚡", callback_data="generate")
            ],[
                InlineKeyboardButton("💬 Support Group", url="https://t.me/Frozensupport1"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/vibeshiftbots")
            ]]
        )
    )

@Client.on_callback_query(filters.regex("chk"))
async def chk(bot: Client, cb: CallbackQuery):
    try:
        await bot.get_chat_member(int(F_SUB), cb.from_user.id)
    except:
        await cb.answer("❗ You haven't joined the channel yet. Please join first and then check again.", show_alert=True)
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=cb.from_user.id,
        text=f"""<b>👋 Hello {cb.from_user.mention}!\n\nI am {me},\nyour trusted <u>String Session Generator Bot</u> — secure, fast, and reliable.\n\n✨ Enjoy hassle-free session generation with complete safety.\n\nPowered by: [Frozen Bots](https://t.me/vibeshiftbots)</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="⚡ Create String Session ⚡", callback_data="generate")
            ],[
                InlineKeyboardButton("💬 Support Group", url="https://t.me/Frozensupport1"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/vibeshiftbots")
            ]]
        )
    )
