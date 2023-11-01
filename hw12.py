from collections import UserDict
from itertools import islice
from datetime import datetime, timedelta
import re
import json


class Field:
    def __init__(self, value):
        self.__privat_value = None
        self.value = value

    @property
    def value(self):
        return self.__privat_value

    @value.setter
    def value(self, value: str):
        if value.isalpha():
            self.__privat_value = value
        else:
            raise Exception("Wrong value")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date_value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Невірний формат дня народження. Використовуйте формат 'YYYY-MM-DD'.")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Невірний формат дня народження. Використовуйте формат 'YYYY-MM-DD'.")
        self._value = new_value

    
class Name(Field):
    def self_name(self, name):
        self.__privat_name = None
        self.name = name
        return str(self.name)

    @property
    def name(self):
        return self.__privat_name

    @name.setter
    def name(self, name: str):
        if name.isalpha():
            self.__privat_name = name
        else:
            raise Exception("Wrong name")


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр.")
        super().__init__(value)
    

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр.")
        self._value = new_value
    

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Невірний формат дня народження. Використовуйте формат 'YYYY-MM-DD'.")
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = self.find_phone(old_phone)
        if old_phone_obj is not None:
            old_phone_obj.value = new_phone
        else:
            raise ValueError("Телефон для редагування не існує.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
    
    def days_to_birthday(self, birthday):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = datetime(today.year, self.birthday.date_value.month, self.birthday.date_value.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.date_value.month, self.birthday.date_value.day).date()
            return (next_birthday - today).days
        else:
            return None
    
    def search_contacts(self, phone):
        keyword = input("Enter keyword: ")
        for ph in self.phones:
            if (self.name.value.lower()).startswith(keyword.lower()):
                print(f"{self.name.value} {ph.value}")
            elif (ph.value).startswith(keyword):
                print(f"{self.name.value} {ph.value}")
            else:
                print(f"No name in list with this attribute {keyword}")

    def to_dict(self):
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": self.birthday.value if self.birthday else None,
            "days to birthday": self.days_to_birthday(self.birthday)
        }

    @staticmethod
    def from_dict(d):
        name = d["name"]
        phones = d["phones"]
        birthday = d["birthday"]
        return Record(name, birthday)


    def __str__(self):
        # return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birth: {self.birthday} ({Record.days_to_birthday(self, self.birthday)} day to birthday))"
        if Birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birth: {self.birthday} ({self.days_to_birthday(self.birthday)} day to birthday)"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"




    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def pack_user(self):
        file_name = "users.json"
        with open(file_name, "w") as fh:
            json.dump([record.to_dict() for record in self.data.values()], fh, indent=4)


    def unpack_user(self):
        with open("users.json", "r") as fh:
            self.data = json.load(fh)

        
    



class Iterator:
    MAX_VALUE = 0

    def __init__(self, adressBook):
        self.current_value = 0
        self.adressBook = AddressBook
        self.MAX_VALUE = len(adressBook.data)

    def __next__(self):
        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.adressBook.data[self.current_value]
        raise StopIteration


if __name__ == "__main__":
    
    book = AddressBook()

    john_record = Record("John","2003-07-11" )
    john_record.add_phone("5555555555")
    john_record.days_to_birthday("2003-07-11")
    book.add_record(john_record)
    john_record.search_contacts(Record)

    tanya_rec = Record("Tanya", "1990-09-12")
    tanya_rec.add_phone("0852869490")
    tanya_rec.days_to_birthday("1990-09-12")
    book.add_record(tanya_rec)
    tanya_rec.search_contacts(Record)

    tany_rec = Record("vova", "2000-02-28")
    tany_rec.add_phone("0852869490")
    tany_rec.days_to_birthday("2000-02-28")
    book.add_record(tany_rec)
    tany_rec.search_contacts(Record)

    pack_user = book.pack_user()
    unpack_user = book.unpack_user()