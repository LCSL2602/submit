from distutils.command.upload import upload
import requests as requests
import openpyxl
from pathlib import Path
import json


from envs import env

constants = env.env()


def getSheet():
    upload_file = constants.getFile()
    xls_file = Path('./',upload_file)
    wb_obj = openpyxl.load_workbook(xls_file)
    sheet = wb_obj.active
    return sheet
    

def run_sheet(sheet):
    if(sheet.max_row > 0):
        indice = 1
        while indice <= sheet.max_row:
            cell_name_B = 'B' + str(indice)

            if confirm_device(sheet[cell_name_B].value) :
                print("Device alredy exist")
            else :
                create_device(sheet)    
            
            indice = indice + 1


def confirm_device(name):
    url = f"{constants.URL_BASE}{constants.GET_DEVICE}{name}"
    response = requests.get(url = url, headers={"x-api":constants.DEVICE_TOKEN},verify= False)
    try: 
        device = response.json()
    except: 
        pass

    if len(device) > 0:
        return True
    else:
        return False       
    
def create_device(sheet):
    print(sheet)

def main():
    sheet = getSheet()
    run_sheet(sheet)

if __name__ == '__main__':
    main()
