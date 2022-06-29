import requests

import get_file_class
import init_config
import submit_devices
import sys
from envs import env

constants = env.env()


def run_file(file):
    if file.max_row > 0:
        index = 2

        while index < file.max_row:
            cell_hostname = f'B{index}'
            cell_ip = f'A{index}'
            if submit_devices.confirm_device(file[cell_ip].value):
                print(f"The device {file[cell_hostname].value} already exist")
            else:
                try:
                    id_device = submit_devices.create_device(sheet=file, hostname=cell_hostname, ip=cell_ip)
                    if id_device != 0:
                        # init_config.init_confi(_id=id_device, config_id="5ffc8910ffaf1d68559f10b6")
                        print(f"Create and init device:{id_device}-{file[cell_hostname].value}-{file[cell_ip].value}")
                    else:
                        print(f"Device:{file[cell_hostname]} don't init")
                except requests.exceptions.HTTPError as err:
                    raise SystemExit(err)
            index += 1


def main():
    file = get_file_class.get_sheet(sys.argv[1])
    run_file(file)


if __name__ == "__main__":
    main()
