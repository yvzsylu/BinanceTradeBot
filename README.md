# BinanceTradeBot

## Description

This project is a web service written in Python. It is created using Flask. The service receives signals generated with any indicator via webhook in the appropriate format and posts these data using the Binance API to perform trades on the Binance exchange. It can open or close positions using these signals. Additionally, it can send a message to a Telegram bot to record each trade.

## Requirements

- Python
- Flask
- Binance API
- Telegram bot API

## Installation

1. Clone the project:

```bash
git clone https://github.com/yvzsylu/BinanceTradeBot
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Navigate to the project directory:

```bash
cd your_project
```

Start the web service by running the following command:

```bash
python app.py
```

Webhook configuration is required. You can use platforms such as:

Discord
Slack
GitHub
Any custom HTTP service

Add your Binance API key and Telegram bot API key to the appropriate places in the project.
Note: You need to set up api key settings from Binance.


## Webhook JSON Example
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


