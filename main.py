from contacts import AddressBook, Record, Name, Phone, Birthday
from datetime import datetime

class ContactBot:
    def __init__(self, address_book):
        self.address_book = address_book

    @staticmethod
    def hello():
        return "How can I help you?"

    def add(self, data):
        try:
            name, phone = data.split()
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
            return f"Contact {name} added with phone {phone}"
        except ValueError:
            raise ValueError("Invalid data format. Please provide both name and phone.")

    def change(self, data):
        try:
            name, phone = data.split()
            record = self.address_book.find(name)
            if record:
                record.add_phone(phone)
                return f"Phone number updated for {name}"
            else:
                raise IndexError("Contact not found")
        except ValueError:
            raise ValueError("Invalid data format. Please provide both name and phone.")

    def phone(self, name):
        record = self.address_book.find(name)
        return record.phones if record else "Contact not found"

    def show_all(self):
        if not self.address_book:
            return "No contacts available"
        else:
            result = "\n".join(str(record) for record in self.address_book.data.values())
            return result

    def add_birthday(self, data):
        try:
            name, birthday = data.split()
            if name in self.address_book:
                self.address_book[name].birthday = Birthday(birthday)
                return f"Birthday added for {name}"
            else:
                return f"Contact with name {name} does not exist."
        except ValueError:
            raise ValueError("Invalid data format. Please provide both name and birthday.")

    def delete(self, name):
        self.address_book.delete(name)
        return f"Contact {name} deleted"

    def search(self, name):
        found_records = [record for record in self.address_book.data.values() if name.lower() in record.name.value.lower()]
        if found_records:
            return "\n".join(str(record) for record in found_records)
        else:
            return f"No contacts found matching '{name}'"

    def main(self):
        while True:
            user_input = input("Enter command: ").lower()
            if user_input in ["good bye", "close", "exit", "."]:
                print("Good bye!")
                self.address_book.save_to_json()
                break
            elif user_input.startswith("add_birthday"):
                data = user_input[len("add_birthday")+1:]
                print(self.add_birthday(data))
            elif user_input == "hello":
                print(self.hello())
            elif user_input.startswith("add"):
                data = user_input[4:]
                print(self.add(data))
            elif user_input.startswith("change"):
                data = user_input[7:]
                print(self.change(data))
            elif user_input.startswith("phone"):
                name = user_input[6:]
                print(self.phone(name))
            elif user_input == "show all":
                print(self.show_all())
            elif user_input.startswith("delete"):
                name = user_input[7:]
                print(self.delete(name))
            elif user_input.startswith("search"):
                name = user_input.split(" ", 1)[1]
                print(self.search(name))
            else:
                print("Invalid command. Try again.")


if __name__ == "__main__":
    address_book = AddressBook("address_book.json")
    bot = ContactBot(address_book)
    bot.main()
