from distutils.command.upload import upload
import requests as requests
import openpyxl
from pathlib import Path
import json


from envs import env

constants = env.env()


def get_sheet():
    upload_file = constants.FILE
    xls_file = Path('./', upload_file)
    wb_obj = openpyxl.load_workbook(xls_file)
    sheet = wb_obj.active
    return sheet
    

def run_sheet(sheet):
    if sheet.max_row > 0:
        indice = 1
        while indice <= sheet.max_row:
            cell_name_B = 'B' + str(indice)
            cell_name_D = 'D' + str(indice)
            if confirm_device(sheet[cell_name_B].value):
                print(f"Device {sheet[cell_name_B].value} already exist")
            else :
                create_device(sheet, cell_name_B, cell_name_D)    
            
            indice = indice + 1


def confirm_device(name):
    url = f"{constants.URL_BASE}{constants.GET_DEVICE}{name}"
    response = requests.get(url=url, headers={"x-api": constants.DEVICE_TOKEN}, verify=False)
    try: 
        device = response.json()
    except: 
        pass

    if len(device) > 0:
        return True
    else:
        return False       


def create_device(sheet, hostname, ip):
    data_device = {
        "host" : sheet[hostname].value,
        "id_confparameters": "5ffc8910ffaf1d68559f10b6", # Default config
        "ip": sheet[ip].value,
        "model":"cisco",
        "name" : sheet[hostname].value,
        "password_template" : 1 ,
        "status" : "active",
        "type" : "cisco_ios",
        "vendor" : "Cisco",
        "tag": '{}'
    }

    url = f"{constants.URL_BASE}{constants.CREATE_DEVICE}"
    #data_device = json.dumps(data_device, indent= 4)

    response = requests.post(url=url, json= data_device, headers={"x-api": constants.DEVICE_TOKEN}, verify=False)
    try:
        res = response.json()
        print(res)
    except:
        print("Fail to create")


def main():
    sheet = get_sheet()
    run_sheet(sheet)


if __name__ == '__main__':
    main()


# device_family: "null"
# device_type: "null"
# guid: "null"
# host: "MUMEXCHL4005"
# id: 33841
# ip: "10.221.16.186"
# iptransport: "10.221.16.186"
# model: "cisco_ios"
# name: "MUMEXCHL4005"
# origin: null
# serial_number: "null"
# site: {name: "EULOGIO PARRA (HGDL0108)", latitude: "20.687", longitude: "-103.368",…}
# site_id: 912
# status: "active"
# tag: "{}"
# type: "cisco_ios"
# vendor: "Cisco"


# host: "MUMEXPAZ4041"
# id_confparameters: "5ffc8910ffaf1d68559f10b6"
# ip: "10.221.16.187"
# model: "cisco"
# name: "MUMEXPAZ4041"
# password_template: 1
# status: "active"
# tag: "{}"
# type: "cisco_nxos"
# vendor: "Cisco"

