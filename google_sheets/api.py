# import os.path
#
# import gspread
# from google.oauth2.service_account import Credentials
#
#
# CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")
#
#
#
# def get_client():
#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive.file",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scopes)
#
#     client = gspread.authorize(credentials)
#
#     return client
#
#
# def write_to_sheet(range_name, data):
#     client = get_client()
#
#     spreasheet = client.open("drfmaster")
#
#     sheet = spreasheet.sheet1
#
#     sheet.update(range_name, data)
#
#
# def read_from_sheet(range_name):
#     client = get_client()
#
#     spreasheet = client.open("drfmaster")
#
#     sheet = spreasheet.sheet1
#
#     values = sheet.get(range_name)
#
#     return values
#
# if __name__ == '__main__':
#     write_to_sheet('A1:B2', [['1', '2']])
#     # print(read_from_sheet('A1:B2'))

import os.path
import gspread
from google.oauth2.service_account import Credentials

# Путь к файлу с учетными данными
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

# Получение клиента для работы с Google Sheets
def get_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scopes)
    client = gspread.authorize(credentials)
    return client

# Запись данных в Google Sheets
def write_to_sheet(range_name, data):
    client = get_client()
    spreadsheet = client.open("drfmaster")
    sheet = spreadsheet.sheet1
    sheet.update(range_name, data)

# Чтение данных из Google Sheets
def read_from_sheet(range_name):
    client = get_client()
    spreadsheet = client.open("drfmaster")
    sheet = spreadsheet.sheet1
    values = sheet.get(range_name)
    return values

if __name__ == '__main__':
    write_to_sheet('A1:B2', [['1', '2']])
    # print(read_from_sheet('A1:B2'))
