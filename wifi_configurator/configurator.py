# Класс для работы с конфигурацией (чтение/запись)

import os

class Configurator:
    def __init__(self, config_file='config.txt'):
        self.config_file = config_file

    def load_config(self):
        if not os.path.exists(self.config_file):
            return {}
        with open(self.config_file, 'r') as file:
            data = file.readlines()
        if data:
            return {line.split('=')[0].strip(): line.split('=')[1].strip() for line in data}
        else:
            return {}

    def save_config(self, config_data):
        with open(self.config_file, 'w') as file:
            for key, value in config_data.items():
                file.write(f'{key}={value}\n')