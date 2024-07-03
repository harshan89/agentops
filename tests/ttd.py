from openai import OpenAI, AsyncOpenAI
import openai
from openai.resources.chat import completions
import agentops
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


# Assuming that initializing will trigger the LlmTracker to override methods
agentops.init(tags=["TTD Test", openai.__version__])

chat_completion_1 = client.chat.completions.create(
    messages=[
        {
            "content": "Come up with a random superpower that is not time travel. Just return the superpower.",
            "role": "user",
        }
    ],
    model="gpt-3.5-turbo",
)
content1 = chat_completion_1.choices[0].message.content
print(content1)

chat_completion_2 = client.chat.completions.create(
    messages=[
        {
            "content": "Come up with a superhero name given this superpower: "
            + content1
            + ". Just return the superhero name.",
            "role": "user",
        }
    ],
    model="gpt-3.5-turbo",
)
content2 = chat_completion_2.choices[0].message.content
print(content2)

chat_completion_3 = client.chat.completions.create(
    messages=[
        {
            "content": "Come up with the superpower of superhero "
            + content2
            + "'s arch nemesis. The superpower cannot be time travel. Just return the superpower.",
            "role": "user",
        }
    ],
    model="gpt-3.5-turbo",
)
content3 = chat_completion_3.choices[0].message.content
print(content3)

chat_completion_4 = client.chat.completions.create(
    messages=[
        {
            "content": "Given the following superpower of a villainous character, come up with the villain's name. Just return the villain's name. Superpower: "
            + content3,
            "role": "user",
        }
    ],
    model="gpt-3.5-turbo",
)
content4 = chat_completion_4.choices[0].message.content
print(content4)


chat_completion_5 = client.chat.completions.create(
    messages=[
        {
            "content": "Write a 100 word superhero story about the feud between superhero"
            + content2
            + " and his arch nemesis "
            + content4,
            "role": "user",
        }
    ],
    model="gpt-3.5-turbo",
)
content5 = chat_completion_5.choices[0].message.content
print(content5)

agentops.end_session("Success")
