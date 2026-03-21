"""
Factory Method - konta bankowe.

Przykład logiki biznesowej bankowego serwisu internetowego.
Factory Method tworzy obiekty określonego rodzaju konta
w zależności od wyborów klienta przy rejestrowaniu konta.
"""

from abc import ABC, abstractmethod


class BankAccount(ABC):
    @abstractmethod
    def validate_user_identity(self):
        pass

    @abstractmethod
    def calculate_interest_rate(self):
        pass

    @abstractmethod
    def register_account(self):
        pass


class PersonalAccount(BankAccount):
    def validate_user_identity(self):
        print("Weryfikacja tożsamości: dowód osobisty...")

    def calculate_interest_rate(self):
        print("Oprocentowanie konta osobistego: 0.5%")

    def register_account(self):
        print("Konto osobiste zarejestrowane!")


class BusinessAccount(BankAccount):
    def validate_user_identity(self):
        print("Weryfikacja tożsamości: KRS + NIP...")

    def calculate_interest_rate(self):
        print("Oprocentowanie konta firmowego: 0.3%")

    def register_account(self):
        print("Konto firmowe zarejestrowane!")


class SavingsAccount(BankAccount):
    def validate_user_identity(self):
        print("Weryfikacja tożsamości: dowód osobisty...")

    def calculate_interest_rate(self):
        print("Oprocentowanie konta oszczędnościowego: 2.0%")

    def register_account(self):
        print("Konto oszczędnościowe zarejestrowane!")


def account_factory(account_type: str) -> BankAccount:
    accounts = {
        "personal": PersonalAccount,
        "business": BusinessAccount,
        "savings": SavingsAccount,
    }
    account_class = accounts.get(account_type)
    if not account_class:
        raise ValueError(f"Nieznany typ konta: {account_type}")
    return account_class()


# Użycie
if __name__ == "__main__":
    account = account_factory("savings")
    account.validate_user_identity()
    account.calculate_interest_rate()
    account.register_account()
