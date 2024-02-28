"""
WELCOME TO THE COINEX TRADING BOT!

Our Crypto Trading bot is a powerful tool that utilizes the CCXT library
in Python programming language to forecast market trends,
execute trades, and analyze data from the CoinEx exchange.
With advanced algorithms and machine learning capabilities,
our bot can make informed decisions based on real-time market data
to maximize profits and minimize risks.

The bot is designed to automate the trading process,
allowing users to set their preferred trading parameters
and let the bot do the rest. It can analyze historical data,
identify patterns, and make predictions
on future price movements with a high degree of accuracy.

Additionally, our Crypto Trading bot offers a user-friendly interface
that allows traders to monitor their portfolio, track performance metrics,
and adjust trading strategies in real-time.
With seamless integration with the CoinEx exchange,
users can execute trades quickly and efficiently without any manual intervention.

Overall, our Crypto Trading bot is a valuable tool for
both novice and experienced traders looking to optimize their trading strategies
and achieve consistent profits in the volatile cryptocurrency market.
"""

pip install pyTelegramBotAPI

pip install fastapi

pip install uvicorn

pip install python-multipart

pip install kaleido

pip install -U kaleido

pip install orca

pip install plotly

pip install newsapi-python

pip install yfinance

pip install ccxt

import telebot
bot = telebot.TeleBot('BOT TOKEN HERE')

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Define the custom keyboard
custom_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
trade_button = telebot.types.KeyboardButton('🔄Trade')
summary_button = telebot.types.KeyboardButton('📝Summary')
forcast_button = telebot.types.KeyboardButton('☔Forcast')
help_button = telebot.types.KeyboardButton('👐🏻Help')
custom_keyboard.add(trade_button,summary_button,forcast_button,help_button)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Define the sub keyboard of Trade
sub_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
login_button = telebot.types.KeyboardButton('👤Login')
Balance_button = telebot.types.KeyboardButton('💰Balance')
order_button = telebot.types.KeyboardButton('🛒Order')
cancel_button = telebot.types.KeyboardButton('🚫Cancel Order')
Info_Bid_button = telebot.types.KeyboardButton('💸Bid Info')
back_button = telebot.types.KeyboardButton('🔙Back')
sub_keyboard.add(login_button,Balance_button,order_button,cancel_button,Info_Bid_button,back_button)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

@bot.message_handler(func=lambda message: message.text == '🔙Back')
def handle_button_click(message):
    bot.send_message(message.chat.id, "─── ⋆⋅☆⋅⋆ ── Back to Home ─── ⋆⋅☆⋅⋆ ──", reply_markup=custom_keyboard)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Define the Back
back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = telebot.types.KeyboardButton('🔙Back')
back_keyboard.add(back_button)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, " 👋🏻 WELCOME TO THE COINEX TRADING BOT 👋🏻", reply_markup=custom_keyboard)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Handle the 'Summary'
@bot.message_handler(func=lambda message: message.text == '📝Summary')
def handle_button_click(message):
    bot.send_message(message.chat.id, "Please provide the name of the currency 🪙")
    bot.register_next_step_handler(message, show_news)

