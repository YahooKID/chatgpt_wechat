import openai


class chatGpt:
    openai.api_key = "" #更换为你的openai apikey
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        if len(self.messages) >= 16:
            self.messages.pop(0)
            self.messages.pop(0)
        self.messages.append({'role': 'user', 'content': message})
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=self.messages
            )
        message = response["choices"][0]["message"]
        print("\n**{} : {}".format(message["role"], message["content"]))
        self.messages.append(message)
        return "[{}/8] {}".format(int(len(self.messages)/2), message["content"].replace('\n',''))

    def cleanlist(self):
        self.messages = []
