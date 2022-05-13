import openpyxl


def create_file(configs):
    wb = openpyxl.Workbook()
    note = wb.active
    note.title = "config"
    note.append(("HOSTNAME", "IP", "CONFIGURATION", "ERR"))

    for config in configs:
        note.append(config)

    wb.save("Config_retriever_by_devices.xlsx")
