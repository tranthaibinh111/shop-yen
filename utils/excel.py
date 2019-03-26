import environ
import pandas as pd
from pandas import ExcelFile
from utils.message import Message


class ShopYenExcel:
    def __init__(self, path_to_file: str):
        self.columns = environ.Env().list('COLUMNS', cast=str, default=list())
        self.file = ExcelFile(path_to_file)

    def check_format_excel(self, file: ExcelFile) -> bool:
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
        for sheet in file.sheet_names:
            for column in pd.read_excel(file, sheet).columns:
                if column in self.columns:
                    continue
                else:
                    title = "(Error) Shop Yen - Import Excel"
                    message = "File: {}\n".format(file.io)
                    message += "Sheet: {}\n".format(sheet)
                    message += "Column: {} don't exist in {}".format(column, self.columns)
                    Message(title, message).exception_console()
                    return False
        return True

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
        if not self.file:
            return list()

        if not self.check_format_excel(self.file):
            return list()

        customers = list()
        df = pd.read_excel(self.file)
        for sheet in self.file.sheet_names:
            customer = dict()
            columns = pd.read_excel(self.file, sheet).columns
            for index, row in df.iterrows():
                for column in columns:
                    customer.update({column: row[column]})
                customers.append(customer)

        return customers
