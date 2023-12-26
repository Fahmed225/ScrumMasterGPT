from flask import Flask, jsonify
from slack_message_history import get_message_history
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/getSlackMessageHistory', methods=['GET'])
def get_slack_message_history():
  response = jsonify(get_message_history())
  response.mimetype = 'application/json'  # Ensure mimetype is set
  return response


app.run(host='0.0.0.0', port=81)
