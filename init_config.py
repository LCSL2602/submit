import requests as requests
import get_file_class

from envs import env
constants = env.env()


def run_file(file):
    index = 1
    while file.max_row > 0:
        cell_host = f'B{index}'
        cell_ip = f'D{index}'
        id_device = get_id(file[cell_ip].value)
        if id_device != 0:
            init_confi(id_device, "5ffc8910ffaf1d68559f10b6")
            index = index + 1
        else:
            break


def init_confi(_id, config_id):
    url = f"{constants.URL_BASE}{constants.INIT_CONFIG}{_id}"
    print(url)
    parameters = {
        "use_specific": False,
        "idconfig_parameters": config_id,
        "status": "notinit"
    }
    try:
        response = requests.post(url=url, json=parameters, headers={"x-api": constants.RETRIEVER_TOKEN})
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    print(response.text)


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


def main():
    upload_file = get_file_class.get_sheet(constants.FILE)
    run_file(upload_file)


if __name__ == '__main__':
    main()
