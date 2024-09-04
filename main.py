# wifi_configurator/main.py

from wifi_configurator.cli import CLI
from wifi_configurator.configurator import Configurator
from wifi_configurator.wifi_manager import WiFiManager
from wifi_configurator.signal_generator import SignalGenerator

HOST = '192.168.1.1'
USERNAME = 'root'
PASSWORD = 'admin'


def main():
    cli = CLI()
    args = cli.parse_arguments()

    configurator = Configurator(config_file=args.file)
    config = configurator.load_config()

    wifi_manager = WiFiManager(
        config,
        host=HOST,
        username=USERNAME,
        password=PASSWORD,
    )
    signal_generator = SignalGenerator()

    if args.action == 'new':
        mac_list, names, frequencies = cli.get_new_points_input()
        for mac, name, frequency in zip(mac_list, names, frequencies):
            power = signal_generator.generate_signal()
            wifi_manager.add_new_point(mac, name, frequency, power)
            wifi_manager.create_wifi(ssid=name, macaddr=mac, frequency=frequency)
        wifi_manager.apply_encryption()
    elif args.action == 'load':
        wifi_manager.load_existing_points()

    configurator.save_config(wifi_manager.get_config_data())

    if args.update_signal:
        wifi_manager.update_signal_strength(iface=args.iface)

    wifi_manager.close()


if __name__ == "__main__":
    main()
