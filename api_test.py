from openai import OpenAI

client = OpenAI(api_key="sk-7eedc4709ec24c4284b5f5f90316f36d", base_url="[https://api.deepseek.com](https://api.deepseek.com/)")

response = client.chat.completions.create(
model="deepseek-chat",
messages=[
{"role": "system", "content": "You are a helpful assistant"},
{"role": "user", "content": "Hello"},
],
stream=False
)

print(response.choices[0].message.content)