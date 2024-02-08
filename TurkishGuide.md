# BinanceTradeBot

## Açıklama

Bu proje, Python dilinde yazılmış bir web servisidir. Flask kullanılarak oluşturulmuştur. Servis, herhangi bir gösterge tarafından üretilen sinyalleri uygun formatta bir webhook aracılığıyla alır ve bu verileri Binance API kullanarak Binance borsasında işlemler yapmak için yayınlar. Bu sinyalleri kullanarak pozisyonları açabilir veya kapatabilir. Ayrıca, her işlemi kaydetmek için bir Telegram botuna bir mesaj gönderebilir.

## Gereksinimler

- Python
- Flask
- Binance API
- Telegram bot API

## Kurulum

1. Projeyi klonlayın:

```bash
git clone https://github.com/yvzsylu/BinanceTradeBot
```

Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

Proje dizinine gidin:

```bash
cd [Your_Project_Path]
```

Web servisi başlatmak için aşağıdaki komutu çalıştırın:

```bash
python app.py
```

Webhook yapılandırması gereklidir. Şu platformları kullanabilirsiniz:

- PipeDream
- Discord
- Slack
- GitHub
- Herhangi bir özel HTTP servisi

Projedeki uygun yerlere Binance API anahtarınızı ve Telegram bot API anahtarınızı ekleyin.
Not: Binance'den API anahtar ayarlarını yapmanız gerekmektedir.


## Webhook JSON Örneği
```json
{
    "symbol": "SOLUSDT.P",
    "sl": "0",
    "tp": "0",
    "leverage": "10",
    "price": "22.882",
    "status": "BUY",
    "time": "15",
    "stopPrice": "22.592",
    "orderPrice": "22.882"
}
```


