import pickle

import openai

openai.api_key = ''

messages = [{"role": "user", "content": 'clear'}]
ini_model = {'history': []}
ini = {}
title = ''


def read_ini():
    global ini
    try:
        with open("ChatGPT.pkl", "rb") as f:
            ini = pickle.load(f)
    except:
        ini = {}


def write_ini():
    with open("ChatGPT.pkl", "wb") as f:
        pickle.dump(ini, f)


while True:
    match messages[len(messages) - 1]['content']:
        case 'clear':
            messages = [{"role": "user", "content": '你好'}]
            title = ''
            print()
        case 'list':
            del messages[len(messages) - 1]
            read_ini()
            if 'history' not in ini or not ini['history']:
                print("\033[31m无数据！\033[0m")
            else:
                for index, messages_dictionary in enumerate(ini['history']):
                    print("\033[33m" + str(index) + '   ' + messages_dictionary['title'] + "\033[0m")
                print("\033[33m-1   返回\033[0m")
                while True:
                    num = input("切换编号：")
                    if num == '-1':
                        break
                    else:
                        try:
                            messages = ini['history'][int(num)]['messages']
                            title = ini['history'][int(num)]['title']
                            for message in messages:
                                match message['role']:
                                    case 'user':
                                        print(message['content'])
                                    case 'assistant':
                                        print("\033[36m" + message['content'] + "\033[0m")
                            break
                        except:
                            print("\033[31m无效编号!\033[0m")
            messages.append({"role": "user", "content": input()})
            continue
        case 'delete':
            del messages[len(messages) - 1]
            if title == '':
                print("\033[31m当前会话非已保存！\033[0m")
                messages.append({"role": "user", "content": input()})
            else:
                read_ini()
                if 'history' not in ini or not ini['history']:
                    print("\033[31m数据丢失！\033[0m")
                else:
                    for index, messages_dictionary in enumerate(ini['history']):
                        if messages_dictionary['title'] == title:
                            del ini['history'][index]
                            try:
                                write_ini()
                                messages = [{"role": "user", "content": 'clear'}]
                            except:
                                print("\033[31m删除失败！\033[0m")
                            break
            continue
        case 'save':
            del messages[len(messages) - 1]
            read_ini()
            if 'history' not in ini:
                ini = ini_model
            data = {'title': input("会话标题："), 'messages': messages}
            for index, messages_dictionary in enumerate(ini['history']):
                print("\033[33m" + str(index) + '   ' + messages_dictionary['title'] + "\033[0m")
            num = input("替换键入编号，新建键入任意其他内容：")
            try:
                ini['history'][int(num)] = data
            except:
                ini['history'].append(data)
            try:
                write_ini()
                messages = [{"role": "user", "content": 'clear'}]
            except:
                print("\033[31m保存失败！\033[0m")
                messages.append({"role": "user", "content": input()})
            continue
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print("\033[36m" + completion.choices[0].message.content + "\033[0m")
    messages.append(completion.choices[0].message)
    messages.append({"role": "user", "content": input()})
