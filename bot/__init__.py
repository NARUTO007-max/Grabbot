from flask import Flask

# Flask app initialize karte hain
app = Flask(__name__)

# Importing routes
from bot import routes

# Optional: Additional configuration or app setup can be done here
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Bot ke liye koi extra settings agar ho toh woh bhi yahan define kar sakte hain.