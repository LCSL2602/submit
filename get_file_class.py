import openpyxl
from pathlib import Path
import sys


def get_sheet(upload_file, sheet_name='none'):
    xls_file = Path(f'./{upload_file}')
    wb_obj = openpyxl.load_workbook(xls_file)
    if sheet_name == 'none':
        sheet = wb_obj.active
    else:
        sheet = wb_obj[sheet_name]
    return sheet


if __name__ == '__main__':
    file = get_sheet(sys.argv[1], 'Equipos Huawei')
    print(file)
