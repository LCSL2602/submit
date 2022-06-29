import requests as requests
import get_file_class

from envs import env

constants = env.env()


def run_sheet(sheet):
    repeat_devices = 0
    created_devices = 0

    if sheet.max_row > 0:
        indice = 1
        while indice <= sheet.max_row:
            cell_name_B = 'B' + str(indice)
            cell_name_D = 'A' + str(indice)
            if confirm_device(sheet[cell_name_D].value):
                print(f"Device {sheet[cell_name_B].value} already exist")
                repeat_devices = repeat_devices + 1
            else:
                create_device(sheet, cell_name_B, cell_name_D)
                created_devices = created_devices + 1

            if sheet[cell_name_D].value is None:
                break
            indice = indice + 1

        print(f"Process finish => devices created: {created_devices} | devices repeats: {repeat_devices} ")


def confirm_device(ip) -> bool:
    data = {
        "name": ip,
        "tags": []
    }
    url = f"{constants.URL_BASE}{constants.VERIFY_DEVICE}"
    try:
        response = requests.post(url=url, json=data, headers={"x-api": constants.DEVICE_TOKEN}, verify=False)
        device = response.json()
        if len(device["data"]) > 0:
            return True
        else:
            return False
    except requests.exceptions.HTTPError as err:
        return False


def create_device(sheet, hostname, ip) -> int:
    data_device = {
        "host": sheet[hostname].value,
        "id_confparameters": "5ffc8910ffaf1d68559f10b6",  # Default config
        "ip": sheet[ip].value,
        "model": "cisco",
        "name": sheet[hostname].value,
        "password_template": 2,
        "status": "active",
        "type": "cisco_ios",
        "vendor": "Cisco",
        "tag": '{}'
    }

    url = f"{constants.URL_BASE}{constants.CREATE_DEVICE}"

    response = requests.post(url=url, json=data_device, headers={"x-api": constants.DEVICE_TOKEN}, verify=False)
    try:
        res = response.json()
        print(res, sheet[hostname].value)
        return res
    except:
        print("Fail to create")
        return 0


def main():
    sheet = get_file_class.get_sheet(constants.FILE)
    run_sheet(sheet)


if __name__ == '__main__':
    main()
