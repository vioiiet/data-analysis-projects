import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import numpy as np

# Настройка стиля для профессиональных графиков
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = [12, 8]


class BankDataVisualizer:
    def __init__(self, csv_file='data/transactions.csv'):
        self.df = pd.read_csv(csv_file)
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
        print("Данные загружены для визуализации")

        # Добавляем недостающие колонки если их нет
        self._add_missing_columns()

    def _add_missing_columns(self):
        """Добавляем недостающие колонки для визуализации"""
        if 'location' not in self.df.columns:
            # Создаем случайные локации
            cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
                      'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону']
            self.df['location'] = np.random.choice(cities, len(self.df))
            print("Добавлена колонка 'location'")

        if 'merchant' not in self.df.columns:
            # Создаем случайных мерчантов
            merchants = ['Amazon', 'OZON', 'Wildberries', 'McDonalds', 'KFC',
                         'Uber', 'Taxi', 'Metro', 'Pharmacy', 'Restaurant']
            self.df['merchant'] = np.random.choice(merchants, len(self.df))
            print(" Добавлена колонка 'merchant'")

    def create_comprehensive_dashboard(self):
        """Создание комплексного дашборда"""
        print(" СОЗДАНИЕ ДАШБОРДА АНАЛИТИКИ...")

        # Создаем сетку графиков (2x4 вместо 3x3)
        fig = plt.figure(figsize=(20, 12))

        # 1. Распределение транзакций по категориям
        ax1 = plt.subplot(2, 4, 1)
        self._plot_category_distribution(ax1)

        # 2. Распределение сумм транзакций
        ax2 = plt.subplot(2, 4, 2)
        self._plot_amount_distribution(ax2)

        # 3. Топ пользователи по объему операций
        ax3 = plt.subplot(2, 4, 3)
        self._plot_top_users(ax3)

        # 4. Динамика транзакций по времени
        ax4 = plt.subplot(2, 4, 4)
        self._plot_temporal_trends(ax4)

        # 5. Heatmap корреляций
        ax5 = plt.subplot(2, 4, 5)
        self._plot_correlation_heatmap(ax5)

        # 6. Подозрительные операции
        ax6 = plt.subplot(2, 4, 6)
        self._plot_suspicious_activity(ax6)

        # 7. Сравнение дебет/кредит
        ax7 = plt.subplot(2, 4, 7)
        self._plot_debit_vs_credit(ax7)

        # 8. Boxplot сумм по категориям
        ax8 = plt.subplot(2, 4, 8)
        self._plot_category_boxplot(ax8)

        plt.tight_layout(pad=3.0)
        plt.savefig('data/banking_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()

    def _plot_category_distribution(self, ax):
        """Распределение транзакций по категориям"""
        category_stats = self.df['category'].value_counts()

        colors = plt.cm.Set3(np.linspace(0, 1, len(category_stats)))
        bars = ax.bar(category_stats.index, category_stats.values, color=colors)

        ax.set_title('РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ', fontsize=12, fontweight='bold')
        ax.set_ylabel('Количество транзакций')
        ax.tick_params(axis='x', rotation=45)

        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=8)

    def _plot_amount_distribution(self, ax):
        """Распределение сумм транзакций"""
        # Исключаем выбросы для лучшей визуализации
        amounts = self.df[self.df['amount'] < self.df['amount'].quantile(0.95)]['amount']

        ax.hist(amounts, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax.axvline(amounts.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'Среднее: {amounts.mean():.2f} руб')
        ax.axvline(amounts.median(), color='green', linestyle='--', linewidth=2,
                   label=f'Медиана: {amounts.median():.2f} руб')

        ax.set_title('РАСПРЕДЕЛЕНИЕ СУММ ТРАНЗАКЦИЙ', fontsize=12, fontweight='bold')
        ax.set_xlabel('Сумма (руб)')
        ax.set_ylabel('Частота')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_top_users(self, ax):
        """Топ-10 пользователей по объему операций"""
        user_stats = self.df.groupby('user_id').agg({
            'amount': 'sum',
            'transaction_id': 'count'
        }).round(2)

        user_stats.columns = ['total_amount', 'transaction_count']
        top_users = user_stats.nlargest(10, 'total_amount')

        y_pos = np.arange(len(top_users))
        bars = ax.barh(y_pos, top_users['total_amount'], color='lightcoral')

        ax.set_yticks(y_pos)
        ax.set_yticklabels([f'User {uid}' for uid in top_users.index], fontsize=8)
        ax.set_xlabel('Общая сумма (руб)')
        ax.set_title(' ТОП-10 ПОЛЬЗОВАТЕЛЕЙ ПО ОБЪЕМУ', fontsize=12, fontweight='bold')

        # Добавляем значения
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + width * 0.01, bar.get_y() + bar.get_height() / 2,
                    f'{width:,.0f} руб', ha='left', va='center', fontweight='bold', fontsize=8)

    def _plot_temporal_trends(self, ax):
        """Динамика транзакций по времени"""
        self.df['date'] = self.df['transaction_date'].dt.date
        daily_stats = self.df.groupby('date').agg({
            'amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()

        ax.plot(daily_stats['date'], daily_stats['amount'],
                marker='o', linewidth=2, markersize=3, color='purple', alpha=0.7)

        ax.set_title('ДИНАМИКА ТРАНЗАКЦИЙ ПО ДНЯМ', fontsize=12, fontweight='bold')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Сумма (руб)')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

    def _plot_correlation_heatmap(self, ax):
        """Тепловая карта корреляций"""
        try:
            # Создаем числовые признаки для корреляции
            numeric_df = self.df.copy()
            numeric_df['is_debit'] = (numeric_df['transaction_type'] == 'debit').astype(int)
            numeric_df['is_suspicious_num'] = numeric_df['is_suspicious'].astype(int)
            numeric_df['hour'] = numeric_df['transaction_date'].dt.hour

            correlation_data = numeric_df[['amount', 'is_debit', 'is_suspicious_num', 'hour', 'user_id']]
            corr_matrix = correlation_data.corr()

            im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

            # Добавляем аннотации
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                            ha='center', va='center', color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black',
                            fontweight='bold', fontsize=8)

            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.columns)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45, fontsize=8)
            ax.set_yticklabels(corr_matrix.columns, fontsize=8)
            ax.set_title(' МАТРИЦА КОРРЕЛЯЦИЙ', fontsize=12, fontweight='bold')
        except Exception as e:
            ax.text(0.5, 0.5, f'Ошибка построения\nкорреляции: {str(e)}',
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title('МАТРИЦА КОРРЕЛЯЦИЙ', fontsize=12, fontweight='bold')

    def _plot_suspicious_activity(self, ax):
        """Визуализация подозрительной активности"""
        # Проверяем есть ли колонка is_suspicious
        if 'is_suspicious' in self.df.columns:
            suspicious = self.df[self.df['is_suspicious'] == True]
        else:
            # Создаем подозрительные операции на основе суммы
            suspicious = self.df[self.df['amount'] > 30000]

        if len(suspicious) > 0:
            suspicious_by_category = suspicious['category'].value_counts()

            colors = ['red' if x > 0 else 'lightgray' for x in suspicious_by_category.values]
            bars = ax.bar(suspicious_by_category.index, suspicious_by_category.values, color=colors)

            ax.set_title( 'ПОДОЗРИТЕЛЬНЫЕ ОПЕРАЦИИ', fontsize=12, fontweight='bold')
            ax.set_ylabel('Количество операций')
            ax.tick_params(axis='x', rotation=45)

            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', fontweight='bold', color='red', fontsize=8)
        else:
            ax.text(0.5, 0.5, ' НЕТ ПОДОЗРИТЕЛЬНЫХ\n   ОПЕРАЦИЙ',
                    ha='center', va='center', transform=ax.transAxes, fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
            ax.set_title('ПОДОЗРИТЕЛЬНЫЕ ОПЕРАЦИИ', fontsize=12, fontweight='bold')

    def _plot_debit_vs_credit(self, ax):
        """Сравнение дебетовых и кредитовых операций"""
        type_stats = self.df.groupby('transaction_type').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)

        types = type_stats.index
        sums = type_stats[('amount', 'sum')]
        counts = type_stats[('amount', 'count')]

        x = np.arange(len(types))
        width = 0.35

        bars1 = ax.bar(x - width / 2, sums, width, label='Общая сумма', color=['red', 'green'])
        bars2 = ax.bar(x + width / 2, counts, width, label='Количество', color=['lightcoral', 'lightgreen'])

        ax.set_xlabel('Тип операции')
        ax.set_ylabel('Значения')
        ax.set_title(' ДЕБЕТ vs КРЕДИТ', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(types)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def _plot_category_boxplot(self, ax):
        """Boxplot сумм по категориям"""
        try:
            # Исключаем выбросы для лучшей визуализации
            filtered_df = self.df[self.df['amount'] < self.df['amount'].quantile(0.95)]

            sns.boxplot(data=filtered_df, x='category', y='amount', ax=ax)
            ax.set_title('РАСПРЕДЕЛЕНИЕ СУММ ПО КАТЕГОРИЯМ', fontsize=12, fontweight='bold')
            ax.set_xlabel('Категория')
            ax.set_ylabel('Сумма (руб)')
            ax.tick_params(axis='x', rotation=45)
        except Exception as e:
            ax.text(0.5, 0.5, f'Ошибка построения\nboxplot: {str(e)}',
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title( 'BOXPLOT', fontsize=12, fontweight='bold')

    def create_simple_report(self):
        print(" СОЗДАНИЕ УПРОЩЕННОГО ОТЧЕТА...")

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # 1. Категории
        category_stats = self.df['category'].value_counts()
        ax1.pie(category_stats.values, labels=category_stats.index, autopct='%1.1f%%')
        ax1.set_title('Распределение по категориям')

        # 2. Типы операций
        type_stats = self.df['transaction_type'].value_counts()
        ax2.bar(type_stats.index, type_stats.values, color=['red', 'green'])
        ax2.set_title('Типы операций')
        ax2.set_ylabel('Количество')

        # 3. Топ пользователи
        user_stats = self.df.groupby('user_id')['amount'].sum().nlargest(5)
        ax3.bar(range(len(user_stats)), user_stats.values, color='orange')
        ax3.set_title('Топ-5 пользователей по объему')
        ax3.set_ylabel('Сумма (руб)')
        ax3.set_xticks(range(len(user_stats)))
        ax3.set_xticklabels([f'User {uid}' for uid in user_stats.index])

        # 4. Распределение сумм
        ax4.hist(self.df['amount'], bins=50, alpha=0.7, color='purple', edgecolor='black')
        ax4.set_title('Распределение сумм транзакций')
        ax4.set_xlabel('Сумма (руб)')
        ax4.set_ylabel('Частота')

        plt.tight_layout()
        plt.savefig('data/simple_report.png', dpi=300, bbox_inches='tight')
        plt.show()


# Запуск визуализации
if __name__ == "__main__":
    print("ЗАПУСК ВИЗУАЛИЗАЦИИ ДАННЫХ...")

    try:
        visualizer = BankDataVisualizer()

        # Создаем упрощенный отчет сначала
        visualizer.create_simple_report()

        # Затем комплексный дашборд
        visualizer.create_comprehensive_dashboard()

        print(" ВИЗУАЛИЗАЦИЯ ЗАВЕРШЕНА!")
        print("Сохраненные файлы:")
        print("   - data/simple_report.png (простой отчет)")
        print("   - data/banking_dashboard.png (комплексный дашборд)")

    except Exception as e:
        print(f"Ошибка: {e}")
        print("Совет: Убедись, что файл data/transactions.csv существует")