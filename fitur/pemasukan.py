import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from decimal import Decimal


################################### MENU PEMASUKAN + FUNGSI DETAIL PEMASUKAN (BPH dan staff) ################################################
def daftar_Pemasukan_Bph():
    from main import allfitur_Bph

    os.system("cls")
    while True:
        read_data_pemasukan()
        namafile = "tampilan/spesial_menu_pemasukan.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            add_pemasukan_and_detail()
        elif user_input == "2":
            read_data_detail_pemasukan()
        elif user_input == "3":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def daftar_Pemasukan_Staff():
    from main import allfitur_Staff

    os.system("cls")
    while True:
        read_data_pemasukan()
        namafile = "tampilan/spesial_menu_pemasukan.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            add_pemasukan_and_detail()
        elif user_input == "2":
            read_data_detail_pemasukan()
        elif user_input == "3":
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

        sql = """
        SELECT 
            p.Id_Pemasukan,
            p.Id_Akun,
            a.Username,
            p.Tanggal
        FROM Pemasukan p
        JOIN Akun a ON p.Id_Akun = a.Id_Akun
        ORDER BY p.Id_Pemasukan ASC
        """

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
    import os
    import psycopg2
    import pandas as pd
    from tabulate import tabulate
    from config import config

    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        sql = """
        SELECT 
            dp.Id_Detail_Pemasukan,
            dp.Id_Pemasukan,
            dp.Id_Jenis_Pemasukan,
            jp.Nama_Jenis_Pemasukan,
            dp.Nominal,
            dp.Keterangan,
            dp.Id_Tabungan,
            tm.Nama_Tabungan
        FROM Detail_Pemasukan dp
        JOIN Jenis_Pemasukan jp ON dp.Id_Jenis_Pemasukan = jp.Id_Jenis_Pemasukan
        JOIN Tabungan_Masjid tm ON dp.Id_Tabungan = tm.Id_Tabungan
        ORDER BY dp.Id_Detail_Pemasukan ASC
        """

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        # Cek apakah kolom "Nominal" ada sebelum mengubah tipe datanya
        if "Nominal" in df.columns:
            df["Nominal"] = df["Nominal"].fillna(0).astype(float).astype(int)

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
    from fitur.akun import read_data_akun
    from fitur.tabungan import read_data_tabungan

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
