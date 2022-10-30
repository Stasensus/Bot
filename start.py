from server import Bot

if __name__ == '__main__':
    TOKEN = 'vk1.a.nxwYoT0jJ_yZA2EWa_JO5K_On6IkShsY71FkxuenlLNtqNime-lYvXs7gMleTIBKMdS31fj1tFC7KdT01_8WS7h8kHYDkBazzbcUtOTu52kI3jbPwsV5BmE7j6mF3a1fwc_ehAelhJVrgx1VcFxqoc_jbg1ZTgxlCfbU-dIUYqIzUj4pfAposuRnfq-brSQI7zrUVdty4R9JNXSE_MgTHg'
    server = Bot(TOKEN)
    COMMANDS = {
        'начать': server.greeting,
        "правила": server.rules,
        'игра': server.prestart,
        '2': server.command_amount,
        '3': server.command_amount,
        '4': server.command_amount,
        '25': server.set_victory_score,
        '50': server.set_victory_score,
        '100': server.set_victory_score,
        'да': server.set_penalty,
        'нет': server.set_penalty,


    }
    server.start(COMMANDS)
