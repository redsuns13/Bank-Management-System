
import json
import random
import string
import hashlib
import secrets
from pathlib import Path
from datetime import datetime


class BankError(Exception):
    """Custom exception for banking operations."""
    pass


class Bank:

    database = "data.json"

    def __init__(self):
        self.data = {
            "accounts": [],
            "transactions": []
        }
        self.load_data()

    # --------------------------------
    # Load and save JSON data
    # --------------------------------

    def load_data(self):
        path = Path(self.database)

        if path.exists():
            try:
                with open(path, "r") as file:
                    stored_data = json.load(file)

                # Support the original JSON list format
                if isinstance(stored_data, list):
                    self.data["accounts"] = stored_data
                    self._migrate_old_accounts()
                    self.save_data()

                elif isinstance(stored_data, dict):
                    self.data = stored_data
                    self.data.setdefault("accounts", [])
                    self.data.setdefault("transactions", [])

            except (json.JSONDecodeError, OSError) as error:
                raise BankError(f"Could not load database: {error}")

    def save_data(self):
        path = Path(self.database)
        temporary_path = path.with_suffix(".tmp")

        with open(temporary_path, "w") as file:
            json.dump(self.data, file, indent=4)

        temporary_path.replace(path)

    # --------------------------------
    # PIN security
    # --------------------------------

    @staticmethod
    def _hash_pin(pin, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)

        hashed_pin = hashlib.pbkdf2_hmac(
            "sha256",
            str(pin).encode(),
            salt.encode(),
            200000
        ).hex()

        return salt, hashed_pin

    def _verify_pin(self, account, pin):
        salt, hashed_pin = self._hash_pin(
            pin,
            account["pin_salt"]
        )

        return secrets.compare_digest(
            hashed_pin,
            account["pin_hash"]
        )

    # --------------------------------
    # Account number generation
    # --------------------------------

    def _generate_account_number(self):
        while True:
            account_number = "".join(
                random.choices(string.digits, k=10)
            )

            exists = any(
                account["account_number"] == account_number
                for account in self.data["accounts"]
            )

            if not exists:
                return account_number

    # --------------------------------
    # Account lookup
    # --------------------------------

    def _find_account(self, account_number):
        for account in self.data["accounts"]:
            if account["account_number"] == account_number:
                return account

        raise BankError("Account not found.")

    def _authenticate(self, account_number, pin):
        account = self._find_account(account_number)

        if not self._verify_pin(account, pin):
            raise BankError("Incorrect PIN.")

        return account

    # --------------------------------
    # Transaction history
    # --------------------------------

    def _add_transaction(self, account_number, transaction_type, amount):
        transaction = {
            "account_number": account_number,
            "type": transaction_type,
            "amount": amount,
            "date": datetime.now().isoformat(timespec="seconds")
        }

        self.data["transactions"].append(transaction)

    # --------------------------------
    # Create account
    # --------------------------------

    def create_account(self, name, age, email, pin):

        name = name.strip()
        email = email.strip().lower()
        pin = str(pin)

        if not name:
            raise BankError("Name cannot be empty.")

        if int(age) < 18:
            raise BankError("You must be at least 18 years old.")

        if not email or "@" not in email:
            raise BankError("Enter a valid email address.")

        if len(pin) != 4 or not pin.isdigit():
            raise BankError("PIN must contain exactly 4 digits.")

        for account in self.data["accounts"]:
            if account["email"] == email:
                raise BankError("Email already registered.")

        salt, hashed_pin = self._hash_pin(pin)

        account = {
            "name": name,
            "age": int(age),
            "email": email,
            "pin_salt": salt,
            "pin_hash": hashed_pin,
            "account_number": self._generate_account_number(),
            "balance": 0
        }

        self.data["accounts"].append(account)
        self.save_data()

        return account.copy()

    # --------------------------------
    # Login
    # --------------------------------

    def login(self, account_number, pin):

        account = self._authenticate(
            account_number.strip(),
            str(pin)
        )

        return account.copy()

    # --------------------------------
    # Deposit money
    # --------------------------------

    def deposit(self, account_number, amount):

        account = self._find_account(account_number)

        amount = round(float(amount), 2)

        if amount <= 0:
            raise BankError("Deposit amount must be greater than zero.")

        if amount > 10000:
            raise BankError("Maximum deposit is SAR 10,000.")

        amount_halalas = round(amount * 100)

        account["balance"] += amount_halalas

        self._add_transaction(
            account_number,
            "Deposit",
            amount_halalas
        )

        self.save_data()

        return account.copy()

    # --------------------------------
    # Withdraw money
    # --------------------------------

    def withdraw(self, account_number, amount):

        account = self._find_account(account_number)

        amount = round(float(amount), 2)

        if amount <= 0:
            raise BankError("Withdrawal amount must be greater than zero.")

        amount_halalas = round(amount * 100)

        if account["balance"] < amount_halalas:
            raise BankError("Insufficient balance.")

        account["balance"] -= amount_halalas

        self._add_transaction(
            account_number,
            "Withdrawal",
            amount_halalas
        )

        self.save_data()

        return account.copy()

    # --------------------------------
    # Show transactions
    # --------------------------------

    def get_transactions(self, account_number):

        self._find_account(account_number)

        transactions = [
            transaction
            for transaction in self.data["transactions"]
            if transaction["account_number"] == account_number
        ]

        return [
            {
                **transaction,
                "amount": transaction["amount"] / 100
            }
            for transaction in transactions
        ]

    # --------------------------------
    # Update account details
    # --------------------------------

    def update_details(self, account_number, name, age, email):

        account = self._find_account(account_number)

        name = name.strip()
        email = email.strip().lower()

        if not name:
            raise BankError("Name cannot be empty.")

        if int(age) < 18:
            raise BankError("Age must be at least 18.")

        if not email or "@" not in email:
            raise BankError("Enter a valid email address.")

        for other in self.data["accounts"]:
            if (
                other["email"] == email
                and other["account_number"] != account_number
            ):
                raise BankError("Email already registered.")

        account["name"] = name
        account["age"] = int(age)
        account["email"] = email

        self.save_data()

        return account.copy()

    # --------------------------------
    # Close account
    # --------------------------------

    def close_account(self, account_number):

        account = self._find_account(account_number)

        if account["balance"] != 0:
            raise BankError(
                "Please withdraw your remaining balance before closing."
            )

        self.data["accounts"].remove(account)
        self.save_data()

        return True

    # --------------------------------
    # Migrate original account format
    # --------------------------------

    def _migrate_old_accounts(self):

        migrated_accounts = []

        for old in self.data["accounts"]:

            # Already in the new format
            if "pin_hash" in old:
                migrated_accounts.append(old)
                continue

            old_pin = str(old["Pin"]).zfill(4)
            salt, hashed_pin = self._hash_pin(old_pin)

            account = {
                "name": old["Name"],
                "age": old["Age"],
                "email": old["Email"].lower(),
                "pin_salt": salt,
                "pin_hash": hashed_pin,
                "account_number": old["Account_Number"],
                "balance": round(float(old["Balance"]) * 100)
            }

            migrated_accounts.append(account)

        self.data["accounts"] = migrated_accounts
