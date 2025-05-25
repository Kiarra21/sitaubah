import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from datetime import datetime
import sys
from decimal import Decimal
import getpass


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
            sys.exit()
        else:
            print("Opsi tidak valid. Silahkan coba lagi.")


################################### MENU AWAL ################################################


################################### LOGIN ################################################
def login(username, password):
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        sql = "SELECT * FROM akun WHERE username = %s AND password = %s"
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        user = cur.fetchone()

        if user:
            id_role = user[3]

            if id_role == 1:
                print("Selamat datang BPH")
                allfitur_Bph()
            elif id_role == 2:
                print("Selamat datang Staff")
                allfitur_Staff()
            elif id_role == 3:
                print("Selamat datang Jamaah")
                allfitur_Jamaah()
            else:
                print("Role tidak valid")
        else:
            print("Login gagal, username atau password salah")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


################################### LOGIN ################################################


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
            print("?")
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
            print("?")
        elif user_input == "4":
            sys.exit()
        elif user_input == "5":
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
            print("?")
        elif user_input == "2":
            print("?")
        elif user_input == "3":
            sys.exit()
        elif user_input == "4":
            input_log = input("Apakah anda Yakin untuk Logout? (y/n) : ")
            if input_log == "y":
                main()
            elif input_log == "n":
                allfitur_Staff()
            else:
                print("Harap Masukkan input y/n")
                allfitur_Jamaah()
        else:
            print("Pilihan invalid")


################################### JAMAAH ################################################


################################### MENU CRUD AKUN + FUNGSI + READ ROLE(BPH) ################################################
def daftar_Tambah_Akun():
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


################################### MENU PEMASUKAN + FUNGSI DETAIL PEMASUKAN (BPH dan staff) ################################################
def daftar_Pemasukan_Bph():
    os.system("cls")
    while True:
        namafile = "tampilan/spesial_menu_pemasukan.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            read_data_pemasukan()
        elif user_input == "2":
            add_pemasukan_and_detail()
        elif user_input == "3":
            read_data_detail_pemasukan()
        elif user_input == "4":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def daftar_Pemasukan_Staff():
    os.system("cls")
    while True:
        namafile = "tampilan/spesial_menu_pemasukan.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            read_data_pemasukan()
        elif user_input == "2":
            add_pemasukan_and_detail()
        elif user_input == "3":
            read_data_detail_pemasukan()
        elif user_input == "4":
            allfitur_Staff()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def read_data_pemasukan():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Pemasukan ORDER BY Id_Pemasukan ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Pemasukan: {error}")
    finally:
        if conn is not None:
            conn.close()
    input("\nTekan Enter untuk kembali...")
    os.system("cls")


