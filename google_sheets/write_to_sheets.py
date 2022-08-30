import os
import gspread


def google_crential_env_to_file():
    with open(os.getenv("GOOGLE_CONFIG_LOCATION"), "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def write_to_google_sheet(data, workbook, sheet):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(workbook).worksheet(sheet)
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_tasks(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeTaskoutput")
    sh.clear()
    sh.update("A1", data)
    sh.sort((3, "asc"), range="A2:Q50000")
    return "done"


def write_tasks_formatted(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeTaskoutputFormatted")
    sh.clear()
    sh.update("A1", data)
    sh.sort((2, "asc"), range="A2:S50000")
    return "done"


def write_folders(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeFolderoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_projects(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeProjectoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_contacts(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeContactoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_workflow(data):
    gc = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("WrikeStatusoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"
