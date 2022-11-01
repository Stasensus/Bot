import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

class BaseBot:
    def __init__(self, token: str):
        self._vk = vk_api.VkApi(token=token)
        self.__long_poll = VkLongPoll(self._vk)

    def start(self, commands):
        self.__commands = commands
        print('Игровой бот запущен. Чтобы начать, напишите "Начать".')
        for event in self.__long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self._command_starter(event)

    def _command_starter(self, event):
        msg = event.text
        if self.__commands.get(msg.lower()):
            self.__commands[msg.lower()](event)
        else:
            self.command_name(event)

    def _send_msg(self, id: int, message: str):
        data = {
            'user_id': id,
            'message': message,
            'random_id': random.randint(1, 1000)
        }
        self._vk.method('messages.send', data)

    def command_name(self, event):
        pass
    
class Bot(BaseBot):
    users = {}

    def greeting(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Привет, ты можешь прочитать правила или начать игру. Напиши: "Правила" или "Игра".')
    

    def rules(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Правила игры таковы:... Если ты готов играть, напиши: "Игра".')
        
    def prestart(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Сколько команд будет играть? Напиши цифру от 2 до 4.')

    def command_amount(self, event):
        user_id = event.user_id
        if 1 < int(event.text) < 5:
            self.users[user_id] = {
                'command_amount': int(event.text),
                'command_name': [],
            }
            self._send_msg(user_id,
                          'Введите название команды №1: ')
        else:
            self._send_msg(user_id,
                           'Количество команд от 2 до 4. Напиши цифру от 2 до 4.')
        
    def command_name(self, event):
        user_id = event.user_id
        if self.users.get(user_id):
            if len(self.users.get(user_id)['command_name']) != self.users.get(user_id)['command_amount']:
                self.users[user_id]['command_name'].append(event.text)
                if len(self.users.get(user_id)['command_name']) + 1 <= self.users.get(user_id)['command_amount']:
                    self._send_msg(user_id,
                                f"Введите название команды №{len(self.users.get(user_id)['command_name']) + 1}: ")
                else:
                    self.victory_score(event)

    def victory_score(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       "До скольки очков играем для победы? Напиши: 25, 50 или 100.")

    def set_victory_score(self, event):
        user_id = event.user_id
        if int(event.text) in [25, 50, 100]:
            self.users[user_id]['score'] = int(event.text)
            print(self.users)
            self.penalty(event)
        else:
            self._send_msg(user_id,
                           "Напиши: 25, 50 или 100.")
            self.set_victory_score(event)

    def penalty(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Отнимать ли очки за пропуск слова? Напиши: "да" или "нет".')

    def set_penalty(self, event):
        user_id = event.user_id
        if event.text.lower() == 'да':
            self.users[user_id]['penalty'] = True
        elif event.text.lower() == 'нет':
            self.users[user_id]['penalty'] = False
        else:
            self._send_msg(user_id, "Ответ не распознан")
            self.set_penalty(event)
        print(self.users)
pass


