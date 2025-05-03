from flask import Flask

# Flask app initialize karte hain
app = Flask(__name__)

# Importing routes
from bot import routes

# Optional: Additional configuration or app setup can be done here
# (SECRET_KEY ki zarurat nahi hai agar sessions/forms use nahi kar rahe)