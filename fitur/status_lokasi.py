import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config


################################### READ DATA STATUS PEMBAYARAN DAN LOKASI ################################################
def read_data_status_pembayaran():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Status_Pembayaran ORDER BY Id_Status ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Status_Pembayaran: {error}")
    finally:
        if conn is not None:
            conn.close()


def read_data_lokasi():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Lokasi ORDER BY Id_Lokasi ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Lokasi: {error}")
    finally:
        if conn is not None:
            conn.close()


################################### READ DATA STATUS PEMBAYARAN DAN sLOKASI ################################################
