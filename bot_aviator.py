import random
import logging
import asyncio
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# 🔑 Token y ruta de la imagen
TOKEN = "7279257503:AAFBuifN_OzBDoJUtqKbXnheK-1RiqJPT0c"
AVIATOR_IMAGE = "AviatorFoto.webp"  # Imagen en la misma carpeta

# 📌 Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("✅ Bot inicializado correctamente.")

# Inicializar bot
bot = Bot(token=TOKEN)

# 📌 Función para generar una predicción
def generar_prediccion():
    probabilidad = random.random()

    if probabilidad < 0.90:  # 90% chance entre 1.10x y 3.00x
        numero = round(random.uniform(1.10, 3.00), 2)
    else:  # 10% chance de más de 5x
        numero = round(random.uniform(5.00, 10.00), 2)

    acertividad = random.randint(60, 95)  # Acertividad 60% - 95%

    return numero, acertividad

# 📌 Función para el mensaje de bienvenida con botón
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    mensaje = "🎮 *Bienvenido al Bot de Predicciones Aviator* 🚀\n\n_Toca el botón para recibir tu primera predicción._"

    keyboard = [[InlineKeyboardButton("🎰 Obtener predicción", callback_data="jugar")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(AVIATOR_IMAGE, "rb") as foto:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(foto), caption=mensaje, reply_markup=reply_markup, parse_mode="Markdown")

# 📌 Función para iniciar el juego con /prediccion
async def iniciar_juego(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    mensaje = "🎮 *Juego Aviator* 🚀\n\n_Toca el botón para recibir una predicción._"

    keyboard = [[InlineKeyboardButton("🎰 Jugar", callback_data="jugar")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(AVIATOR_IMAGE, "rb") as foto:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(foto), caption=mensaje, reply_markup=reply_markup, parse_mode="Markdown")

# 📌 Función para manejar los clics en los botones
async def manejar_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()

    if query.data == "jugar":
        # Animación de despegue
        await query.message.edit_caption(caption="🚀 *Avión despegando...*", parse_mode="Markdown")
        await asyncio.sleep(2)  # Simula el vuelo

        # Obtener predicción
        numero, acertividad = generar_prediccion()

        mensaje = (
            f"🎰 *Próxima predicción:* `{numero}x` 🚀\n"
            f"👌 *Acertividad:* `{acertividad}%`\n\n"
            f"🚀 *Link para jugar:* [🤑 Haz clic aquí](https://bit.ly/4ebYjdf)"
        )

        # Nuevo botón para volver a jugar
        keyboard = [[InlineKeyboardButton("🎰 Volver a jugar", callback_data="jugar")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_caption(caption=mensaje, reply_markup=reply_markup, parse_mode="Markdown")

# 📌 Configurar comandos y botones
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))  # Nuevo comando de bienvenida
    app.add_handler(CommandHandler("prediccion", iniciar_juego))
    app.add_handler(CallbackQueryHandler(manejar_callback))

    logging.info("🚀 Bot iniciado...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # Mantener el bot en ejecución

if __name__ == "__main__":
    asyncio.run(main())
