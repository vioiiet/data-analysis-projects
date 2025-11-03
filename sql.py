import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
import random


def generate_transactions(num_records=1000):


    """Генерация реалистичных банковских транзакций"""
    print(" Генерация данных...")

    # Создаем папку data если её нет
    os.makedirs('data', exist_ok=True)

    categories = ['food', 'transport', 'shopping', 'entertainment', 'health', 'transfer', 'salary', 'withdrawal']
    merchants = {
        'food': ['McDonalds', 'KFC', 'Burger King', ' grocery_store', 'Restaurant'],
        'transport': ['Uber', 'Taxi', 'Metro', 'Bus', 'Gas Station'],
        'shopping': ['Amazon', 'AliExpress', 'OZON', 'Wildberries', 'MVideo'],
        'entertainment': ['Cinema', 'Netflix', 'Spotify', 'YouTube Premium', 'Club'],
        'health': ['Pharmacy', 'Hospital', 'Dental Clinic', 'Fitness Club'],
        'transfer': ['Bank Transfer', 'Peer-to-Peer', 'Remittance'],
        'salary': ['Company Inc', 'Freelance', 'Investment'],
        'withdrawal': ['ATM', 'Bank Branch', 'Cash withdrawal']
    }

    # Генерация дат за последние 3 месяца
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    data = []
    for i in range(num_records):
        transaction_date = start_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Реалистичное распределение сумм
        if random.random() < 0.7:  # 70% мелкие транзакции
            amount = round(random.uniform(50, 5000), 2)
        else:  # 30% крупные транзакции
            amount = round(random.uniform(5000, 50000), 2)

        category = random.choice(categories)
        transaction_type = 'debit' if category != 'salary' else 'credit'
        merchant = random.choice(merchants[category])

        # Подозрительные транзакции
        is_suspicious = (amount > 30000 and transaction_type == 'debit') or (amount > 100000)

        data.append({
            'transaction_id': i + 1,
            'user_id': random.randint(1, 100),
            'amount': amount,
            'transaction_type': transaction_type,
            'category': category,
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'merchant': merchant,
            'is_suspicious': is_suspicious,
            'location': f'City_{random.randint(1, 10)}'
        })

    df = pd.DataFrame(data)
    df.to_csv('data/transactions.csv', index=False)
    print(f"Сгенерировано {num_records} транзакций")
    return df


