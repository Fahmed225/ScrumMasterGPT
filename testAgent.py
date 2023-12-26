from openai import OpenAI
client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a personal secretary. When asked a to write an email, ask for who to send it to and try to get a gist of it so you can compose an email. Verify before sending email.",
    name="Secretary",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)
print(my_assistant)
