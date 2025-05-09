
from aiohttp import web
from .route import routes
from asyncio import sleep 
from datetime import datetime
from database.users_chats_db import db
from info import LOG_CHANNEL

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def check_expired_premium(client):
    while 1:
        data = await db.get_expired(datetime.now())
        for user in data:
            user_id = user["id"]
            await db.remove_premium_access(user_id)
            try:
                user = await client.get_users(user_id)
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>Dᴇᴀʀ {user.mention},\n\n ☹️ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴘʟᴀɴ ʜᴀꜱ ᴇxᴘɪʀᴇᴅ, ᴛᴏ ᴇɴᴊᴏʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ꜱᴇʀᴠɪᴄᴇꜱ ᴀɢᴀɪɴ ᴘʟᴇᴀꜱᴇ ʙᴜʏ ᴄɪɴᴇᴡᴏᴏᴅ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴀɢᴀɪɴ ᴀꜱ ᴘᴇʀ ʏᴏᴜʀ ᴘʟᴀɴ ᴛᴏ ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀɴ ᴜꜱᴇ /myplan ᴛᴏ ᴄʜᴇᴄᴋ ᴘʟᴀɴꜱ ʟɪꜱᴛ ᴜꜱᴇ /Plans</b>"
                )
                await client.send_message(LOG_CHANNEL, text=f"<b>#Premium_Expire\n\nUser name: {user.mention}\nUser id: <code>{user_id}</code>")
            except Exception as e:
                print(e)
            await sleep(0.5)
        await sleep(1)

