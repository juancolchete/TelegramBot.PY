import requests  
from bottle import Bottle, response, request as bottle_request

class BotHandlerMixin:  
    BOT_URL = None

    def get_chat_id(self, data):
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']

        return chat_id

    def get_message(self, data):
        """
        Method to extract message id from telegram request.
        """
        message_text = data['message']['text']

        return message_text

    def get_fromName(self, data):
        """
        Method to extract fisrt name from telegram request.
        """
        first_name = data['message']['from']['first_name']

        return first_name

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """       
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):  
    BOT_URL = 'https://api.telegram.org/bot1320348444:AAEbeKsURrNmyDjSRr-cJaV5_vQtCkTEizU/'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def change_text_message(self, text):
        if (text.lower() == 'help'):
            text = 'discord \n youtube \n twitch \n github \n canela \n bom dia \n boa tarde'
        elif (text.lower() == 'bom dia' or text.lower() == 'boa tarde'):
            text = text+' '+first_name
        elif (text.lower() == 'discord'):
            text = 'https://discord.gg/bpcNJxy'
        elif (text.lower() == 'youtube'):
            text = 'https://www.youtube.com/channel/UCITdE7wFDqlNxt_aJ2nSzIQ'
        elif (text.lower() == 'github'):
            text = 'https://github.com/juanudk'
        elif (text.lower() == 'twitch'):
            text = 'https://www.twitch.tv/jovemdev'
        elif (text.lower() == 'canela'):
            text = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fstd1.bebee.com%2Fbc%2F2722499281%2Fus%2F13761466%2F18d060e6%2F0%2F0%2F1%2F1%2F200&imgrefurl=https%3A%2F%2Fwww.bebee.com%2Fbr%2Fbee%2Fguilherme-carvalho-lopes&tbnid=MBOZsOJeRCsO1M&vet=12ahUKEwiIuejxl9LqAhXqK7kGHSohCKQQMygBegUIARCMAQ..i&docid=BaJpNK-FG2TZdM&w=200&h=200&q=guilherme%20carvalho%20lopes&ved=2ahUKEwiIuejxl9LqAhXqK7kGHSohCKQQMygBegUIARCMAQ'
        else:
            text = 'Não entendi, para ver todos os comandos digite: help'
        return text

    def prepare_data_for_answer(self, data):
        global first_name
        first_name = self.get_fromName(data)
        message = self.get_message(data)
        chat_id = self.get_chat_id(data)
        answer = self.change_text_message(message)
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
