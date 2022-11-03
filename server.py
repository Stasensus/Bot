import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

FILE = r'C:\Users\USER\PycharmProjects\Bot\dict1.txt'
class BaseBot:
    def __init__(self, token: str):
        self._vk = vk_api.VkApi(token=token)
        self.__long_poll = VkLongPoll(self._vk)
        self.keyboard = KeyboardMixin()

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

    def _send_msg(self, id: int, message: str, keyboard: VkKeyboard = None):
        if not keyboard:
            data = {
                'user_id': id,
                'message': message,
                'random_id': random.randint(1, 1000)
            }
            self._vk.method('messages.send', data)
        elif keyboard:
            data = {
                'user_id': id,
                'message': message,
                'random_id': random.randint(1, 1000),
                'keyboard': keyboard.get_keyboard()
            }
            self._vk.method('messages.send', data)

    def command_name(self, event):
        pass
    
class Bot(BaseBot):
    users = {}

    def greeting(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Привет, ты можешь прочитать правила или начать игру. Напиши: "Правила" или "Игра".',
                       keyboard=self.keyboard.get_standart_keyboard())
    

    def rules(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Правила игры таковы:... Если ты готов играть, напиши: "Игра".')
        
    def prestart(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='2', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='3', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='4', color=VkKeyboardColor.POSITIVE)
        self._send_msg(user_id,
                       'Сколько команд будет играть? Напиши цифру от 2 до 4.', keyboard)

    def command_amount(self, event):
        user_id = event.user_id
        if 1 < int(event.text) < 5:
            self.users[user_id] = {
                'command_amount': int(event.text),
                'command_name': [],
            }
            self._send_msg(user_id,
                          'Введите название команды №1: ',)
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
        else:
            self._send_msg(user_id, 'Ваш ответ не распознан')

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
            self.explain_time(event)
        elif event.text.lower() == 'нет':
            self.users[user_id]['penalty'] = False
            self.explain_time(event)
        print(self.users)

    def explain_time(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Сколько времени даём на объяснение? Напиши: "60", "90" или "120" секунд.')
    def set_explain_time(self, event):
        user_id = event.user_id
        if event.text.lower() == '60':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        elif event.text.lower() == '90':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        elif event.text.lower() == '120':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        print(self.users)

    def choose_dict(self, event):
        user_id = event.user_id
        self._send_msg(user_id,
                       'Выбери словарь для игры. Напиши: "просто", "средне" или "сложно".')


    def create_dict(self, event):
        user_id = event.user_id
        if event.text.lower() == 'просто':
            self.users = Dictionaries(event, self.users).create_easy_dict()


        elif event.text.lower() == 'средне':
            with open(FILE, encoding='utf-8') as f:
                moderate = f.readlines()
                moderate = [line.rstrip('\n') for line in moderate]
                self.users[user_id]['dictionary'] = moderate

        elif event.text.lower() == 'сложно':
            with open(FILE, encoding='utf-8') as f:
                hard = f.readlines()
                hard = [line.rstrip('\n') for line in hard]
                self.users[user_id]['dictionary'] = hard

        print(self.users)



class Dictionaries():
    def __init__(self, event, users):
        self.user_id = event.user_id
        self.users = users
    def create_easy_dict(self):
        with open(FILE, encoding='utf-8') as f:
            easy = f.readlines()
            easy = [line.rstrip('\n') for line in easy]
            self.users[self.user_id]['dictionary'] = easy
            return self.users

class KeyboardMixin(VkKeyboard):
    """
    Working with the VK keyboard, implemented methods for
    getting, hiding the keyboard and showing auxiliary commands
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hide_keyboard(self, label: str = '📌️Вернуть клавиатуру'):
        keyboard = VkKeyboard()
        keyboard.add_button(label=label, color=VkKeyboardColor.POSITIVE)
        return keyboard

    def get_standart_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Правила', color=VkKeyboardColor.PRIMARY)
        return keyboard

    def get_help(self):
        keyboard = VkKeyboard()
        keyboard.add_button(label='🔎Помощь', color=VkKeyboardColor.POSITIVE)
        return keyboard
