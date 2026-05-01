import os
import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-5b13a90466bf48c9af7f477a4d6bac8e",
    base_url="https://api.deepseek.com",
    max_retries=0,
)

for i in range(5):
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "只回复ok"}],
            max_tokens=8,
            stream=False,
        )
        print(i, "SUCCESS", resp.choices[0].message.content)
    except Exception as e:
        print(i, "FAILED", repr(e))
    time.sleep(2)