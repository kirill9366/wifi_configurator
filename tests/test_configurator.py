# Тесты для конфигуратора

import pytest
from wifi_configurator.configurator import Configurator


def test_load_config(tmp_path):
    config_file = tmp_path / "config.txt"
    config_file.write_text("point_1=MAC1;name1;2.4GHz\n")
    
    configurator = Configurator(config_file)
    config = configurator.load_config()
    
    assert config["point_1"] == "MAC1;name1;2.4GHz"


def test_load_empty_config(tmp_path):
    config_file = tmp_path / "config.txt"
    config_file.write_text("")

    configurator = Configurator(config_file)
    config = configurator.load_config()
    assert config == {}


def test_save_config(tmp_path):
    config_file = tmp_path / "config.txt"
    configurator = Configurator(config_file)

    config_data = {"point_1": "MAC1;name1;2.4GHz"}
    configurator.save_config(config_data)
    
    saved_data = config_file.read_text()
    assert "point_1=MAC1;name1;2.4GHz" in saved_data
