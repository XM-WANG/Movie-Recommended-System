import time
import logging
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import urllib.parse as up
import urllib.request as ur
#########################功能型函数##########################
def sendReq(values,url):
    #url = 'http://127.0.0.1:5000/ '
    # values = {'req':'/start'}
    data = up.urlencode(values)
    data = data.encode('ascii')
    req = ur.Request(url, data)
    with ur.urlopen(req) as response:
        page = response.read()
        page = page.decode('ascii')
    return page
#########################start函数##########################
def start(chat_id): #判断新老用户，最后将print改为send
    url = 'http://127.0.0.1:5000/register '
    values = {'chat_id': chat_id}
    res = eval(sendReq(values, url))
    if res['exists'] == 1:
        print("Welcome back!")
        bot.sendMessage(chat_id, "Welcome back!")
    elif res['exists'] == 0:
        print('Welcome!')
        bot.sendMessage(chat_id, "Welcome!")
    else:
        print('something must be wrong!')
#####################get_unrated_movie函数#################
def get_unrated_movie(chat_id):
    url = 'http://127.0.0.1:5000/get_unrated_movie'
    values = {'chat_id': chat_id}
    res = sendReq(values, url)
    js = eval(res)
    return js#这里返回的是个字典也就是个json
#####################键盘函数####################
def keybd(chat_id,movie_id,rating):
    url= 'http://127.0.0.1:5000/get_unrated_movie/status'
    values = {"chat_id":chat_id,"movie_id":movie_id,"rating":rating}
    req ={"values":values}
    res = sendReq(req, url)
    js = eval(res)
    if js['status']=="success":
        print("Ok")
    else:
        print("Wrong")
#####################推荐函数####################
def rec(chat_id):
    url = 'http://127.0.0.1:5000/recommend'
    values = {"chat_id": chat_id, "top_n":3}
    req = {"values": values}
    res = sendReq(req, url)
    return res

logging.basicConfig(level=logging.INFO)
r = {}
l = []


def handle(msg):
    """
    A function that will be invoked when a message is
    recevied by the bot
    """
    # Get text or data from the message
    text = msg.get("text", None)
    data = msg.get("data", None)

    if data is not None:
        # This is a message from a custom keyboard
        chat_id = msg["message"]["chat"]["id"]
        content_type = "data"
    elif text is not None:
        # This is a text message from the user
        chat_id = msg["chat"]["id"]
        content_type = "text"
    else:
        # This is a message we don't know how to handle
        content_type = "unknown"

    if content_type == "text":
        message = msg["text"]
        logging.info("Received from chat_id={}: {}".format(chat_id, message))

        if message == "/start":
            start(chat_id)


        elif message == "/rate":
            js = get_unrated_movie(chat_id)
            print(js)
            r["movie_id"] = js["movieId"]
            backword =str(js['title'])+str(js['url'])
            bot.sendMessage(chat_id,backword)

            # Create a custom keyboard to let user enter rating
            my_inline_keyboard = [[
                InlineKeyboardButton(text='1', callback_data='rate_movie_1'),
                InlineKeyboardButton(text='2', callback_data='rate_movie_2'),
                InlineKeyboardButton(text='3', callback_data='rate_movie_3'),
                InlineKeyboardButton(text='4', callback_data='rate_movie_4'),
                InlineKeyboardButton(text='5', callback_data='rate_movie_5')
            ]]
            keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)
            bot.sendMessage(chat_id, "How do you rate this movie?", reply_markup=keyboard)

        elif message == "/recommend":
            # Ask the server to generate a list of
            # recommended movies to the user
            if len(l)<10:
                bot.sendMessage(chat_id, "Please finish rating firstly.")
            else:
                req = rec(chat_id)
                js = eval(req)
                movieList = js["movies"]
                for i in range(len(movieList)):
                    message = str(movieList[i]["title"])+'\n'+str(movieList[i]["url"])
                    bot.sendMessage(chat_id,message)

        else:
            # Some command that we don't understand
            bot.sendMessage(chat_id, "I don't understand your command.")

    elif content_type == "data":
        # This is data returned by the custom keyboard
        # Extract the movie ID and the rating from the data
        # and then send this to the server
        movie_id = r['movie_id']
        rating = data
        keybd(chat_id, movie_id, rating)
        logging.info("Received rating: {}".format(data))
        bot.sendMessage(chat_id, "Your rating is received!")
        l.append(movie_id)


if __name__ == "__main__":

    # Povide your bot's token
    bot = telepot.Bot("620336112:AAHlqfRRVrYY6VwN9RPrpFWiD9ZuSClEvvo")
    MessageLoop(bot, handle).run_as_thread()

    while True:
        time.sleep(10)