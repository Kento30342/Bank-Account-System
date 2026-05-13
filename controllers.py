import json
from datetime import datetime
from models import Account, CheckingAccount, SavingsAccount, CreditAccount, Transaction

class BankController:
    """Контроллер для управления банковской системой"""

    def __init__(self):
        self.accounts = {}
        self.next_account_id = 1

    def create_account(self, owner_name, account_type):
        """Создание нового счета"""
        account_id = self.next_account_id
        self.next_account_id += 1

        if account_type == 'Checking':
            account = CheckingAccount(account_id, owner_name)
        elif account_type == 'Savings':
            account = SavingsAccount(account_id, owner_name)
        elif account_type == 'Credit':
            account = CreditAccount(account_id, owner_name)
        else:
            raise ValueError("Неверный тип счета")

        self.accounts[account_id] = account
        return account

    def get_account(self, account_id):
        """Получение счета по ID"""
        if account_id not in self.accounts:
            raise ValueError(f"Счет #{account_id} не найден")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        """Внесение депозита на счет"""
        account = self.get_account(account_id)
        transaction = account.deposit(amount)
        return transaction

    def withdraw(self, account_id, amount):
        """Снятие средств со счета"""
        account = self.get_account(account_id)
        transaction = account.withdraw(amount)
        return transaction

    def transfer(self, from_account_id, to_account_id, amount):
        """Перевод средств между счетами"""
        if from_account_id == to_account_id:
            raise ValueError("Нельзя перевести средства на тот же счет")

        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        # Снятие со счета отправителя
        withdraw_transaction = from_account.withdraw(amount)

        # Зачисление на счет получателя
        deposit_transaction = to_account.deposit(amount)

        # Создаем транзакцию перевода
        transfer_transaction = Transaction(
            len(from_account.transaction_history) + 1,
            from_account_id,
            f"transfer_to_{to_account_id}",
            amount
        )
        from_account.transaction_history.append(transfer_transaction)

        transfer_transaction2 = Transaction(
            len(to_account.transaction_history) + 1,
            to_account_id,
            f"transfer_from_{from_account_id}",
            amount
        )
        to_account.transaction_history.append(transfer_transaction2)

        return transfer_transaction

    def get_all_accounts(self):
        """Получение всех счетов"""
        return list(self.accounts.values())

    def get_account_transactions(self, account_id=None):
        """Получение транзакций для счета или всех счетов"""
        transactions = []

        if account_id:
            account = self.get_account(account_id)
            transactions = list(account.transaction_history)
        else:
            for account in self.accounts.values():
                transactions.extend(account.transaction_history)

        return sorted(transactions, key=lambda x: x.date, reverse=True)

    def filter_transactions(self, transactions, filter_type, filter_value):
        """Фильтрация транзакций"""
        if not filter_type or not filter_value:
            return transactions

        filtered = []
        for transaction in transactions:
            if filter_type == 'date':
                if transaction.date.date() == filter_value:
                    filtered.append(transaction)
            elif filter_type == 'type':
                if filter_value in transaction.transaction_type:
                    filtered.append(transaction)
            elif filter_type == 'account':
                if transaction.account_id == filter_value:
                    filtered.append(transaction)

        return filtered

    def save_to_json(self, filename='data.json'):
        """Сохранение данных в JSON файл"""
        try:
            data = {
                'next_account_id': self.next_account_id,
                'accounts': [account.to_dict() for account in self.accounts.values()]
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, "Данные успешно сохранены"
        except Exception as e:
            return False, f"Ошибка сохранения: {str(e)}"

    def load_from_json(self, filename='data.json'):
        """Загрузка данных из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.next_account_id = data['next_account_id']
            self.accounts.clear()

            for account_data in data['accounts']:
                account = Account.from_dict(account_data)
                self.accounts[account.account_id] = account

            return True, f"Загружено {len(self.accounts)} счетов"
        except FileNotFoundError:
            return False, "Файл не найден"
        except Exception as e:
            return False, f"Ошибка загрузки: {str(e)}"
