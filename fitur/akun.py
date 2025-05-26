import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from datetime import datetime
import sys
from decimal import Decimal
import getpass


################################### MENU CRUD AKUN + FUNGSI + READ ROLE(BPH) ################################################
def daftar_Tambah_Akun():
    from main import allfitur_Bph

    os.system("cls")
    while True:
        read_data_akun()
        namafile = "tampilan/all_menu_crud.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            insert_data_akun()
        elif user_input == "2":
            update_data_akun()
        elif user_input == "3":
            delete_data_akun()
        elif user_input == "4":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")


def read_data_akun():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Akun ORDER BY Id_Akun ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_data_akun_jamaah():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = """
        SELECT Id_Akun, Username
        FROM Akun
        WHERE Id_Role = 3
        ORDER BY Id_Akun ASC
        """

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data akun jamaah: {error}")
    finally:
        if conn is not None:
            conn.close()


def read_data_akun_staff():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = """
        SELECT Id_Akun, Username
        FROM Akun
        WHERE Id_Role = 2
        ORDER BY Id_Akun ASC
        """

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data akun jamaah: {error}")
    finally:
        if conn is not None:
            conn.close()


def update_data_akun():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        read_data_akun()
        id_akun = input("Inputkan id akun yang ingin diedit: ")
        username = input("Inputkan Username Baru: ")
        password = input("Inputkan Password Baru: ")
        read_data_role()
        id_role = int(input("Inputkan Id Role Baru: "))

        sql = """
        UPDATE Akun
        SET Username = %s, Password = %s, Id_Role = %s
        WHERE Id_Akun = %s
        """
        cur = conn.cursor()
        cur.execute(sql, (username, password, id_role, id_akun))
        conn.commit()
        cur.close()
        print("Data berhasil diupdate pada tabel Akun.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_data_akun():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(Id_Akun), 0) FROM Akun")
        max_id = cur.fetchone()[0]
        new_id = max_id + 1

        username = input("Inputkan Username: ")
        password = input("Inputkan Password: ")
        id_role = int(input("inputkan Id Role: "))

        sql = """
        INSERT INTO Akun (Id_Akun, Username, Password, Id_Role)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (new_id, username, password, id_role))
        conn.commit()
        cur.close()
        print(f"Data akun berhasil ditambahkan dengan id: {new_id}.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()


def delete_data_akun():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        read_data_akun()
        id_akun = input("Inputkan Id Akun Yang Ingin Dihapus: ")

        sql = "DELETE FROM Akun WHERE Id_Akun = %s"
        cur = conn.cursor()
        cur.execute(sql, (id_akun,))
        conn.commit()
        cur.close()
        print("Data berhasil dihapus dari tabel Akun.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_data_role():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Role ORDER BY Id_Role ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Terjadi kesalahan saat membaca data Role: {error}")
    finally:
        if conn is not None:
            conn.close()


################################### MENU CRUD AKUN + FUNGSI + READ ROLE(BPH) ################################################
