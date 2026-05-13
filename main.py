from controllers import BankController
from views import BankView

class BankApplication:
    """Главное приложение банка"""

    def __init__(self):
        self.controller = BankController()
        self.view = BankView()

    def run(self):
        """Запуск приложения"""
        self.view.show_message("Добро пожаловать в банковскую систему!")

        # Попытка загрузить данные при запуске
        success, message = self.controller.load_from_json()
        if success:
            self.view.show_message(message)

        while True:
            choice = self.view.show_menu()

            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.show_accounts()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.withdraw()
            elif choice == '5':
                self.transfer()
            elif choice == '6':
                self.show_transactions()
            elif choice == '7':
                self.filter_transactions()
            elif choice == '8':
                self.save_data()
            elif choice == '9':
                self.load_data()
            elif choice == '0':
                self.view.show_message("До свидания!")
                break
            else:
                self.view.show_message("Неверный выбор. Попробуйте снова.", is_error=True)

    def create_account(self):
        """Создание нового счета"""
        owner_name, account_type = self.view.get_account_info()
        if owner_name and account_type:
            try:
                account = self.controller.create_account(owner_name, account_type)
                self.view.show_message(f"Счет успешно создан! ID: {account.account_id}")
            except Exception as e:
                self.view.show_message(str(e), is_error=True)

    def show_accounts(self):
        """Просмотр всех счетов"""
        accounts = self.controller.get_all_accounts()
        self.view.show_accounts(accounts)

    def deposit(self):
        """Внесение депозита"""
        account_id, amount = self.view.get_transaction_info()
        if account_id is not None and amount is not None:
            try:
                transaction = self.controller.deposit(account_id, amount)
                self.view.show_message(f"Внесено ${amount:.2f} на счет #{account_id}")
            except Exception as e:
                self.view.show_message(str(e), is_error=True)

    def withdraw(self):
        """Снятие средств"""
        account_id, amount = self.view.get_transaction_info()
        if account_id is not None and amount is not None:
            try:
                transaction = self.controller.withdraw(account_id, amount)
                self.view.show_message(f"Снято ${amount:.2f} со счета #{account_id}")
            except Exception as e:
                self.view.show_message(str(e), is_error=True)

    def transfer(self):
        """Перевод средств"""
        from_id, to_id, amount = self.view.get_transfer_info()
        if from_id is not None and to_id is not None and amount is not None:
            try:
                transaction = self.controller.transfer(from_id, to_id, amount)
                self.view.show_message(f"Переведено ${amount:.2f} со счета #{from_id} на счет #{to_id}")
            except Exception as e:
                self.view.show_message(str(e), is_error=True)

    def show_transactions(self):
        """Показать все транзакции"""
        transactions = self.controller.get_account_transactions()
        self.view.show_transactions(transactions)

    def filter_transactions(self):
        """Фильтрация транзакций"""
        filter_type, filter_value = self.view.get_filter_criteria()
        transactions = self.controller.get_account_transactions()
        filtered = self.controller.filter_transactions(transactions, filter_type, filter_value)
        self.view.show_transactions(filtered)

    def save_data(self):
        """Сохранение данных"""
        success, message = self.controller.save_to_json()
        self.view.show_message(message, is_error=not success)

    def load_data(self):
        """Загрузка данных"""
        success, message = self.controller.load_from_json()
        self.view.show_message(message, is_error=not success)

if __name__ == "__main__":
    app = BankApplication()
    app.run()
