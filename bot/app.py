from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Bot API!")

@app.route('/start', methods=['POST'])
def start_bot():
    # Add your bot start logic here
    return jsonify(message="Bot Started Successfully")

@app.route('/stop', methods=['POST'])
def stop_bot():
    # Add your bot stop logic here
    return jsonify(message="Bot Stopped Successfully")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)