import pytest
import paramiko
from unittest.mock import patch, MagicMock
from wifi_configurator.wifi_manager import WiFiManager


@pytest.fixture
def wifi_manager():
    with patch.object(WiFiManager, '_connect_ssh', return_value=MagicMock()):
        return WiFiManager({}, host='192.168.1.1', username='root', password='admin')


def test_create_wifi(wifi_manager):
    with patch.object(wifi_manager, '_run_command', return_value=("output", "error")) as mock_run_command:
        wifi_manager.create_wifi(ssid="TestNetwork", key="TestPassword", frequency='2.4GHz')

        # Проверяем вызовы команд UCI
        assert mock_run_command.call_count > 0
        assert "uci set wireless.@wifi-iface[-1]=wifi-iface" in mock_run_command.call_args_list[0][0][0]
        assert "uci set wireless.@wifi-iface[-1].device='radio0'" in mock_run_command.call_args_list[1][0][0]
        assert "uci set wireless.@wifi-iface[-1].ssid='TestNetwork'" in mock_run_command.call_args_list[3][0][0]


def test_get_signal_strength(wifi_manager):
    with patch.object(wifi_manager, '_run_command', return_value=("Signal: -65 dBm", "")) as mock_run_command:
        signal_strength = wifi_manager.get_signal_strength(iface="wlan0")

        # Проверяем, что команда вызвана правильно
        mock_run_command.assert_called_once_with("iwinfo wlan0 info | grep 'Signal:'")
        assert signal_strength == -65


def test_get_signal_strength_no_signal(wifi_manager):
    with patch.object(wifi_manager, '_run_command', return_value=("No signal", "")) as mock_run_command:
        signal_strength = wifi_manager.get_signal_strength(iface="wlan0")

        # Проверяем, что сигнал отсутствует
        assert signal_strength is None


def test_update_signal_strength(wifi_manager):
    with patch.object(wifi_manager, 'get_signal_strength', return_value=-65) as mock_get_signal:
        with patch.object(wifi_manager, '_update_wifi_signal') as mock_update_signal:
            with patch('time.sleep', return_value=None):  # Чтобы избежать реальной задержки в тесте
                wifi_manager.update_signal_strength(iface="wlan0")

                # Проверяем, что сигнал был получен и обновлен
                mock_get_signal.assert_called()
                mock_update_signal.assert_called_with("wlan0", -65)


def test_update_wifi_signal(wifi_manager):
    with patch.object(wifi_manager, '_run_command', return_value=("output", "error")) as mock_run_command:
        wifi_manager._update_wifi_signal(iface="wlan0", signal_strength=-65)

        # Проверяем вызов команды UCI для обновления мощности сигнала
        assert mock_run_command.call_count > 0
        assert "uci set wireless.@wifi-iface[-1].txpower='-65'" in mock_run_command.call_args_list[0][0][0]


def test_close(wifi_manager):
    with patch.object(wifi_manager.ssh, 'close') as mock_close:
        wifi_manager.close()

        # Проверяем, что SSH-соединение было закрыто
        mock_close.assert_called_once()
