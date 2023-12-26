from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import current_app, jsonify
import json
import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# Initialize a Web client with your OAuth access token
authToken = os.getenv('AUTH_TOKEN')
my_secret = os.getenv('CHANNEL_ID')

client = WebClient(token=authToken)
channel_id = my_secret


def get_message_history():

  def get_user_names(user_id, users_cache):
    if user_id in users_cache:
      return users_cache[user_id]

    user_info_response = client.users_info(user=user_id)
    user_profile = user_info_response['user']['profile']
    first_name = user_profile.get('first_name', '')
    last_name = user_profile.get('last_name', '')
    users_cache[user_id] = {'first_name': first_name, 'last_name': last_name}
    return users_cache[user_id]

  def convert_ts_to_et(ts):
    utc_time = datetime.datetime.utcfromtimestamp(float(ts))
    utc_time = pytz.utc.localize(utc_time)
    eastern = pytz.timezone('US/Eastern')
    eastern_time = utc_time.astimezone(eastern)
    return eastern_time.strftime('%Y-%m-%d %H:%M:%S %Z')

  messages_info = []
  try:
    response = client.conversations_history(channel=channel_id)
    # print('<<<<MESSAGES>>>>>', json.dumps(response["messages"], indent=2))

    users_cache = {}
    for message in response['messages']:
      user_names = {'first_name': '', 'last_name': ''}  # Define user_names
      if 'user' in message:
        user_names = get_user_names(message['user'], users_cache)

      message_data = {
          "client_msg_id": message.get("client_msg_id"),
          "text": message.get("text"),
          "user": message.get("user"),
          "first_name": user_names['first_name'],
          "last_name": user_names['last_name'],
          "ts": convert_ts_to_et(message.get("ts"))  # Convert ts here
      }
      messages_info.append(message_data)

      if message.get('reply_count', 0) > 0:
        thread_ts = message['ts']
        thread_response = client.conversations_replies(channel=channel_id,
                                                       ts=thread_ts)
        for thread_message in thread_response['messages']:
          if thread_message['ts'] != thread_ts:
            if 'user' in thread_message:
              user_names = get_user_names(thread_message['user'], users_cache)

            thread_message_data = {
                "client_msg_id": thread_message.get("client_msg_id"),
                "text": thread_message.get("text"),
                "user": thread_message.get("user"),
                "first_name": user_names['first_name'],
                "last_name": user_names['last_name'],
                "ts":
                convert_ts_to_et(thread_message.get("ts"))  # Convert ts here
            }
            messages_info.append(thread_message_data)

  except SlackApiError as e:
    print(f"Error fetching conversations: {e}")

  # current_app.logger.info('Done something important...')
  # current_app.logger.info(messages_info)
  # current_app.logger.info(jsonify(messages_info))


  return messages_info

if __name__ == "__main__":
  get_message_history()
