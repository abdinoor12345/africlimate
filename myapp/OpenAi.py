from openai import OpenAI
client = OpenAI()
key="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"

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)