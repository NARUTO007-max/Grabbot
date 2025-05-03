from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Import routes after app is initialized
from bot.routes import main
app.register_blueprint(main)