class BankView:
    """Класс представления для взаимодействия с пользователем"""

    @staticmethod
    def show_menu():
        print("\n" + "="*50)
        print("          БАНКОВСКАЯ СИСТЕМА")
        print("="*50)
        print("1. Создать новый счет")
        print("2. Просмотреть все счета")
        print("3. Внести депозит")
        print("4. Снять средства")
        print("5. Перевести средства между счетами")
        print("6. Показать историю транзакций")
        print("7. Фильтрация транзакций")
        print("8. Сохранить данные")
        print("9. Загрузить данные")
        print("0. Выйти")
        print("-"*50)
        return input("Выберите опцию: ")

    @staticmethod
    def get_account_info():
        print("\n--- Создание нового счета ---")
        owner_name = input("Имя владельца: ")
        print("Типы счетов:")
        print("1. Расчетный счет (Checking)")
        print("2. Сберегательный счет (Savings)")
        print("3. Кредитный счет (Credit)")
        account_type = input("Выберите тип (1-3): ")

        account_types = {'1': 'Checking', '2': 'Savings', '3': 'Credit'}
        return owner_name, account_types.get(account_type, 'Checking')

    @staticmethod
    def get_transaction_info():
        try:
            account_id = int(input("ID счета: "))
            amount = float(input("Сумма: $"))
            return account_id, amount
        except ValueError:
            print("❌ Ошибка: Некорректный ввод!")
            return None, None

    @staticmethod
    def get_transfer_info():
        try:
            from_id = int(input("ID счета-отправителя: "))
            to_id = int(input("ID счета-получателя: "))
            amount = float(input("Сумма перевода: $"))
            return from_id, to_id, amount
        except ValueError:
            print("❌ Ошибка: Некорректный ввод!")
            return None, None, None

    @staticmethod
    def get_filter_criteria():
        print("\n--- Фильтрация транзакций ---")
        print("1. Фильтр по дате")
        print("2. Фильтр по типу транзакции")
        print("3. Фильтр по ID счета")
        print("4. Показать все")
        choice = input("Выберите фильтр: ")

        filter_type = None
        filter_value = None

        if choice == '1':
            date_str = input("Введите дату (YYYY-MM-DD): ")
            try:
                from datetime import datetime
                filter_type = 'date'
                filter_value = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print("❌ Некорректный формат даты!")
        elif choice == '2':
            print("Типы: deposit, withdraw, transfer")
            filter_type = 'type'
            filter_value = input("Введите тип транзакции: ").lower()
        elif choice == '3':
            try:
                filter_type = 'account'
                filter_value = int(input("Введите ID счета: "))
            except ValueError:
                print("❌ Некорректный ID!")

        return filter_type, filter_value

    @staticmethod
    def show_accounts(accounts):
        if not accounts:
            print("\n❌ Счета не найдены!")
            return

        print("\n" + "="*60)
        print("СПИСОК СЧЕТОВ")
        print("="*60)
        for account in accounts:
            print(account)
        print("-"*60)

    @staticmethod
    def show_transactions(transactions):
        if not transactions:
            print("\n❌ Транзакции не найдены!")
            return

        print("\n" + "="*60)
        print("ИСТОРИЯ ТРАНЗАКЦИЙ")
        print("="*60)
        for transaction in transactions:
            print(transaction)
        print("-"*60)

    @staticmethod
    def show_message(message, is_error=False):
        if is_error:
            print(f"\n❌ {message}")
        else:
            print(f"\n✅ {message}")

    @staticmethod
    def show_info(message):
        print(f"\nℹ️ {message}")
