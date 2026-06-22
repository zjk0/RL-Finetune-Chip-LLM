from openai import OpenAI
import os

# os.environ["all_proxy"] = "http://127.0.0.1:7897/"

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Write a code to calculate the Fibonacci sequence up to the 10th number."},
    ],
    max_tokens=12800,
    temperature=0.7,
    stream=False,
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)