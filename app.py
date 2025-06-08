from flask import Flask
import threading
from bot import start_bot
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot rodando com sucesso!'

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
