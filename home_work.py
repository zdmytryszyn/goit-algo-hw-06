from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class PhoneVerificationError(Exception):
    pass


class Phone(Field):
    def __init__(self, value: str):
        self.verify_phone(value=value)
        super().__init__(value)

    @staticmethod
    def verify_phone(value: str):
        if type(value) is not str:
            raise PhoneVerificationError(f"Incorrect phone data type given: {type(value)}, must be 'str'")
        if len(value) != 10:
            raise PhoneVerificationError("Incorrect length of phone, must be 10 digits")
        if not value.isdigit():
            raise PhoneVerificationError(f"Phone must include only numbers, '{value}' is not a number")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None | str:
        for phone_record in self.phones:
            if phone_record.value == phone:
                return "Phone already in the record!"

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None | str:
        for phone_record in self.phones:
            if phone_record.value == phone:
                self.phones.remove(phone_record)
        else:
            return "Phone you are trying to remove is not in the record. Add the phone"

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        try:
            for phone_record in self.phones:
                if phone_record.value == old_phone and Phone.verify_phone(new_phone):
                    phone_record.value = new_phone
                    return
            else:
                raise ValueError(
                    "Incorrect input. Phone you are trying to edit "
                    "is not in the record or incorrect input type given, "
                    "must be 'str'."
                )
        except PhoneVerificationError:
            raise ValueError(
                "New phone value is incorrect. "
                "Must be 10 digits long, include only letters and be of 'str' type"
            )

    def find_phone(self, phone: str):
        return next(
            (phone_record for phone_record in self.phones if phone_record.value == phone),
            None
        )

    def __str__(self) -> str:
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join((p.value if self.phones else None) for p in self.phones)}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data.keys():
            del self.data[name]

    def __str__(self) -> str:
        return '\n'.join(str(self.data[record]) for record in self.data)
