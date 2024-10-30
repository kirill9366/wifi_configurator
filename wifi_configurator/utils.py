# Вспомогательные функции (например, генерация случайных имен)

import random
import string

def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