def insert_data_pemasukan(id_akun):
    os.system("cls")
    try:
        conn = psycopg2.connect(**config())
        sql = """
        INSERT INTO Pemasukan (Tanggal, Id_Akun)
        VALUES (CURRENT_TIMESTAMP, %s)
        RETURNING Id_Pemasukan
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_akun,))
                result = cur.fetchone()
                if result:
                    new_id = result[0]
                    print(f"Data pemasukan berhasil ditambahkan dengan id: {new_id}.")
                    return new_id
                else:
                    print("Gagal mendapatkan ID pemasukan.")
                    return None
    except Exception as error:
        print(f"Error: {error}")
        return None
    finally:
        if conn:
            conn.close()


def read_data_detail_pemasukan():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Detail_Pemasukan ORDER BY Id_Detail_Pemasukan ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Detail_Pemasukan: {error}")
    finally:
        if conn is not None:
            conn.close()
    input("\nTekan Enter untuk kembali...")
    os.system("cls")


def insert_data_detail_pemasukan(
    id_pemasukan, id_jenis_pemasukan, nominal, keterangan, id_tabungan
):
    try:
        conn = psycopg2.connect(**config())
        sql = """
        INSERT INTO Detail_Pemasukan (Id_Pemasukan, Id_Jenis_Pemasukan, Nominal, Keterangan, Id_Tabungan)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING Id_Detail_Pemasukan
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        id_pemasukan,
                        id_jenis_pemasukan,
                        nominal,
                        keterangan or None,
                        id_tabungan,
                    ),
                )
                result = cur.fetchone()
                if result:
                    print(
                        f"Data detail pemasukan berhasil ditambahkan dengan id: {result[0]}"
                    )
                else:
                    print("Gagal menambahkan detail pemasukan.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()


def add_pemasukan_and_detail():
    os.system("cls")
    try:
        read_data_akun()
        id_akun = int(input("Masukkan ID Akun: "))
        id_pemasukan_baru = insert_data_pemasukan(id_akun)

        if id_pemasukan_baru:
            while True:
                try:
                    read_data_jenis_pemasukan()
                    id_jenis_pemasukan = int(input("Masukkan ID Jenis Pemasukan: "))
                    nominal = Decimal(input("Masukkan Nominal: "))
                    keterangan = input("Masukkan Keterangan (boleh kosong): ")
                    read_data_tabungan()
                    id_tabungan = int(input("Masukkan ID Tabungan: "))

                    insert_data_detail_pemasukan(
                        id_pemasukan_baru,
                        id_jenis_pemasukan,
                        nominal,
                        keterangan,
                        id_tabungan,
                    )

                    tambah_lagi = input("Tambah detail lagi? (y/n): ").lower()
                    if tambah_lagi != "y":
                        break
                except ValueError:
                    print("Input angka tidak valid. Ulangi.")
        else:
            print("Gagal menambahkan data pemasukan.")
    except ValueError:
        print("Input tidak valid. Pastikan semua angka diisi dengan benar.")
    except Exception as error:
        print(f"Terjadi kesalahan: {error}")
    input("\nTekan Enter untuk kembali ke menu...")
    os.system("cls")


def read_data_jenis_pemasukan():
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Jenis_Pemasukan ORDER BY Id_Jenis_Pemasukan ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Jenis_Pemasukan: {error}")
    finally:
        if conn is not None:
            conn.close()


################################### MENU PEMASUKAN + FUNGSI DETAIL PEMASUKAN (BPH dan staff) ################################################


################################### MENU PENGELUARAN + FUNGSI DETAIL PENGELUARAN (BPH dan staff) ################################################
def daftar_Pengeluaran_Bph():
    os.system("cls")
    while True:
        namafile = "tampilan/spesial_menu_pengeluaran.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            read_data_pengeluaran()
        elif user_input == "2":
            add_pengeluaran_and_detail()
        elif user_input == "3":
            read_data_detail_pengeluaran()
        elif user_input == "4":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def daftar_Pengeluaran_Staff():
    os.system("cls")
    while True:
        namafile = "tampilan/spesial_menu_pengeluaran.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            read_data_pengeluaran()
        elif user_input == "2":
            add_pengeluaran_and_detail()
        elif user_input == "3":
            read_data_detail_pengeluaran()
        elif user_input == "4":
            allfitur_Staff()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def read_data_pengeluaran():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Pengeluaran ORDER BY Id_Pengeluaran ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Pengeluaran: {error}")
    finally:
        if conn is not None:
            conn.close()
    input("\nTekan Enter untuk kembali...")
    os.system("cls")


def read_data_detail_pengeluaran():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Detail_Pengeluaran ORDER BY Id_Detail_Pengeluaran ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Detail_Pengeluaran: {error}")
    finally:
        if conn is not None:
            conn.close()
    input("\nTekan Enter untuk kembali...")
    os.system("cls")


def insert_data_pengeluaran(id_akun):
    os.system("cls")
    try:
        conn = psycopg2.connect(**config())
        sql = """
        INSERT INTO Pengeluaran (Tanggal, Id_Akun)
        VALUES (CURRENT_TIMESTAMP, %s)
        RETURNING Id_Pengeluaran
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_akun,))
                result = cur.fetchone()
                if result:
                    new_id = result[0]
                    print(f"Data pengeluaran berhasil ditambahkan dengan id: {new_id}.")
                    return new_id
                else:
                    print("Gagal mendapatkan ID pengeluaran.")
                    return None
    except Exception as error:
        print(f"Error: {error}")
        return None
    finally:
        if conn:
            conn.close()


def insert_data_detail_pengeluaran(
    id_pengeluaran, id_jenis_pengeluaran, nominal, keterangan, id_tabungan
):
    try:
        conn = psycopg2.connect(**config())
        sql = """
        INSERT INTO Detail_Pengeluaran (Id_Pengeluaran, Id_Jenis_Pengeluaran, Nominal, Keterangan, Id_Tabungan)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING Id_Detail_Pengeluaran
        """
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        id_pengeluaran,
                        id_jenis_pengeluaran,
                        nominal,
                        keterangan or None,
                        id_tabungan,
                    ),
                )
                result = cur.fetchone()
                if result:
                    print(
                        f"Data detail pengeluaran berhasil ditambahkan dengan id: {result[0]}"
                    )
                else:
                    print("Gagal menambahkan detail pengeluaran.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()


def add_pengeluaran_and_detail():
    os.system("cls")
    try:
        read_data_akun()
        id_akun = int(input("Masukkan ID Akun: "))
        id_pengeluaran_baru = insert_data_pengeluaran(id_akun)

        if id_pengeluaran_baru:
            while True:
                try:
                    read_data_jenis_pengeluaran()
                    id_jenis_pengeluaran = int(input("Masukkan ID Jenis Pengeluaran: "))
                    nominal = Decimal(input("Masukkan Nominal: "))
                    keterangan = input("Masukkan Keterangan (boleh kosong): ")
                    read_data_tabungan()
                    id_tabungan = int(input("Masukkan ID Tabungan: "))

                    insert_data_detail_pengeluaran(
                        id_pengeluaran_baru,
                        id_jenis_pengeluaran,
                        nominal,
                        keterangan,
                        id_tabungan,
                    )

                    tambah_lagi = input("Tambah detail lagi? (y/n): ").lower()
                    if tambah_lagi != "y":
                        break
                except ValueError:
                    print("Input angka tidak valid. Ulangi.")
        else:
            print("Gagal menambahkan data pengeluaran.")
    except ValueError:
        print("Input tidak valid. Pastikan semua angka diisi dengan benar.")
    except Exception as error:
        print(f"Terjadi kesalahan: {error}")
    input("\nTekan Enter untuk kembali ke menu...")
    os.system("cls")


def read_data_jenis_pengeluaran():
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        sql = "SELECT * FROM Jenis_Pengeluaran ORDER BY Id_Jenis_Pengeluaran ASC"

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Jenis_Pengeluaran: {error}")
    finally:
        if conn is not None:
            conn.close()


################################### MENU PENGELUARAN + FUNGSI DETAIL PENGELUARAN (BPH dan staff) ################################################


################################### MENU TABUNGAN (BPH) ################################################
def daftar_Tambah_Tabungan():
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
                saldo_tabungan = f"{row[2]:,.0f}"  # Format langsung di sini 👈
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

if __name__ == "__main__":
    main()
