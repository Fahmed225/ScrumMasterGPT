from openai import OpenAI
from dotenv import load_dotenv
from slack_message_history import get_message_history
import json
import time

load_dotenv()
client = OpenAI()

# slackMessages = get_message_history()
# jsonMessages = json.dumps(slackMessages, indent=2)
# jsonMessages = jsonMessages.replace("}", "")
# # save jsonMessages to a file
#     with open("jsonMessages.json", "w") as outfile:
#         outfile.write(jsonMessages)
    
slack_extractor_assistant = client.beta.assistants.retrieve("asst_27s57CBocuIcKDwUekJjPg5e")

file = client.files.create(
    file=open("cachedMessages.json", "rb"),
    purpose="assistants"
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Please take the chat history.",
      "file_ids": [file.id]
    }
  ]
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=slack_extractor_assistant.id
)

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

run = wait_on_run(run, thread)
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
# save value to a file
with open("output.json", "w") as outfile:
    outfile.write(messages.data[0].content[0].text.value)

