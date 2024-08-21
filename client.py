from openai import OpenAI 

client = OpenAI(
  api_key="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",
)
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)