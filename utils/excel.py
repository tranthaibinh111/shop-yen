import pandas as pd
import numpy as np
from datetime import date
from django.conf import settings
from pandas import ExcelFile
from utils.message import Message


class ShopYenExcel:
    def __init__(self, path_to_file: str):
        self.columns = settings.COLUMN_EXCEL
        self.file = ExcelFile(path_to_file)

    def get_sheets(self):
        return self.file.sheet_names

    def check_format_sheet_excel(self, sheet) -> bool:
        """
        Check Excel Import has struct such as
            Columns:
                name
                birthday
                mobile
                email
        :param file:
        :param sheet:
        :return:
        """
        for column in pd.read_excel(self.file, sheet).columns:
            if column in self.columns:
                continue
            else:
                title = "(Error) Shop Yen - Import Excel"
                message = "File: {}\n".format(self.file.io)
                message += "Sheet: {}\n".format(sheet)
                message += "Column: {} don't exist in {}".format(column, self.columns)
                Message(**{'title': title, 'message': message}).exception_console()
                return False
        return True

    def check_format_excel(self) -> bool:
        """
        Check Excel Import has struct such as
            Columns:
                name
                birthday
                mobile
                email
        :param file: IO Excel
        :return: If ok return True, return False
        """
        for sheet in self.file.sheet_names:
            result = self.check_format_sheet_excel(sheet)
            if not result:
                return False
        return True

    def read_sheet_excel(self, sheet) -> list:
        """
        Read info in excel import
        :return: [
            {
                'full_name': 'Tran Thai Binh',
                'birthday': '1992-09-15',
                'mobile': '0988284955',
                'email': 'tranthaibinh111@gmail.com',
            },
            ...
        ]
        """
        customers = list()
        df = pd.read_excel(self.file, dtype={'full_name': str, 'birthday': date, 'mobile': str, 'email': str})
        columns = pd.read_excel(self.file, sheet).columns
        for index, row in df.iterrows():
            customer = dict()
            for column in columns:
                value = row[column]
                if value is np.nan:
                    value = None
                customer.update({column: value})
            customers.append(customer)

        return customers

    def read_excel(self) -> list:
        """
        Read info in excel import
        :return: [
            {
                'full_name': 'Tran Thai Binh',
                'birthday': '1992-09-15',
                'mobile': '0988284955',
                'email': 'tranthaibinh111@gmail.com',
            },
            ...
        ]
        """
        customers = list()
        for sheet in self.get_sheets():
            customers.append(self.read_sheet_excel(sheet))
        return customers
