import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_transactions(num_records=10000):
    # Списки для генерации данных
    categories = ['food', 'transport', 'shopping', 'entertainment', 'health', 'transfer', 'salary', 'withdrawal']
    transaction_types = ['debit', 'credit']

    # Генерация дат за последние 6 месяцев
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    data = []
    for i in range(num_records):
        transaction_date = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        amount = round(random.uniform(10, 50000), 2)
        category = random.choice(categories)
        transaction_type = random.choice(transaction_types)

        # Подозрительные транзакции (большие суммы)
        is_suspicious = amount > 30000 and transaction_type == 'debit'

        data.append({
            'transaction_id': i + 1,
            'user_id': random.randint(1, 1000),
            'amount': amount,
            'transaction_type': transaction_type,
            'category': category,
            'transaction_date': transaction_date,
            'merchant': f'Merchant_{random.randint(1, 100)}',
            'is_suspicious': is_suspicious
        })

    df = pd.DataFrame(data)
    df.to_csv('data/transactions.csv', index=False)
    print(f"Сгенерировано {num_records} транзакций")
    return df


if __name__ == "__main__":
    generate_transactions()