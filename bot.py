#!/usr/bin/env python3
"""
🤖 SIMPLE TEST BOT FOR CHOREO
This WILL work if Choreo is configured correctly
"""

import os
import logging
from flask import Flask
from threading import Thread

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get token from environment
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Flask app for health checks (REQUIRED for Choreo)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Simple Bot is RUNNING on Choreo"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "pong", 200

@app.route('/test')
def test():
    return f"""
    <h1>🤖 Simple Bot Test</h1>
    <p>Status: ✅ Running</p>
    <p>Telegram Token: {'✅ SET' if TOKEN else '❌ NOT SET'}</p>
    <p>If token is set, bot should respond to /start in Telegram</p>
    """

def run_flask():
    """Run Flask server on port 8080 (Choreo requirement)"""
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Starting web server on port {port}")
    print(f"📡 Health check: http://0.0.0.0:{port}/health")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

def main():
    print("=" * 60)
    print("🤖 SIMPLE BOT STARTING")
    print("=" * 60)
    
    # Start Flask server first (Choreo needs this)
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    import time
    time.sleep(2)
    
    print("✅ Web server started")
    print(f"🔑 Telegram Token: {'✅ PRESENT' if TOKEN else '❌ MISSING'}")
    
    if TOKEN:
        # Import telegram inside the condition to avoid errors if token missing
        try:
            from telegram import Update
            from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
            
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                """Simple start command"""
                await update.message.reply_text("🎉 SIMPLE BOT IS WORKING! Test successful!")
            
            async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
                """Ping command"""
                await update.message.reply_text("🏓 Pong! Bot is alive and responding.")
            
            # Create and start Telegram bot
            print("🤖 Starting Telegram bot...")
            telegram_app = ApplicationBuilder().token(TOKEN).build()
            telegram_app.add_handler(CommandHandler("start", start))
            telegram_app.add_handler(CommandHandler("ping", ping_cmd))
            
            print("=" * 60)
            print("✅ BOT IS READY!")
            print("📱 Send /start or /ping in Telegram")
            print("=" * 60)
            
            telegram_app.run_polling(drop_pending_updates=True)
            
        except ImportError as e:
            print(f"❌ Missing python-telegram-bot: {e}")
            print("Add to requirements.txt: python-telegram-bot==20.7")
        except Exception as e:
            print(f"❌ Telegram bot error: {e}")
    else:
        print("⚠️ TELEGRAM_BOT_TOKEN not set in environment")
        print("Add it in Choreo → Environment Variables")
        print("=" * 60)
        print("📡 Web server is still running for health checks")
        print("💡 Set token to enable Telegram bot")
        print("=" * 60)
        
        # Keep the script running
        while True:
            time.sleep(3600)

if __name__ == "__main__":
    main()
