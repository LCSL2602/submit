import requests as requests

from envs import env
import get_file_class
import create_excel_class

constants = env.env()


def run(file):
    index = 1
    create_excel_class.create_file()
    while file.max_row > 0:
        cell_host = f'B{index}'
        cell_ip = f'D{index}'
        id_device = get_id(file[cell_ip].value)
        print(f"id:{id_device}", f"index:{index}")
        if id_device != 0:
            confirm_config_retriever(id_device, file[cell_ip].value, file[cell_host].value)
            index = index + 1
        else:
            break


def get_id(ip):
    if ip is not None:
        data = {
            "name": ip,
            "tags": []
        }

        url = f"{constants.URL_BASE}{constants.VERIFY_DEVICE}"
        response = requests.post(url=url, json=data, headers={"x-api": constants.DEVICE_TOKEN}, verify=False)
        try:
            device = response.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        if len(device["data"]) > 0:
            return device["data"][0]["id"]
        else:
            return 0
    else:
        return 0


def confirm_config_retriever(id_device, ip, hostname):
    if id_device != 0:
        url = f"{constants.URL_BASE}{constants.CONFIG_RETRIEVER}{id_device}"
        try:
            response = requests.get(url=url, headers={"x-api": constants.RETRIEVER_TOKEN}, verify=False)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        print(response.text)
        message = ""
        err = ""
        if response.status_code == 404 or 500:
            message = f"The configuration for device:{ip} does not exist"
            err = response.json()['error']

        if response.status_code == 200 and response.json()['status'] == "notok":
            message = f"The configuration for device:{ip} has some issues"
            err = response.json()['error']

        if response.status_code == 200 and response.json()['configuration'] != {}:
            message = f"Correct"
            err = None

        config = (hostname, ip, message, err)
        print(config)
        create_excel_class.modify_file("Config_retriever_by_devices.xlsx", config)


def main():
    upload_file = get_file_class.get_sheet(constants.FILE)
    run(upload_file)


if __name__ == '__main__':
    main()
