import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# --- Flask Server for 24/7 Hosting ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    # Render default port use karega
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Configuration ---
API_TOKEN = '8743636826:AAFF_pXt8NtWFFvbpBQGa_ppUYsZ1aB42Zg'
ADMIN_ID = 8077226075
CHANNEL_LINK = "https://t.me/+lCjhMJ_UWeUyZTI1"
CHANNEL_ID = -1003104991859 

bot = telebot.TeleBot(API_TOKEN)
free_keys_list = []

# --- Attractive Price List ---
PRICE_LIST_TEXT = (
    "🔥 *SPECIAL OFFER* 🔥\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "✅ *LOADER OR MOD AVAILABLE*\n"
    "🏆 *ONLY FOR FIRST 10 MEMBERS*\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "✔️ *1 DAY* = 49 RS\n"
    "✔️ *3 DAY* = 99 RS\n"
    "✔️ *7 DAY* = 149 RS\n"
    "✔️ *15 DAY* = 299 RS\n"
    "✔️ *30 DAY* = 399 RS\n"
    "✔️ *60 DAY* = 599 RS\n"
    "✔️ *FULL SEASON* = 599 RS\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "💰 *MAIN ID FULL SAFE* 💯\n"
    "⚡ *Instant Delivery after Payment*"
)

# Membership Check Logic
def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return False

# Admin Command: Add Free Keys
@bot.message_handler(commands=['addfree'])
def add_free_key(message):
    if message.from_user.id == ADMIN_ID:
        try:
            key = message.text.split(maxsplit=1)[1]
            free_keys_list.append(key)
            bot.reply_to(message, f"✅ *Key Added!* \nTotal Stock: `{len(free_keys_list)}`", parse_mode='Markdown')
        except:
            bot.reply_to(message, "❌ Format: `/addfree KEY_HERE`")

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_free = types.InlineKeyboardButton("🎁 Get Free Key", callback_data="check_task")
    btn_paid = types.InlineKeyboardButton("💳 Paid Key", callback_data="paid_menu")
    markup.add(btn_free, btn_paid)
    
    welcome_text = (
        f"✨ *Namaste {message.from_user.first_name}!* ✨\n\n"
        "Hamare *Official Key Store* mein aapka swagat hai.\n"
        "Sabse sasti aur safe keys yahan milti hain.\n\n"
        "👇 *Niche diye gaye options select karein:*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id

    if call.data == "check_task" or call.data == "verify_now":
        if check_membership(user_id):
            if len(free_keys_list) > 0:
                key = free_keys_list.pop(0)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                     text=f"✅ *Verification Success!* ✅\n\n🔑 *Your Key:* `{key}`\n\nAb aap ise use kar sakte hain! 🔥", 
                                     parse_mode='Markdown')
                bot.send_message(ADMIN_ID, f"📢 *Free Key Distributed!*\n👤 User: {call.from_user.first_name}\n🔑 Key: `{key}`")
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                     text="❌ *Out of Stock!*\n\nAbhi koi free key available nahi hai. Admin jald hi aur add karenge!", 
                                     parse_mode='Markdown')
        else:
            # Task Approval Buttons
            markup = types.InlineKeyboardMarkup()
            btn_join = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
            btn_verify = types.InlineKeyboardButton("✅ Verify / Approval", callback_data="verify_now")
            markup.add(btn_join)
            markup.add(btn_verify)
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 text="⚠️ *TASK:* Free key ke liye pehle niche link se channel join karein aur *Approval* button dabayein.", 
                                 reply_markup=markup, parse_mode='Markdown')

    elif call.data == "paid_menu":
        markup = types.InlineKeyboardMarkup()
        btn_price = types.InlineKeyboardButton("📋 View Price List", callback_data="show_price")
        btn_back = types.InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
        markup.add(btn_price, btn_back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="💳 *Premium Paid Keys*\n\nPrice list dekhne ke liye niche button dabayein.", 
                             reply_markup=markup, parse_mode='Markdown')

    elif call.data == "show_price":
        markup = types.InlineKeyboardMarkup()
        btn_buy = types.InlineKeyboardButton("🛒 Buy Now (Contact Admin)", url=f"tg://user?id={ADMIN_ID}")
        btn_back = types.InlineKeyboardButton("🔙 Back", callback_data="paid_menu")
        markup.add(btn_buy, btn_back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text=PRICE_LIST_TEXT, reply_markup=markup, parse_mode='Markdown')

    elif call.data == "back_to_start":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)

# --- Execution ---
if __name__ == "__main__":
    print("🚀 Bot is LIVE with ID Verification and Keep-Alive...")
    keep_alive() # Web server starts here
    bot.infinity_polling() # Bot starts polling here
