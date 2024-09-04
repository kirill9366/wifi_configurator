# Класс для генерации мощности сигнала

import random

class SignalGenerator:
    def generate_signal(self):
        return random.randint(2, 5)

    def update_signal_strength(self):
        # Метод, который может быть реализован для обновления сигнала в реальном времени
        pass
