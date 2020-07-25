import requests 
from bottle import Bottle, response, request as bottle_request
from bs4 import BeautifulSoup as bs

class BotHandlerMixin:
    BOT_URL = None

    def get_chat_id(self, data):
        chat_id = data['message']['chat']['id']

        return chat_id
    
    def get_message(self, data):
        message_id = data['message']['text']

        return message_id
   
    def get_firstName(self, data):
        first_name = data['message']['from']['first_name']

        return first_name

    def send_message(self, prepared_data):

        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)

    def getName(self,text):
        stringtSize = len(text)
        name = text[15:stringtSize]
        return name

    def getMeaning(self,nome):
        request = requests.get("https://www.dicionariodenomesproprios.com.br/"+nome)
        html = bs(request.text, "html.parser")

        divMeaning = html.find(id="significado")
        meanigP = divMeaning.find_all("p")
        Meaning  = ""
        for x in meanigP:
            Meaning  += x.text+"\n\n"
        return Meaning

class TelegramBot(BotHandlerMixin, Bottle):
    BOT_URL = 'https://api.telegram.org/bot<token>/'

    def __init__(self,*args,**kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")
    
    def change_text_message(self, text):
        if(text.lower() == 'ola'):
            text = 'Olá'
        elif(text.lower().index('significado de ') != -1):
            name = self.getName(text)
            text = self.getMeaning(name)
        else:
            text = text[::-1]
        return text

    def prepare_data_for_answer(self,data):
        message = self.get_message(data)
        if(message.lower() == 'significado do meu nome'):
            first_name = self.get_firstName(data)
            answer = self.getMeaning(first_name)
        else:
            answer = self.change_text_message(message)
        chat_id = self.get_chat_id(data)
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }

        return json_data
    
    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response

if __name__ == '__main__':
    app = TelegramBot()
    app.run(host='localhost', port=8080)