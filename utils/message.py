class Message:
    def __init__(self, **kwargs):
        self.title = 'Error'
        self.message = None

        if kwargs.get('title'):
            self.title = kwargs.get('title')
        if kwargs.get('message'):
            self.message = kwargs.get('message')

    def exception_console(self):
        template = ""
        template += "===========================================================\n"
        template += "=             Chuong trinh shop yen - Console             =\n"
        template += "===========================================================\n"
        template += "{}\n"
        template += "{}\n"

        print(template.format(self.title, self.message))
