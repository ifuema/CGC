import openai
openai.api_key = ''

messages = [{"role": "user", "content": 'clear'}]
while True:
    if messages[len(messages)-1]['content'] == 'clear':
        messages = [{"role": "user", "content": '你好'}]
        print()
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print("\033[36m" + completion.choices[0].message.content + "\033[0m")
    messages.append(completion.choices[0].message)
    messages.append({"role": "user", "content": input()})
