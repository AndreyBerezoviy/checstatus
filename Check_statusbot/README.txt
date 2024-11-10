
# Telegram Server Monitoring Bot

This bot monitors the availability of specific server plans on Cherry Servers. When a server is "In stock", the bot notifies all subscribed users in Telegram with details about the server, including region and available quantity.

## Features

- Automatically checks server availability on the Cherry Servers website.
- Sends notifications to users when servers are available.
- Allows users to start receiving notifications by sending `/start` command.

## Prerequisites

- Python 3.8+
- Access to a server or a local environment where you can run the bot.
- `aiogram` and `playwright` libraries.
- A Telegram bot token from BotFather.

## Installation

### 1. Clone the repository or download the script file.

### 2. Install dependencies

```bash
pip install aiogram playwright
playwright install
```

### 3. Set up your Telegram bot

Replace `API_TOKEN` in the script with your bot token from BotFather.

```python
API_TOKEN = 'YOUR_API_TOKEN'
```

### 4. Run the Bot

Activate the virtual environment (optional but recommended) and start the bot:

```bash
python your_script.py
```

The bot will start polling messages on Telegram and check the server status periodically.

## Usage

### /start command

Users can subscribe to server availability notifications by sending `/start` command to the bot.

### Server Status Monitoring

The bot will periodically check the server availability on Cherry Servers and send notifications if any server from the specified plans is "In stock".

