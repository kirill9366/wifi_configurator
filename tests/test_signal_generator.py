# Тесты для генератора сигнала

import pytest
from wifi_configurator.signal_generator import SignalGenerator

def test_generate_signal():
    generator = SignalGenerator()
    signal = generator.generate_signal()
    
    assert 2 <= signal <= 5
