import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# VPN параметры
IP = "147.45.101.79"
PORT = 40124
PBK = "3vxmV7dj-sXDceO4thYat90u5D2qTBeJXw2boLx4awA"
SNI = "yahoo.com"
SID = "774f22f4e918b3"
SPX = "/"
FP = "chrome"

# Инициализация бота с указанием parse_mode
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 7 дней"), KeyboardButton(text="📅 30 дней")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Выбери тариф для подключения к VPN:", reply_markup=kb)

@dp.message(lambda msg: msg.text in ["🗓 7 дней", "📅 30 дней"])
async def handle_tariff(msg: types.Message):
    user_uuid = str(uuid.uuid4())
    link = (
        f"vless://{user_uuid}@{IP}:{PORT}"
        f"?type=tcp&security=reality&pbk={PBK}"
        f"&fp={FP}&sni={SNI}&sid={SID}&spx={SPX}#vpn_{msg.from_user.id}"
    )
    await msg.answer(f"✅ Готово!\n\nВот твоя ссылка:\n\n<code>{link}</code>")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
