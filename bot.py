import os
from telegram import Update, InputMediaVideo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8106772232:AAFVElBWl5YZ7MPyszr3N0BGo9a3IH8uNCo"  # Replace with your token

# Simulated AI generation function
def generate_ai_video(prompt, image_path):
    print(f"Generating video for prompt: {prompt} and image: {image_path}")
    # Simulate video generation delay
    import time
    time.sleep(5)
    # Return sample video path
    return "sample_output.mp4"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a prompt and an image to generate a 4K AI video!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {"prompt": update.message.text}
    await update.message.reply_text("✅ Prompt received! Now please send me an image.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or "prompt" not in user_data[user_id]:
        await update.message.reply_text("❗Please send the prompt first.")
        return

    photo_file = await update.message.photo[-1].get_file()
    image_path = f"{user_id}_image.jpg"
    await photo_file.download_to_drive(image_path)

    prompt = user_data[user_id]["prompt"]
    await update.message.reply_text("🧠 Generating video... please wait 10-15 seconds.")

    video_path = generate_ai_video(prompt, image_path)

    with open(video_path, "rb") as video:
        await update.message.reply_video(video, caption="🎉 Here is your AI-generated 4K video!")

    os.remove(image_path)
    user_data.pop(user_id, None)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Bot is running...")
    app.run_polling()
