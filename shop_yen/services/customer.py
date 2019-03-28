import os
import re
from django.db.models import Q
from django.utils.dateparse import parse_date
from shop_yen.models import *
from mvc.models import *
from utils.excel import ShopYenExcel


class CustomerService:
    def change_head_mobile(self, mobile) -> str:
        # Check mobile null
        if not isinstance(mobile, str):
            return str()
        # Check head number is 4 character
        head_number = mobile[:4]
        if len(head_number) != 4:
            return str()
        # Change head mobile
        # Viettel
        if head_number == '0162':
            return re.sub(r'^0162', '032', mobile)
        elif head_number == '0163':
            return re.sub(r'^0163', '033', mobile)
        elif head_number == '0164':
            return re.sub(r'^0164', '034', mobile)
        elif head_number == '0165':
            return re.sub(r'^0165', '035', mobile)
        elif head_number == '0166':
            return re.sub(r'^0166', '036', mobile)
        elif head_number == '0167':
            return re.sub(r'^0167', '037', mobile)
        elif head_number == '0168':
            return re.sub(r'^0168', '038', mobile)
        elif head_number == '0169':
            return re.sub(r'^0169', '039', mobile)
        # Mobifone
        elif head_number == '0120':
            return re.sub(r'^0120', '070', mobile)
        elif head_number == '0121':
            return re.sub(r'^0121', '079', mobile)
        elif head_number == '0122':
            return re.sub(r'^0122', '077', mobile)
        elif head_number == '0126':
            return re.sub(r'^0126', '076', mobile)
        elif head_number == '0128':
            return re.sub(r'^0128', '078', mobile)
        # Vinaphone
        elif head_number == '0123':
            return re.sub(r'^0123', '083', mobile)
        elif head_number == '0124':
            return re.sub(r'^0124', '084', mobile)
        elif head_number == '0125':
            return re.sub(r'^0125', '085', mobile)
        elif head_number == '0127':
            return re.sub(r'^0127', '081', mobile)
        elif head_number == '0129':
            return re.sub(r'^0129', '082', mobile)
        # Vietnamobile
        elif head_number == '0186':
            return re.sub(r'^0186', '056', mobile)
        elif head_number == '0188':
            return re.sub(r'^0188', '058', mobile)
        # Gmobile
        elif head_number == '0199':
            return re.sub(r'^0199', '059', mobile)
        else:
            return str()

    def import_excel(self, path_to_file: str):
        """
        Import customer info in Customer Table
        :param path_to_file:
        :return:
        """
        customers = list()
        user = User.objects.filter(pk=1).first()
        for row in ShopYenExcel(path_to_file).read_excel():
            # full name
            full_name = row.get('full_name')
            if not full_name:
                continue
            full_name = full_name.strip().title()
            # first name
            first_name = re.search(r'\w+$', full_name)
            if first_name:
                first_name = first_name.group()
            # last name
            last_name = re.search(r'^\w+', full_name)
            if last_name:
                last_name = last_name.group()
            # birthday
            birthday = row.get('birthday')
            if birthday:
                try:
                    birthday = parse_date(birthday.strip())
                except Exception as ex:
                    birthday = None
            # add contact mobile
            mobile = row.get('mobile')
            if isinstance(mobile, str):
                mobile = mobile.strip()
                customers.append(Customer(
                    first_name=first_name,
                    last_name=last_name,
                    full_name=full_name,
                    birthday=birthday,
                    contact_type=ContactChoice.M.name,
                    contact=mobile,
                    creator=user,
                    writer=user
                ))
                # add contact mobile which have 10 number
                if len(mobile) == 11:
                    mobile = self.change_head_mobile(mobile)
                    if isinstance(mobile, str):
                        customers.append(Customer(
                            first_name=first_name,
                            last_name=last_name,
                            full_name=full_name,
                            birthday=birthday,
                            contact_type=ContactChoice.M.name,
                            contact=mobile,
                            creator=user,
                            writer=user
                        ))
            # add contact email
            email = row.get('email')
            if isinstance(email, str):
                email = email.strip().lower()
                customers.append(Customer(
                    first_name=first_name,
                    last_name=last_name,
                    full_name=full_name,
                    birthday=birthday,
                    contact_type=ContactChoice.E.name,
                    contact=email,
                    creator=user,
                    writer=user
                ))
            # Insert 100 customer
            if len(customers) > 100:
                self.insert_customers(customers)
                customers.clear()
        # Insert when customer exists
        if len(customers) > 0:
            self.insert_customers(customers)
            customers.clear()
        # Remove file target when finished
        if os.path.exists(path_to_file):
            os.remove(path_to_file)

    @staticmethod
    def insert_customers(customers: list):
        # Insert data into Customer
        data = list()
        for customer in customers:
            # Check exist in Customer
            if not Customer.objects.filter(
                    Q(full_name=customer.full_name) &
                    Q(contact_type=customer.contact_type) &
                    Q(contact=customer.contact)
            ).exists():
                data.append(customer)
                print(customer)
            # Insert data if data length == 100
            if len(data) > 100:
                Customer.objects.bulk_create(data)
                data.clear()
        if len(data) > 0:
            Customer.objects.bulk_create(data)