def show_news(message):

  CurrencyName = message.text

  bot.send_message(message.chat.id, f"The Chart of: {CurrencyName} 📈")

  import yfinance as yf
  import pandas as pd
  import datetime as dt
  import dateutil.relativedelta


  now = dt.datetime.now()
  start = now + dateutil.relativedelta.relativedelta(months=-1)
  df = yf.download(CurrencyName, start, now)

  import plotly.graph_objects as go
  fig = go.Figure(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close']))
  # hide weekends
  fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
  # removing all empty dates
  # build complete timeline from start date to end date
  dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
  # retrieve the dates that ARE in the original datset
  dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
  # define dates with missing values
  dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
  fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

  # add moving averages to df
  df['MA20'] = df['Close'].rolling(window=20).mean()
  df['MA5'] = df['Close'].rolling(window=5).mean()

  fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA5'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='MA 5'))
  fig.add_trace(go.Scatter(x=df.index,
                          y=df['MA20'],
                          opacity=0.7,
                          line=dict(color='orange', width=2),
                          name='MA 20'))

  fig_chart = fig



  fig_chart.write_image("fig_chart.png", width=800, height=600, scale=2)
  bot.send_photo(message.chat.id, open("fig_chart.png", 'rb'))
  bot.send_message(message.chat.id, f"Last CLOSED price of {CurrencyName} is 💵🔒: {df['Close']}")


  bot.send_message(message.chat.id, f"The news about: {CurrencyName}")

  from newsapi import NewsApiClient
  newsapi = NewsApiClient(api_key='NEWS API KEY HERE')
  all_articles = newsapi.get_everything(q=CurrencyName,language='en',sort_by='popularity',page_size=5)
  for article in all_articles['articles']:
      source = article['source']['name']
      title = article['title']
      description = article['description']
      url = article['url']

      divider = '꒦꒷꒦꒷꒦꒷꒦꒷꒦꒷꒦꒷꒷꒦꒷꒦꒷꒦꒷꒦꒷꒦꒷꒷꒦꒷꒦꒷꒦꒷꒦꒷꒦꒷꒷꒦꒷꒦'
      bot.send_message(message.chat.id, divider)
      bot.send_message(message.chat.id, f"Source 📰: {source}")
      bot.send_message(message.chat.id, f"Tile ✍🏻 : {title}")
      bot.send_message(message.chat.id, f"Description 📙: {description}")
      bot.send_message(message.chat.id, f"url 🌐:{url}")

  bot.send_message(message.chat.id, "Done !✅",reply_markup=back_keyboard)



#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# META Prophet
# Handle the 'Forcast'
@bot.message_handler(func=lambda message: message.text == '☔Forcast')
def forcast(message):
    bot.send_message(message.chat.id, f"Please provide your desired currency 💲 ")
    bot.register_next_step_handler(message, get_currency_forcast)


def get_currency_forcast(message):
    CurrencyForcast = message.text
    bot.send_message(message.chat.id, f"Please provide your desire time to forcast in providing format📅,  ✨example: 2024-02-20 17:20:30")
    bot.register_next_step_handler(message, lambda message:forcasting(message,CurrencyForcast))


def forcasting(message,CurrencyForcast):
    Date_Forcast = message.text
    print(Date_Forcast)

    import yfinance
    import datetime as dt

    start = dt.datetime(2020,1,1)
    end = dt.datetime.now()
    data = yfinance.download(CurrencyForcast, start, end)

    data.to_csv("Stock_data.csv")
    import pandas as pd
    data = pd.read_csv("Stock_data.csv")
    data = data[["Date","Close"]]
    data.columns = ["ds", "y"]

    from prophet import Prophet
    prophet = Prophet(daily_seasonality=True)
    prophet.fit(data)
    future_dates = prophet.make_future_dataframe(periods=180)
    predictions = prophet.predict(future_dates)

    from prophet.plot import plot_plotly
    fig = plot_plotly(prophet, predictions)

    fig.write_image("fig1.png", width=800, height=600, scale=2)

    future = pd.DataFrame({'ds': pd.to_datetime([Date_Forcast])})
    forecast = prophet.predict(future)
    f1=(forecast[['ds', 'yhat']])

    original_string = f"{f1}"
    characters_to_remove = "dsyhat"

    result_string = original_string
    for char in characters_to_remove:
        result_string = result_string.replace(char, "")



    bot.send_photo(message.chat.id, open("fig1.png", 'rb'))
    bot.send_message(message.chat.id, f"The forcasting for {CurrencyForcast} in this time is 🔮: {result_string}",reply_markup=back_keyboard)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Handle the 'Help'
@bot.message_handler(func=lambda message: message.text == '👐🏻Help')
def handle_button_click(message):
  welcome_message =  "Welcome to the ✦ COINEX TRADING BOT ✦ ,Our Crypto Trading bot is a powerful tool that utilizes the CCXT library in Python programming language to forecast market trends, execute trades, and analyze  data from the CoinEx exchange. With advanced algorithms and machine learning capabilities, our bot can make informed decisions based on real-time market data to maximize profits and minimize risks. The bot is designed to automate the trading process, allowing users to set their preferred trading parameters and let the bot do the rest. It can analyze historical data, identify patterns, and make predictions on future price movements with a high degree of accuracy.Additionally, our Crypto Trading bot offers a user-friendly interface that allows traders to monitor their portfolio, track performance metrics, and adjust trading strategies in real-time. With seamless integration with the CoinEx exchange, users can execute trades quickly and efficiently without any manual intervention. Overall, our Crypto Trading bot is a valuable tool for both novice and experienced traders looking to optimize their trading strategies and achieve consistent profits in the volatile cryptocurrency market."
  bot.send_message(message.chat.id, welcome_message,reply_markup=back_keyboard)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Handle the 'Trade'
@bot.message_handler(func=lambda message: message.text == '🔄Trade')
def handle_button_click(message):
    bot.send_message(message.chat.id, "─── ⋆⋅☆⋅⋆ ── Wecome to Trade section ─── ⋆⋅☆⋅⋆ ──", reply_markup=sub_keyboard)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆

# Handle the 'Login'
@bot.message_handler(func=lambda message: message.text == '👤Login')
def handle_button_click(message):
    bot.send_message(message.chat.id, "Please provide your CoinEx API Keyword 🔒")
    bot.register_next_step_handler(message, get_API_Key)


def get_API_Key(message):
    API_Key = message.text
    bot.send_message(message.chat.id, "Please enter the Secret Key 🔑")
    bot.register_next_step_handler(message, lambda message: get_Secret_Key(message, API_Key))


def get_Secret_Key(message, API_Key):
    Secret_Key = message.text
    bot.send_message(message.chat.id, f"Your API Key🔒 is: {API_Key}\nYour Secret Key 🔑 is: {Secret_Key}",reply_markup=sub_keyboard)

    """ API Keys """
    authentication = {}

    authentication["apiKey"] = API_Key
    authentication["secret"] = Secret_Key
    bot.send_message(message.chat.id, f"{authentication} Login Success!")

    import ccxt
    exchange = ccxt.coinex(authentication)
    markets = exchange.loadMarkets()

    @bot.message_handler(func=lambda message: message.text == '💰Balance')
    def Balance(message):
      fetch_all_balance = exchange.fetchBalance()

      usdt_available = exchange.fetchBalance()['USDT']['free']
      bot.send_message(message.chat.id,f"{usdt_available} USDT")

      bnb_available = exchange.fetchBalance()['BNB']['free']
      bot.send_message(message.chat.id,f"{bnb_available} BNB")

    # Bid Price
    @bot.message_handler(func=lambda message: message.text == '💸Bid Info')
    def bid(message):
      ticker = exchange.fetchTicker('ADA/USDT')
      bot.send_message(message.chat.id,f"Bid price is: {ticker['bid']} USDT")


    class OrderBot:
        def __init__(self):
          self.order_data = {}

        def start_order(self, chat_id):
            bot.send_message(chat_id, "Please select Order Side Buy/Sell")
            bot.register_next_step_handler_by_chat_id(chat_id, self.get_order_side)

        def get_order_side(self, message):
            self.order_data['order_side'] = message.text
            bot.send_message(message.chat.id, "Please enter the amount in USDT")
            bot.register_next_step_handler(message, self.get_amount)

        def get_amount(self, message):
            self.order_data['amount'] = message.text
            bot.send_message(message.chat.id, "Please enter the symbol/coin")
            bot.register_next_step_handler(message, self.get_symbol)

        def get_symbol(self, message):
            self.order_data['symbol'] = message.text
            bot.send_message(message.chat.id, "Please enter the base price")
            bot.register_next_step_handler(message, self.get_base_price)

        def get_base_price(self, message):
            self.order_data['base_price'] = message.text
            bot.send_message(message.chat.id, "Order details: {}".format(self.order_data))

            """ Orders """

            symbol = self.order_data['symbol']
            order_type = 'limit'
            side = self.order_data['order_side']

            base_price = float(self.order_data['base_price'])  # The price at which you want to buy or sell

            # 1 USDT
            amount_in_usdt = float(self.order_data['amount'])
            # amount_in_usdt = usdt_available / 2.
            current_price = (exchange.fetchTicker(symbol)['ask'] + exchange.fetchTicker(symbol)['bid'] ) / 2
            amount = amount_in_usdt / current_price

            order = exchange.createOrder(symbol, order_type, side, amount, base_price)
            bot.send_message(message.chat.id,f"Order Info: {order} ")

            @bot.message_handler(func=lambda message: message.text == '🚫Cancel Order')
            def cancel(message):
              cancelorder = exchange.cancelOrder(order['id'], symbol)
              bot.send_message(message.chat.id,f"Cancel Order Info: {cancelorder} ")


    order_bot = OrderBot()
    @bot.message_handler(func=lambda message: message.text == '🛒Order')
    def handle_start(message):
      order_bot.start_order(message.chat.id)

#☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆★☆★☆☆★☆


bot.polling()