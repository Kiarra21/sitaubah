import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from decimal import Decimal


################################### MENU TABUNGAN (BPH) ################################################
def daftar_Tambah_Tabungan():
    from main import allfitur_Bph

    os.system("cls")
    while True:
        read_data_tabungan()
        namafile = "tampilan/all_menu_crud.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            insert_data_tabungan()
        elif user_input == "2":
            update_data_tabungan()
        elif user_input == "3":
            delete_data_tabungan()
        elif user_input == "4":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")


def read_data_tabungan():
    os.system("cls")
    try:
        conn = psycopg2.connect(**config())
        sql = "SELECT * FROM Tabungan_Masjid ORDER BY Id_Tabungan ASC"

        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            print("+----+---------------+-----------------+------------------+")
            print("| No | Id_Tabungan   | Nama_Tabungan   | Saldo_Tabungan   |")
            print("+====+===============+=================+==================+")
            for i, row in enumerate(rows):
                id_tabungan = row[0]
                nama_tabungan = row[1]
                saldo_tabungan = f"{row[2]:,.0f}"
                print(
                    f"| {i:<2} | {id_tabungan:<13} | {nama_tabungan:<15} | {saldo_tabungan:<16} |"
                )
            print("+----+---------------+-----------------+------------------+")
    except Exception as e:
        print(f"Error saat membaca data Tabungan_Masjid: {e}")
    finally:
        if conn:
            conn.close()


def insert_data_tabungan():
    os.system("cls")
    try:
        from decimal import Decimal, InvalidOperation
        import traceback

        conn = psycopg2.connect(**config())

        nama_tabungan = input("Inputkan Nama Tabungan: ").strip()
        saldo_input = input("Inputkan Saldo Awal Tabungan: ").strip()

        try:
            saldo_tabungan = Decimal(saldo_input)
        except InvalidOperation:
            print("Saldo tidak valid. Harus berupa angka.")
            return

        print(f"DEBUG: Nama = {nama_tabungan}, Saldo = {saldo_tabungan}")

        sql = """
        INSERT INTO Tabungan_Masjid (Nama_Tabungan, Saldo_Tabungan)
        VALUES (%s, %s)
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nama_tabungan, saldo_tabungan))
                print("Data tabungan berhasil ditambahkan.")
    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
    finally:
        if conn:
            conn.close()


def update_data_tabungan():
    os.system("cls")
    try:
        conn = psycopg2.connect(**config())

        read_data_tabungan()
        id_tabungan = int(input("Inputkan ID Tabungan yang ingin diubah: "))
        nama_tabungan = input("Masukkan Nama Tabungan Baru: ")
        saldo_tabungan = Decimal(input("Masukkan Saldo Baru: "))

        sql = """
        UPDATE Tabungan_Masjid
        SET Nama_Tabungan = %s, Saldo_Tabungan = %s
        WHERE Id_Tabungan = %s
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nama_tabungan, saldo_tabungan, id_tabungan))
                print("Data tabungan berhasil diperbarui.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()


def delete_data_tabungan():
    os.system("cls")
    try:
        conn = psycopg2.connect(**config())

        read_data_tabungan()
        id_tabungan = int(input("Masukkan ID Tabungan yang ingin dihapus: "))

        sql = "DELETE FROM Tabungan_Masjid WHERE Id_Tabungan = %s"
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_tabungan,))
                print("Data tabungan berhasil dihapus.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()


################################### MENU TABUNGAN (BPH) ################################################
