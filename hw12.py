from collections import UserDict
from datetime import datetime
import pickle



class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = value
        except: ValueError("Value must be an integer")



class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not all([len(value) == 10, value.isdigit()]):
            raise ValueError("Номер телефону повинен складатися з 10 цифр.")
        self._value = value

    def __eq__(self, __value: object) -> bool:
        return self._value == __value._value




class Birthday(Field):
    def __init__(self, value) -> None:
        self._value = None
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.strptime(value, '%Y-%m-%d')

    def __str__(self):
        return datetime.strftime(self.value, '%Y-%m-%d')


class Record:
    def __init__(self, name, phone= None, birthday= None) -> None:
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone (self, phone):
        new_phone = Phone(phone)
        if new_phone not in self.phones:
            return self.phones.append(new_phone)
        raise ValueError("Phone in list")

    def remove_phone(self, phone):
        phone = Phone(phone)
        if phone in self.phones:
            return self.phones.remove(phone)
        return f"No record {phone}"

    def edit_phone(self, phone, new_phone):
        old_phone = Phone(phone)
        new_phone = Phone(phone)
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
        raise ValueError("Телефон для редагування не існує.") 


        

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
    
    def days_to_birthday(self):
        if self.birthday:
            current_date = datetime.now()
            user_date = datetime.strptime(str(self.birthday), '%Y-%m-%d')
            user_date = user_date.replace(year=current_date.year)
            delta_days = user_date - current_date
            if delta_days.days > 0:
                return f"Days left {delta_days.days}, before birthday"
            else:
                user_date = user_date.replace(year=user_date.year+1)
                delta_days = user_date - current_date
                return f" {delta_days.days} Days left before birthday"
        else:
            return None
    
    def search_contacts(self):
        while True:
            keyword = input("Enter keyword: ")
            if keyword:
                if keyword.lower() in self.name.value.lower():
                    print(f"{self.name.value} - {', '.join(p.value for p in self.phones)}")
                for phone in self.phones:
                    if keyword in phone.value:
                        print(f"{self.name.value} - {phone.value}")
            if keyword == "end":
                break
            


    def __str__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "Birthday not set"
        days_to_birthday = self.days_to_birthday()
        return f'{self.name} - {phone_numbers}; ( {birthday}, {days_to_birthday} )'




class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    
    def pack_user(self):
        with open("users.bin", "wb") as fh:
            pickle.dump(self.data, fh)

    def unpack_user(self):
        with open("users.bin", "rb") as fh:
            self.data = pickle.load(fh)


if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John", "0852869490", "2020-1-1")
    john_record.add_phone("0852869499")
    john_record.add_phone("0994848744")
    book.add_record(john_record)

    # Search contacts
    john_record.search_contacts()
