import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from datetime import datetime
import sys
from decimal import Decimal
import getpass

# auth
from fitur.auth import login
from fitur.auth import register

# Akun
from fitur.akun import daftar_Tambah_Akun

# tabungan
from fitur.tabungan import daftar_Tambah_Tabungan

# pemasukan
from fitur.pemasukan import daftar_Pemasukan_Bph
from fitur.pemasukan import daftar_Pemasukan_Staff

# pengeluaran
from fitur.pengeluaran import daftar_Pengeluaran_Bph
from fitur.pengeluaran import daftar_Pengeluaran_Staff

# reservasi
from fitur.reservasi import read_reservasi_masjid
from fitur.reservasi import insert_reservasi_masjid
from fitur.reservasi import daftar_reservasi_Bph

# transaksi
from fitur.reservasi import read_data_transaksi


def connect():
    try:
        conn = None
        params = config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


################################### MENU AWAL ################################################
def main():
    os.system("cls")
    while True:
        namafile = "tampilan/login.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Masukkan opsi: ")
        if user_input == "1":
            username = input("Masukkan username: ")
            password = getpass.getpass("Masukkan password: ")
            login(username, password)
        elif user_input == "2":
            register()
        elif user_input == "3":
            sys.exit()
        else:
            print("Opsi tidak valid. Silahkan coba lagi.")


################################### MENU AWAL ################################################


################################### MENU BPH ################################################
def allfitur_Bph():
    os.system("cls")
    while True:
        namafile = "tampilan/allfitur_bph.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("pilih opsi: ")
        if user_input == "1":
            daftar_Pemasukan_Bph()
        elif user_input == "2":
            daftar_Pengeluaran_Bph()
        elif user_input == "3":
            daftar_reservasi_Bph()
        elif user_input == "4":
            daftar_Tambah_Tabungan()
        elif user_input == "5":
            daftar_Tambah_Akun()
        elif user_input == "6":
            sys.exit()
        elif user_input == "7":
            input_log = input("Apakah anda Yakin untuk Logout? (y/n) : ")
            if input_log == "y":
                main()
            elif input_log == "n":
                allfitur_Bph()
            else:
                print("Harap Masukkan input y/n")
                allfitur_Bph()
        else:
            print("Pilihan invalid")


################################### MENU BPH ################################################


################################### MENU STAFF ################################################
def allfitur_Staff():
    os.system("cls")
    while True:
        namafile = "tampilan/allfitur_staff.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("pilih opsi: ")
        if user_input == "1":
            daftar_Pemasukan_Staff()
        elif user_input == "2":
            daftar_Pengeluaran_Staff()
        elif user_input == "3":
            read_reservasi_masjid()
        elif user_input == "4":
            read_data_transaksi()
        elif user_input == "5":
            sys.exit()
        elif user_input == "6":
            input_log = input("Apakah anda Yakin untuk Logout? (y/n) : ")
            if input_log == "y":
                main()
            elif input_log == "n":
                allfitur_Staff()
            else:
                print("Harap Masukkan input y/n")
                allfitur_Staff()
        else:
            print("Pilihan invalid")


################################### MENU STAFF ################################################


################################### MENU JAMAAH ################################################
def allfitur_Jamaah():
    os.system("cls")
    while True:
        namafile = "tampilan/allfitur_jamaah.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("pilih opsi: ")
        if user_input == "1":
            read_reservasi_masjid()
        elif user_input == "2":
            insert_reservasi_masjid()
        elif user_input == "3":
            sys.exit()
        elif user_input == "4":
            input_log = input("Apakah anda Yakin untuk Logout? (y/n) : ")
            if input_log == "y":
                main()
            elif input_log == "n":
                allfitur_Jamaah()
            else:
                print("Harap Masukkan input y/n")
                allfitur_Jamaah()
        else:
            print("Pilihan invalid")


################################### MENU JAMAAH ################################################
if __name__ == "__main__":
    main()
