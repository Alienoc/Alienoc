import random
import requests
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Environment variable for Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# BIN API Key (directly included in the script)
BIN_API_KEY = '3c0472522emsh371a89fd9cb7807p177d09jsn4a7329306aed'
BIN_API_URL = "https://bin-info-checker-api.p.rapidapi.com/info2"

# Function to validate Luhn
def is_valid_luhn(number):
    total = 0
    reverse_digits = list(map(int, str(number)))[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit = digit * 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0

# Function to calculate Luhn check digit
def calculate_luhn(bin_code):
    cc = bin_code
    while len(cc) < 15:  # Generate up to 15 digits
        cc += str(random.randint(0, 9))
    check_digit = (10 - (sum(map(int, str(cc)[::-1])) % 10)) % 10
    cc += str(check_digit)
    return cc

# Function to generate random expiry date (MM|YYYY)
def generate_expiry():
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2025, 2030))
    return month, year

# /start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    update.message.reply_text(
        "Hi, welcome to Siekevitz's CC generator Bot!", parse_mode="MarkdownBold"
    )

# /gen command (Generate 10 CCs based on BIN)
def gen(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) != 1:
        update.message.reply_text("Please provide a BIN code.")
        return

    bin_code = context.args[0]
    
    # Generate 10 credit cards
    cards = []
    for _ in range(10):
        cc = calculate_luhn(bin_code)  # Generate valid CC number using Luhn
        expiry_month, expiry_year = generate_expiry()
        cards.append(f"{cc}|{expiry_month}|{expiry_year}|{random.randint(100, 999)}")

    # Send the generated cards with the requested format
    response = "\n".join(cards)
    update.message.reply_text(
        f"𝗜𝗻𝗳𝗼: MASTERCARD - DEBIT - CIRRUS\n𝗕𝗮𝗻𝗸: BANCO SANTANDER, S.A,\n𝗖𝗼𝘂𝗻𝗧𝗿𝘆: MEXICO\n━━━━━━━━⊛\n{response}\n━━━━━━━━━━━━━━━━━\n| Format: 55471820094xxxxx|09|2029|rnd\n| Amount: 5"
    )

# /bin command (Get BIN info from API)
def bin_info(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) != 1:
        update.message.reply_text("Please provide a BIN code.")
        return

    bin_code = context.args[0]
    headers = {
        "x-rapidapi-host": "bin-info-checker-api.p.rapidapi.com",
        "x-rapidapi-key": BIN_API_KEY
    }

    # API Request to get BIN info
    response = requests.get(f"{BIN_API_URL}?bin={bin_code}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            update.message.reply_text(f"Error: {data['error']}")
        else:
            info = data.get('data', {})
            bank = info.get('bank', 'Unknown Bank')
            scheme = info.get('scheme', 'Unknown Scheme')
            type_ = info.get('type', 'Unknown Type')
            update.message.reply_text(f"𝗕𝗮𝗻𝗸: {bank}\n𝗦𝗰𝗵𝗲𝗺𝗲: {scheme}\n𝗧𝘆𝗽𝗲: {type_}")
    else:
        update.message.reply_text("Failed to retrieve BIN info.")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers for the commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen", gen))
    dp.add_handler(CommandHandler("bin", bin_info))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
