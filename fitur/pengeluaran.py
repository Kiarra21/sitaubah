import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config
from decimal import Decimal


################################### MENU PENGELUARAN + FUNGSI DETAIL PENGELUARAN (BPH dan staff) ################################################
def daftar_Pengeluaran_Bph():
    from main import allfitur_Bph

    os.system("cls")
    while True:
        read_data_pengeluaran()
        namafile = "tampilan/spesial_menu_pengeluaran.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            add_pengeluaran_and_detail()
        elif user_input == "2":
            read_data_detail_pengeluaran()
        elif user_input == "3":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def daftar_Pengeluaran_Staff():
    from main import allfitur_Staff

    os.system("cls")
    while True:
        read_data_pengeluaran()
        namafile = "tampilan/spesial_menu_pengeluaran.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            add_pengeluaran_and_detail()
        elif user_input == "2":
            read_data_detail_pengeluaran()
        elif user_input == "3":
            allfitur_Staff()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def read_data_pengeluaran():
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
            p.Id_Pengeluaran,
            p.Id_Akun,
            a.Username,
            p.Tanggal
        FROM Pengeluaran p
        JOIN Akun a ON p.Id_Akun = a.Id_Akun
        ORDER BY p.Id_Pengeluaran ASC
        """

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


def read_data_detail_pengeluaran():
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
            dp.Id_Detail_Pengeluaran,
            dp.Id_Pengeluaran,
            dp.Id_Jenis_Pengeluaran,
            jp.Nama_Jenis_Pengeluaran,
            dp.Nominal,
            dp.Keterangan,
            dp.Id_Tabungan,
            tm.Nama_Tabungan
        FROM Detail_Pengeluaran dp
        JOIN Jenis_Pengeluaran jp ON dp.Id_Jenis_Pengeluaran = jp.Id_Jenis_Pengeluaran
        JOIN Tabungan_Masjid tm ON dp.Id_Tabungan = tm.Id_Tabungan
        ORDER BY dp.Id_Detail_Pengeluaran ASC
        """

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        if "Nominal" in df.columns:
            df["Nominal"] = df["Nominal"].fillna(0).astype(float).astype(int)

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
    from fitur.akun import read_data_akun
    from fitur.tabungan import read_data_tabungan

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
