# wifi_configurator/main.py

from wifi_configurator.cli import CLI
from wifi_configurator.configurator import Configurator
from wifi_configurator.wifi_manager import WiFiManager
from wifi_configurator.signal_generator import SignalGenerator

HOST = '192.168.1.1'
USERNAME = 'root'
PASSWORD = 'root'


def main():
    with open("config.txt", "w") as file:
        file.write("")
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
    wifi_manager.remove_wifis()
    signal_generator = SignalGenerator()
    if args.file == "config.txt":
        mac_list, names, frequencies = cli.get_new_points_input()
        for mac, name, frequency in zip(mac_list, names, frequencies):
            power = signal_generator.generate_signal()
            wifi_manager.add_new_point(mac, name, frequency, power)
            wifi_manager.create_wifi(ssid=name, macaddr=mac, frequency='2.4GHz' if frequency == "1" else "5GHz")
        wifi_manager.apply_encryption()
        configurator.save_config(wifi_manager.get_config_data())
    else:
        wifi_manager.load_existing_points()
        print(wifi_manager.points.items())
        for key, point in wifi_manager.points.items():
            wifi_manager.create_wifi(
                ssid=point["name"],
                macaddr=key.split("_")[1], 
                frequency='2.4GHz' if point["frequency"] == "1" else "5GHz",
            )
    
    wifi_manager.close()


if __name__ == "__main__":
    main()
