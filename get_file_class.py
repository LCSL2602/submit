import openpyxl
from pathlib import Path


def get_sheet(upload_file):
    xls_file = Path('./', upload_file)
    wb_obj = openpyxl.load_workbook(xls_file)
    sheet = wb_obj.active
    return sheet

