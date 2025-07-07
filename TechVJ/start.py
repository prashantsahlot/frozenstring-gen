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
                await msg.reply("**Make Sure I Am Admin In Your Channel**")
                return 
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🌹 Join Channel 🌹", url=invite_link.invite_link),
                    InlineKeyboardButton("✨ Check Again ✨", callback_data="chk")
                ]]
            ) 
        await msg.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me.If You Joined The Channel Then Click On Check Again Button To Confirm.**", reply_markup=key)
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""<b>𝐇𝐞𝐲 {msg.from_user.mention}🍷,\n\nɪ ᴀᴍ {me},\nᴛʀᴜsᴛᴇᴅ 𝗦𝗧𝗥𝗜𝗡𝗚 𝗚𝗥𝗡𝗘𝗥𝗔𝗧𝗢𝗥 ʙᴏᴛ.ғᴜʟʟʏ sᴀғᴇ & sᴇᴄᴜʀᴇ.\nɴᴏ ᴀɴʏ ᴇʀʀᴏʀ\n\nMade With By : [Zoro Bot](https://t.me/PAID_PROMOTION_PROOFS) !</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="⚡ Generate String Session ⚡", callback_data="generate")
            ],[
                InlineKeyboardButton("⚡ Support Group ✨", url="https://t.me/Frozensupport1"),
                InlineKeyboardButton("🌹 Join Channel 🌹", url="https://t.me/vibeshiftbots")
            ]]
        )
    )

@Client.on_callback_query(filters.regex("chk"))
async def chk(bot : Client, cb : CallbackQuery):
    try:
        await bot.get_chat_member(int(F_SUB), cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️", show_alert=True)
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=cb.from_user.id,
        text=f"""<b>𝐇𝐞𝐲 {cb.from_user.mention}🍷,\n\nɪ ᴀᴍ {me},\nᴛʀᴜsᴛᴇᴅ 𝗦𝗧𝗥𝗜𝗡𝗚 𝗚𝗥𝗡𝗘𝗥𝗔𝗧𝗢𝗥 ʙᴏᴛ.ғᴜʟʟʏ sᴀғᴇ & sᴇᴄᴜʀᴇ.\nɴᴏ ᴀɴʏ ᴇʀʀᴏʀ\n\nMade With By : [Zozo Bots](https://t.me/PAID_PROMOTION_PROOFS) !</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="⚡ Generate String Session ⚡", callback_data="generate")
            ],[
                InlineKeyboardButton("💕 Support Group 💕", url="https://t.me/Frozensupport1"),
                InlineKeyboardButton("⚡ Update Channel ✨", url="https://t.me/vibeshiftbots")
            ]]
        )
    )
