# Класс для управления точками доступа (создание, настройка)
import re
import time

import paramiko


class WiFiManager:
    def __init__(self, config, host, username, password):
        self.config = config
        self.points = {}
        self.host = host
        self.username = username
        self.password = password
        self.ssh = self._connect_ssh()

    def _connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.host,
            username=self.username,
            password=self.password,
            disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
        )
        return ssh

    def add_new_point(self, mac, name, frequency, power):
        self.points[mac] = {
            'name': name,
            'frequency': frequency,
            'power': power
        }

    def load_existing_points(self):
        self.points = {key: value for key, value in self.config.items() if key.startswith('point_')}

    def apply_encryption(self):
        for point in self.points.values():
            point['encryption'] = 'WPA2'

    def get_config_data(self):
        return {f'point_{key}': value for key, value in self.points.items()}

    def _run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error:
            print(f"Error executing {command}: {error}")
        return stdout.read().decode(), stderr.read().decode()

    def remove_wifis(self):
        delete_command = "for iface in $(uci show wireless | grep '.device=' | cut -d. -f2); do uci delete wireless.$iface; done"
        self._run_command(delete_command)

    def create_wifi(self, ssid, encryption='psk2', key='password', network='lan', mode='ap', macaddr=None, frequency='2.4GHz'):
        # Добавляем новую WiFi точку доступа
        add_command = f"uci add wireless wifi-iface"
        self._run_command(add_command)

        # Задаем параметры точки доступа
        set_commands = [
            f"uci set wireless.@wifi-iface[-1].device='radio0'",
            f"uci set wireless.@wifi-iface[-1].mode='{mode}'",
            f"uci set wireless.@wifi-iface[-1].ssid='{ssid}'",
            f"uci set wireless.@wifi-iface[-1].network='{network}'",
            f"uci set wireless.@wifi-iface[-1].encryption='{encryption}'",
            f"uci set wireless.@wifi-iface[-1].key='{key}'",
        ]

        if macaddr:
            set_commands.append(f"uci set wireless.@wifi-iface[-1].macaddr='{macaddr}'")

        if frequency == '5GHz':
            set_commands[0] = f"uci set wireless.@wifi-iface[-1].device='radio1'"

        for cmd in set_commands:
            self._run_command(cmd)

        # Сохраняем и перезагружаем WiFi
        self._run_command("uci commit wireless")
        self._run_command("wifi")

    def close(self):
        self.ssh.close()

    def get_signal_strength(self, iface):
        """Получает текущий уровень сигнала dBm для указанного интерфейса."""
        command = f"iwinfo {iface} info | grep 'Signal:'"
        output, _ = self._run_command(command)
        match = re.search(r'Signal: (-\d+) dBm', output)
        if match:
            return int(match.group(1))
        return None

    def update_signal_strength(self, iface):
        """Постоянно обновляет мощность сигнала для указанного интерфейса."""
        while True:
            signal_strength = self.get_signal_strength(iface)
            if signal_strength is not None:
                print(f"Current dBm for {iface}: {signal_strength} dBm")
                # Здесь можно добавить логику для изменения конфигурации в зависимости от dBm
                self._update_wifi_signal(iface, signal_strength)
            time.sleep(10)  # Обновляем каждые 10 секунд

    def _update_wifi_signal(self, iface, signal_strength):
        """Обновляет конфигурацию на основе нового значения dBm."""
        # Пример: Установка мощности сигнала в UCI
        set_command = f"uci set wireless.@wifi-iface[-1].txpower='{signal_strength}'"
        self._run_command(set_command)
        self._run_command("uci commit wireless")
        self._run_command("wifi")
