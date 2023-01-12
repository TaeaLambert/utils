from enum import Enum


class googleDriveFileExportType(Enum):
    PDF = "pdf"
    CSV = "csv"
    XLS = "xls"
    XLSX = "xlsx"
    TSV = "tsv"
    ODS = "ods"
    ZIP = "zip"

    TXT = "txt"
    DOCX = "docx"


class googleDriveFileType(Enum):
    XLSX = "spreadsheets"
    DOCX = "document"