class BankTransactionAnalyzer:
    def __init__(self, csv_file='data/transactions.csv'):



        """Инициализация анализатора"""
        if not os.path.exists(csv_file):
            print("Файл с данными не найден.")
            generate_transactions(2000)

        self.df = pd.read_csv(csv_file)
        self.conn = sqlite3.connect(':memory:')
        self.df.to_sql('transactions', self.conn, index=False, if_exists='replace')
        print("База данных загружена")

    def run_comprehensive_analysis(self):



        """Полный анализ транзакций"""
        print("\n" + "=" * 60)
        print("=" * 60)

        self._basic_statistics()
        self._category_analysis()
        self._suspicious_activity_detection()
        self._user_behavior_analysis()
        self._monthly_trends()
        self._aml_compliance_check()

    def _basic_statistics(self):
        """Базовая статистика"""
        print(" 1. ОСНОВНАЯ СТАТИСТИКА")

        query = """
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(DISTINCT user_id) as unique_users,
            ROUND(SUM(amount), 2) as total_volume,
            ROUND(AVG(amount), 2) as avg_transaction,
            ROUND(MAX(amount), 2) as max_transaction,
            ROUND(MIN(amount), 2) as min_transaction
        FROM transactions;
        """
        result = pd.read_sql_query(query, self.conn)
        print(result.to_string(index=False))

    def _category_analysis(self):


        """Анализ по категориям"""
        print("  2. АНАЛИЗ ПО КАТЕГОРИЯМ")

        # Расходы по категориям
        query = """
        SELECT 
            category,
            COUNT(*) as count,
            ROUND(SUM(amount), 2) as total_amount,
            ROUND(AVG(amount), 2) as avg_amount,
            ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM transactions WHERE transaction_type = 'debit'), 2) as percentage
        FROM transactions 
        WHERE transaction_type = 'debit'
        GROUP BY category
        ORDER BY total_amount DESC;
        """
        result = pd.read_sql_query(query, self.conn)
        print(" Расходы по категориям:")
        print(result.to_string(index=False))

    def _suspicious_activity_detection(self):



        """Обнаружение подозрительной активности"""
        print(" 3. ДЕТЕКЦИЯ ПОДОЗРИТЕЛЬНОЙ АКТИВНОСТИ (AML)")

        # Крупные транзакции
        query_large = """
        SELECT 
            user_id,
            COUNT(*) as large_transactions,
            ROUND(SUM(amount), 2) as total_large_amount
        FROM transactions 
        WHERE amount > 30000 
        GROUP BY user_id
        HAVING COUNT(*) > 2
        ORDER BY total_large_amount DESC;
        """
        result_large = pd.read_sql_query(query_large, self.conn)

        if len(result_large) > 0:
            print("Пользователи с частыми крупными транзакциями:")
            print(result_large.to_string(index=False))
        else:
            print("Подозрительных паттернов не обнаружено, все хорошо")

        # Самые крупные транзакции
        query_top = """
        SELECT 
            transaction_id, user_id, amount, category, merchant, transaction_date
        FROM transactions 
        WHERE amount > 40000
        ORDER BY amount DESC
        LIMIT 5;
        """
        result_top = pd.read_sql_query(query_top, self.conn)
        if len(result_top) > 0:
            print(" Топ-5 самых крупных транзакций:")
            print(result_top.to_string(index=False))

    def _user_behavior_analysis(self):



        """Анализ поведения пользователей"""
        print(" 4. АНАЛИЗ ПОВЕДЕНИЯ ПОЛЬЗОВАТЕЛЕЙ")

        # Самые активные пользователи
        query_active = """
        SELECT 
            user_id,
            COUNT(*) as transaction_count,
            ROUND(SUM(amount), 2) as total_volume,
            ROUND(AVG(amount), 2) as avg_transaction,
            COUNT(DISTINCT category) as unique_categories
        FROM transactions
        GROUP BY user_id
        ORDER BY total_volume DESC
        LIMIT 10;
        """
        result_active = pd.read_sql_query(query_active, self.conn)
        print("самые активных пользователи:")
        print(result_active.to_string(index=False))

    def _monthly_trends(self):



        """Анализ месячных трендов"""
        print(" 5.ТРЕНДЫ")

        query = """
        SELECT 
            strftime('%Y-%m', transaction_date) as month,
            COUNT(*) as transaction_count,
            ROUND(SUM(amount), 2) as monthly_volume,
            ROUND(AVG(amount), 2) as avg_monthly_transaction
        FROM transactions
        GROUP BY month
        ORDER BY month;
        """
        result = pd.read_sql_query(query, self.conn)
        print(" Динамика по месяцам:")
        print(result.to_string(index=False))

    def _aml_compliance_check(self):


        """Проверка соответствия AML требованиям"""
        print("  6. AML COMPLIANCE CHECK")

        query = """
        SELECT 
            COUNT(*) as total_suspicious,
            ROUND(SUM(amount), 2) as suspicious_volume,
            COUNT(DISTINCT user_id) as users_involved
        FROM transactions 
        WHERE is_suspicious = 1 OR amount > 40000;
        """
        result = pd.read_sql_query(query, self.conn)
        print(" Статистика подозрительной активности")
        print(result.to_string(index=False))

        # Рекомендации по AML
        if result.iloc[0]['total_suspicious'] > 10:
            print("  ВНИМАНИЕ: Обнаружено значительное количество подозрительных операций!")


    def close(self):

        """Закрытие соединения"""
        self.conn.close()


# Запуск анализа
if __name__ == "__main__":
    print("запуск анализа")
    analyzer = BankTransactionAnalyzer()
    analyzer.run_comprehensive_analysis()
    analyzer.close()
    print("")