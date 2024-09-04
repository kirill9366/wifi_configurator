# Класс для обработки командной строки

import argparse

from wifi_configurator.utils import generate_random_name


class CLI:
    @property
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='WiFi Configurator')
        parser.add_argument('--file', type=str, default='config.txt', help='Path to the configuration file')
        parser.add_argument('action', choices=['new', 'load'], help='Action to perform: create new points or load existing')
        return parser.parse_args()

    def get_new_points_input(self):
        mac_list = input("Введите MAC адреса (через запятую): ").split(',')
        names = input("Введите имена (через запятую или '1' для рандомных имен): ").split(',')
        if '1' in names:
            names = [generate_random_name() if name == '1' else name for name in names]
        frequencies = input("Введите частоу (через запятую, 1 для 2.4 GHz, 2 для 5 GHz): ").split(',')
        return mac_list, names, frequencies
