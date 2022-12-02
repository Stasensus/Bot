from server import Bot

if __name__ == '__main__':
    TOKEN = 'vk1.a.nxwYoT0jJ_yZA2EWa_JO5K_On6IkShsY71FkxuenlLNtqNime-lYvXs7gMleTIBKMdS31fj1tFC7KdT01_8WS7h8kHYDkBazzbcUtOTu52kI3jbPwsV5BmE7j6mF3a1fwc_ehAelhJVrgx1VcFxqoc_jbg1ZTgxlCfbU-dIUYqIzUj4pfAposuRnfq-brSQI7zrUVdty4R9JNXSE_MgTHg'
    server = Bot(TOKEN)
    COMMANDS = {
        'начать': server.greeting,
        'начать игру': server.get_command_amount,
        'правила': server.rules,
        'две': server.set_command_amount,
        'три': server.set_command_amount,
        'четыре': server.set_command_amount,
        'пять': server.set_command_amount,
        '25': server.set_victory_score,
        '50': server.set_victory_score,
        '100': server.set_victory_score,
        'да': server.set_penalty,
        'нет': server.set_penalty,
        '60': server.set_explain_time,
        '90': server.set_explain_time,
        '120': server.set_explain_time,
        'простой': server.create_dict,
        'средний': server.create_dict,
        'сложный': server.create_dict,
        'английский': server.create_dict,
        'начать объяснение!': server.TheGame.start_explanation,
        'следующее слово': server.TheGame.demonstrate_word,
        'пропустить слово': server.TheGame.demonstrate_word,
        'сыграть ещё раз': server.greeting,
        '0': server.TheGame.finish_explanation_2,
        '1': server.TheGame.finish_explanation_2,
        '2': server.TheGame.finish_explanation_2,
        '3': server.TheGame.finish_explanation_2,
        '4': server.TheGame.finish_explanation_2,
        '5': server.TheGame.finish_explanation_2,
        '6': server.TheGame.finish_explanation_2,
        '7': server.TheGame.finish_explanation_2,
        '8': server.TheGame.finish_explanation_2,
        '9': server.TheGame.finish_explanation_2,
        '10': server.TheGame.finish_explanation_2,
         'command': 'start'

    }
    server.start(COMMANDS)


