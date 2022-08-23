import os
import gspread
from program.utils import config


def google_crential_env_to_file():
    with open(config.CONFIG_LOCATION, "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def write_to_google_sheet(data, workbook, sheet):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(workbook).worksheet(sheet)
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_tasks(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeTaskoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_tasks_formatted(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeTaskoutputFormatted")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_folders(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeFolderoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_projects(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeProjectoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_contacts(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("wrikeContactoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"


def write_workflow(data):
    gc = gspread.service_account(config.CONFIG_LOCATION)
    sh = gc.open(os.getenv("WRIKE_FILE")).worksheet("WrikeStatusoutput")
    sh.clear()
    sh.update("A1", data)
    return "done"
