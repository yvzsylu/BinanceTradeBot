from flask import Flask, request
import json
import telebot
from binance.client import Client
import math
import requests
from py_linq import Enumerable

app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():
    try:
    
        #Telegram bota bilgi gonderme
        def send_telegram(message):
            telebot.TeleBot('TELEGRAM_API_KEY').send_message("BOT_NUMBER",
                                                     message)
            

        def to_fixed(number, decimal_places):
            if decimal_places == 0:
                return math.floor(number)
            str_number = str(number)
            integer_part, decimal_part = str_number.split(".")
        
            if len(decimal_part) > decimal_places:
                decimal_part = decimal_part[:decimal_places]
            
            fixed_number = integer_part + "." + decimal_part
            return float(fixed_number)
        

        #Pozisyon kapatma
        def close_position(symbol,_timestamp):
            try:

                position_quantity = next(obj for obj in client.futures_account()['positions'] if obj['symbol'] == sembol)['positionAmt']
                
        
                side = Client.SIDE_BUY if float(position_quantity) < 0 else Client.SIDE_SELL
                
                client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=abs(float(position_quantity)),
                    timestamp=_timestamp
                )
                
        
            except Exception as e:
                send_telegram(f"An error occurred:{e}")


        #Pozisyon Acma
        def open_position(sembol,_side,_quantity,newSide,stopLoss,takeprofit,tp_percent,_timestamp):
            try:
                client.futures_create_order(symbol=sembol, side=_side, type='MARKET', quantity=_quantity,timestamp =_timestamp)
                client.futures_create_order(workingType='MARK_PRICE',symbol=sembol,side=newSide,type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,stopPrice=stopLoss,closePosition =True,timestamp=_timestamp)
                
                if tp_percent > 0:
                    client.futures_create_order(workingType='MARK_PRICE',symbol=sembol,side=newSide,type=Client.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,stopPrice=takeprofit,closePosition =True,timestamp=_timestamp)
        
            except Exception as e:
                send_telegram(f"pozisyonacma: {e}")
                pass
            
        #Kaldirac Ayarlama    
        def set_margin_leverage(sembol,kaldirac,_timestamp):
            try:
                isIsoleted = next(obj for obj in client.futures_account()['positions'] if obj['symbol'] == sembol)['isolated']
                client.futures_change_leverage(symbol=sembol,leverage=kaldirac,timestamp=_timestamp)
                if isIsoleted == False:
                    client.futures_change_margin_type(symbol=sembol,marginType='ISOLATED',timestamp=_timestamp) # hata donuyor
            except Exception as e:
                send_telegram(f"Leverage/Margin: {e}")
            pass
        


        #Tradingview.com dan verileri alma // PineScript'le uygun formatta veriyi webhookla bu webservise gondermelisiniz.
        # Ornek Json
        #'{"sembol":"SOLUSDT.P", "sl":"0","tp":"0", "kaldirac":"10","fiyat":"22.882",  "durum":"BUY","Zaman" : "15","stopPrice": "22.592","price":"22.882" }'
        # Herhangi bir platfromdan bu sekilde bir sinyal uretip, Json olarak gondermelisiniz. (Pipedream) 

        data = json.loads(request.data)

        time = data['Zaman']
        kaldirac = int(data ['kaldirac'])
        slPrice = float(data['stopPrice'])
        sl_percent = float(data ['sl'])
        tp_percent = float(data ['tp'])
        user_price = float(data ['price'])
        ticker = data['sembol']
        _side = data['durum']
        sembol = ticker.split('.', 1)[0]


        #userInfo = json.loads(requests.get("APIURL").text)
        #Api ile kullanici bilgileri alinabilir.

        api_key = "BINANCE_API_KEY"                 #userInfo['apikey'] / API ile alınırsa
        api_secret = "BINANCE_API_SECRET"           #userInfo['secretkey'] API ile alınırsa
        
        # Degisken Tanimlama
        
        status = None
        
        client = Client(api_key, api_secret)
        positions = client.futures_account()['positions']
        control = next(obj for obj in client.futures_account()['positions'] if obj['symbol'] == sembol)['positionAmt']
        control = int(float(control))
        send_telegram("2-Client Rama Cikti.")
        server_time = client.get_server_time()
        timestamp = server_time['serverTime']
        
        if control > 0:
            status = "BUY"
        else:
            status = "SELL"
        
        set_margin_leverage(sembol,kaldirac,timestamp)
        
        acc_balance = client.futures_account_balance()
        _balances = Enumerable(acc_balance)
        balance_result = _balances.where(lambda x: x['asset'] == 'USDT').select(lambda x: x['balance']) # balance
        result = client.futures_exchange_info()
        _symbols = Enumerable(result['symbols'])
        quantity_precision = _symbols.where(lambda x: x['symbol'] == sembol).select(lambda x: x['quantityPrecision']) # virgulden sonra rakam
        price_precision = _symbols.where(lambda x: x['symbol'] == sembol).select(lambda x: x['pricePrecision']) # price 
        _quantity_precision = int(quantity_precision[0])
        price_precision = int(price_precision[0])
        coinCurrentPrice = client.futures_symbol_ticker(symbol=sembol)
        print(balance_result[0])
        real_price = balance_result[0]
        if user_price != 0:
            real_price = user_price 
        _quantity = (float(real_price) / float(coinCurrentPrice.get('price')) * kaldirac) # quantity
        _quantity = _quantity - (_quantity * 0.03)
        _quantity = to_fixed(_quantity,_quantity_precision)
        newSide = None
        
        send_telegram("3-Miktar ve Kusurat Hesaplama")
        if _side == 'BUY':
            stopLoss =  float(coinCurrentPrice.get('price')) - (float(coinCurrentPrice.get('price')) * sl_percent)
            takeprofit =  float(coinCurrentPrice.get('price')) + (float(coinCurrentPrice.get('price')) * tp_percent)
            newSide = "SELL"
        else:
            stopLoss =  float(coinCurrentPrice.get('price')) + (float(coinCurrentPrice.get('price')) * sl_percent)
            takeprofit =  float(coinCurrentPrice.get('price')) - (float(coinCurrentPrice.get('price')) * tp_percent)
            newSide = "BUY"
        
        if sl_percent == 0:
            stopLoss = slPrice
        stopLoss = to_fixed(stopLoss,price_precision)
        takeprofit = to_fixed(takeprofit,price_precision)
        
        #Stop Loss Tale profit Tanimlama

        if control == 0:
            open_position(sembol,_side,_quantity,newSide,stopLoss,takeprofit,tp_percent,timestamp)
        
        if status != _side and control != 0:
            close_position(sembol,timestamp)
            client.futures_cancel_all_open_orders(symbol=sembol)
            open_position(sembol,_side,_quantity,newSide,stopLoss,takeprofit,tp_percent,timestamp)
        
        
        #Pozisyonlari Acma Kapatma
        
        send_telegram(f"Coin:{sembol}\nSide:{_side}\nQuantity:{_quantity}\nPrice:{coinCurrentPrice.get('price')}\nİşlem Alındı.\n\nStop Loss:{stopLoss}\nSide:{newSide}\n\nTP:{takeprofit}\nSide:{newSide}\n\nTime:{time}")
            
    except Exception as e:
        send_telegram(f"Genel: {e}")
        pass
    return {
        "code": "success",
    }