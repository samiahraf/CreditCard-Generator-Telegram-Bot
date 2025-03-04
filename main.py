# Install python-telegram-bot Before running

import random
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = "Your bot token"

def generate_cc(bin_number):
    bin_number = bin_number.ljust(15, 'X')
    generated = [random.randint(0, 9) if ch == 'X' else int(ch) for ch in bin_number]

    checksum = 0
    for i, digit in enumerate(generated[::-1]):
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    last_digit = (10 - (checksum % 10)) % 10
    generated.append(last_digit)

    return "".join(map(str, generated))

def generate_expiry():
    current_year = datetime.now().year % 100
    exp_year = random.randint(current_year + 1, current_year + 5)
    exp_month = f"{random.randint(1, 12):02d}"
    return f"{exp_month}/{exp_year}"

def generate_cvv(card_number):
    return f"{random.randint(1000, 9999)}" if card_number.startswith("3") else f"{random.randint(100, 999)}"

async def generate_cards(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /gen <BIN>\nExample: /gen 41472XXXXX")
        return

    bin_input = context.args[0].upper()

    if not re.match(r'^[0-9X]+$', bin_input):
        await update.message.reply_text("Invalid BIN format! Use only numbers and 'X'.")
        return

    generated_cards = [f"{generate_cc(bin_input)} | {generate_expiry()} | {generate_cvv(generate_cc(bin_input))}" for _ in range(10)]
    response = "**Generated Cards:**\n" + "\n".join(generated_cards)

    await update.message.reply_text(response)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! to 𝐿𝑒𝓎𝓌𝒾𝓃 𝑀𝐸𝒯𝐻𝒪𝒟 bot. Use /gen to Generate 10 valid credit card.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", generate_cards))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
