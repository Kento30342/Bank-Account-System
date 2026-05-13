import json
from datetime import datetime
from collections import deque
from abc import ABC, abstractmethod

class Transaction:
    """Класс транзакции"""
    def __init__(self, transaction_id, account_id, transaction_type, amount, date=None):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type  # deposit, withdraw, transfer
        self.amount = amount
        self.date = date or datetime.now()

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'date': self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['transaction_id'],
            data['account_id'],
            data['transaction_type'],
            data['amount'],
            datetime.fromisoformat(data['date'])
        )

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d %H:%M:%S')}] {self.transaction_type}: ${self.amount:.2f}"

class Account(ABC):
    """Абстрактный базовый класс счета"""
    def __init__(self, account_id, owner_name, balance=0):
        self.account_id = account_id
        self.owner_name = owner_name
        self.balance = balance
        self.transaction_history = deque()

    @abstractmethod
    def get_account_type(self):
        pass

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount
        transaction = Transaction(
            len(self.transaction_history) + 1,
            self.account_id,
            "deposit",
            amount
        )
        self.transaction_history.append(transaction)
        return transaction

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        transaction = Transaction(
            len(self.transaction_history) + 1,
            self.account_id,
            "withdraw",
            amount
        )
        self.transaction_history.append(transaction)
        return transaction

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'owner_name': self.owner_name,
            'balance': self.balance,
            'account_type': self.get_account_type(),
            'transaction_history': [t.to_dict() for t in self.transaction_history]
        }

    @classmethod
    def from_dict(cls, data):
        if data['account_type'] == 'Checking':
            account = CheckingAccount(data['account_id'], data['owner_name'], data['balance'])
        elif data['account_type'] == 'Savings':
            account = SavingsAccount(data['account_id'], data['owner_name'], data['balance'])
        elif data['account_type'] == 'Credit':
            account = CreditAccount(data['account_id'], data['owner_name'], data['balance'])
        else:
            raise ValueError(f"Неизвестный тип счета: {data['account_type']}")

        for t_data in data['transaction_history']:
            account.transaction_history.append(Transaction.from_dict(t_data))

        return account

    def __str__(self):
        return f"{self.get_account_type()} счет #{self.account_id} - Владелец: {self.owner_name}, Баланс: ${self.balance:.2f}"

class CheckingAccount(Account):
    """Расчетный счет"""
    def get_account_type(self):
        return "Checking"

class SavingsAccount(Account):
    """Сберегательный счет"""
    def get_account_type(self):
        return "Savings"

    def withdraw(self, amount):
        if amount > 1000:
            raise ValueError("Лимит снятия со сберегательного счета: $1000 в день")
        return super().withdraw(amount)

class CreditAccount(Account):
    """Кредитный счет"""
    def __init__(self, account_id, owner_name, balance=0, credit_limit=2000):
        super().__init__(account_id, owner_name, balance)
        self.credit_limit = credit_limit

    def get_account_type(self):
        return "Credit"

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance + self.credit_limit:
            raise ValueError(f"Превышен кредитный лимит (${self.credit_limit})")
        self.balance -= amount
        transaction = Transaction(
            len(self.transaction_history) + 1,
            self.account_id,
            "withdraw",
            amount
        )
        self.transaction_history.append(transaction)
        return transaction

    def to_dict(self):
        data = super().to_dict()
        data['credit_limit'] = self.credit_limit
        return data

    @classmethod
    def from_dict(cls, data):
        account = super().from_dict(data)
        account.credit_limit = data.get('credit_limit', 2000)
        return account
