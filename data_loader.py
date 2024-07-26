import pandas as pd
import psycopg2
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Подключение к PostgreSQL
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="my_postgres_container"
    )
    cursor = conn.cursor()
    logging.info("Connected to the database.")

    # Загрузка данных из CSV
    data = pd.read_csv('IMOEX_230101_240601.csv', delimiter=';')
    logging.info("CSV file loaded successfully.")

    # Вывод структуры данных
    logging.info(f"Data columns: {data.columns}")

    # Преобразование формата даты и времени
    data['DATE'] = pd.to_datetime(data['<DATE>'], format='%y%m%d').dt.date

    # Вставка данных в таблицу
    for index, row in data.iterrows():
        cursor.execute(
            "INSERT INTO stock_data (ticker, period, trade_date, trade_time, open_price, high_price, low_price, close_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (row['<TICKER>'], row['<PER>'], row['DATE'], int(row['<TIME>']), row['<OPEN>'], row['<HIGH>'], row['<LOW>'],
             row['<CLOSE>'], row['<VOL>'])
        )
    conn.commit()
    logging.info("Data loaded into the database successfully.")
except Exception as e:
    logging.error(f"Error occurred: {e}")
finally:
    cursor.close()
    conn.close()
    logging.info("Database connection closed.")
