# Тесты для вспомогательных функций

import pytest
from wifi_configurator.utils import generate_random_name

def test_generate_random_name():
    name = generate_random_name()
    
    assert len(name) == 8
    assert name.islower()
    assert name.isalpha()
