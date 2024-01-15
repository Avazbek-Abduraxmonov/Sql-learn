import telebot
import sqlite3
bot = telebot.TeleBot(token='API_TOKEN')

name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('baza.sql',isolation_level=None, check_same_thread=False,)
    cur = conn.cursor()


    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER AUTO_INCREMENT PRIMARY KEY,)")
    conn.commit()
    cur.close()
    conn.close()


    bot.send_message(message.chat.id, "Salom Botimizga xush kleibsiz\nRoyxatdan otish uchun Ismingizni kiriting")
    bot.register_next_step_handler(message, user_name)




def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Parol kiriting")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('baza.sql',isolation_level=None, check_same_thread=False,)
    cur = conn.cursor()


    cur.execute(f"INSERT INTO users(name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Korish", callback_data='users'))

    bot.send_message(message.chat.id, "Royxatdan otish yakunlandi", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('baza.sql',isolation_level=None, check_same_thread=False,)
    cur = conn.cursor()


    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    
    info = ''
    for el in users:
        info += f'Name: {el[1]}, password: {el[2]}\n'

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)
if __name__ == '__main__':
    bot.polling()
