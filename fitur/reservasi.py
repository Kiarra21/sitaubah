import os
import psycopg2
import pandas as pd
from tabulate import tabulate
from config import config


################################### MENU RESERVASI DAN TRANSKASI ################################################
def daftar_Tansaksi_Bph():
    os.system("cls")

    while True:
        read_data_transaksi()
        namafile = "tampilan/spesial_menu_transaksi.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            update_transaksi()
        elif user_input == "2":
            daftar_reservasi_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def daftar_reservasi_Bph():
    from main import allfitur_Bph

    os.system("cls")

    while True:
        read_reservasi_masjid_khusus_bph()
        namafile = "tampilan/spesial_menu_reservasi.txt"
        with open(namafile, "r") as file:
            isi_file = file.read()
            print(isi_file)

        user_input = input("Pilih opsi: ")
        if user_input == "1":
            insert_reservasi_masjid()
        elif user_input == "2":
            update_reservasi_masjid()
        elif user_input == "3":
            delete_reservasi_masjid()
        elif user_input == "4":
            daftar_Tansaksi_Bph()
        elif user_input == "5":
            allfitur_Bph()
        else:
            print("Opsi Tidak valid")
            input("Tekan Enter untuk lanjut...")


def read_reservasi_masjid():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        sql = """
            SELECT 
                rm.Id_Reservasi,
                rm.Tanggal_Reservasi,
                rm.Id_Akun,
                a.Username AS Nama_Akun,
                rm.Id_Lokasi,
                l.Nama_Lokasi,
                l.Harga_Lokasi
            FROM Reservasi_Masjid rm
            JOIN Akun a ON rm.Id_Akun = a.Id_Akun
            JOIN Lokasi l ON rm.Id_Lokasi = l.Id_Lokasi
            ORDER BY rm.Id_Reservasi ASC
        """
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        df["harga_lokasi"] = df["harga_lokasi"].astype(float).astype(int)

        print(tabulate(df, headers="keys", tablefmt="grid"))

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Reservasi_Masjid: {error}")
    finally:
        if conn is not None:
            conn.close()

    input("\nTekan Enter untuk kembali ke menu...")
    os.system("cls")


def read_reservasi_masjid_khusus_bph():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        sql = """
            SELECT 
                rm.Id_Reservasi,
                rm.Tanggal_Reservasi,
                rm.Id_Akun,
                a.Username AS Nama_Akun,
                rm.Id_Lokasi,
                l.Nama_Lokasi,
                l.Harga_Lokasi
            FROM Reservasi_Masjid rm
            JOIN Akun a ON rm.Id_Akun = a.Id_Akun
            JOIN Lokasi l ON rm.Id_Lokasi = l.Id_Lokasi
            ORDER BY rm.Id_Reservasi ASC
        """
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        df["harga_lokasi"] = df["harga_lokasi"].astype(float).astype(int)

        print(tabulate(df, headers="keys", tablefmt="grid"))

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Reservasi_Masjid: {error}")
    finally:
        if conn is not None:
            conn.close()


def insert_reservasi_masjid():
    from fitur.akun import read_data_akun_jamaah
    from fitur.status_lokasi import read_data_lokasi

    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        read_data_akun_jamaah()
        id_akun = int(input("Masukkan ID Akun yang Mengajukan: "))
        read_data_lokasi()
        id_lokasi = int(input("Masukkan ID Lokasi: "))
        tanggal_reservasi = input("Masukkan Tanggal Reservasi (YYYY-MM-DD HH:MM): ")

        sql_reservasi = """
        INSERT INTO Reservasi_Masjid (Tanggal_Reservasi, Id_Akun, Id_Lokasi)
        VALUES (%s, %s, %s)
        RETURNING Id_Reservasi
        """
        cur = conn.cursor()
        cur.execute(sql_reservasi, (tanggal_reservasi, id_akun, id_lokasi))
        id_reservasi_baru = cur.fetchone()[0]

        sql_transaksi = """
        INSERT INTO Transaksi (Id_Reservasi)
        VALUES (%s)
        """
        cur.execute(sql_transaksi, (id_reservasi_baru,))

        conn.commit()
        cur.close()
        print(
            f"Reservasi berhasil dibuat dengan ID {id_reservasi_baru} dan transaksi otomatis dibuat."
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membuat reservasi: {error}")
    finally:
        if conn is not None:
            conn.close()


def update_reservasi_masjid():
    from fitur.status_lokasi import read_data_lokasi

    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        read_reservasi_masjid_khusus_bph()
        id_reservasi = int(input("Masukkan ID Reservasi yang ingin diupdate: "))
        tanggal_baru = input("Masukkan Tanggal Baru (YYYY-MM-DD HH:MM): ")
        read_data_lokasi()
        id_lokasi_baru = int(input("Masukkan ID Lokasi Baru: "))

        sql = """
        UPDATE Reservasi_Masjid
        SET Tanggal_Reservasi = %s, Id_Lokasi = %s
        WHERE Id_Reservasi = %s
        """
        cur = conn.cursor()
        cur.execute(sql, (tanggal_baru, id_lokasi_baru, id_reservasi))
        conn.commit()
        cur.close()
        print("Reservasi berhasil diperbarui.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat memperbarui reservasi: {error}")
    finally:
        if conn is not None:
            conn.close()


def delete_reservasi_masjid():
    os.system("cls")
    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        read_reservasi_masjid_khusus_bph()
        id_reservasi = int(input("Masukkan ID Reservasi yang ingin dihapus: "))

        sql_delete_transaksi = "DELETE FROM Transaksi WHERE Id_Reservasi = %s"
        sql_delete_reservasi = "DELETE FROM Reservasi_Masjid WHERE Id_Reservasi = %s"

        cur = conn.cursor()
        cur.execute(sql_delete_transaksi, (id_reservasi,))
        cur.execute(sql_delete_reservasi, (id_reservasi,))
        conn.commit()
        cur.close()
        print("Reservasi dan transaksi terkait berhasil dihapus.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat menghapus reservasi: {error}")
    finally:
        if conn is not None:
            conn.close()


def read_data_transaksi():

    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        sql = """
        SELECT 
            t.Id_Transaksi,
            t.Id_Reservasi,
            r.Tanggal_Reservasi,
            t.Id_Akun as akun_staff,
            a.Username,
            t.Tanggal_Pembayaran,
            t.Id_Tabungan,
            tb.Nama_Tabungan,
            t.Id_Status,
            sp.Jenis_Status
        FROM Transaksi t
        JOIN Reservasi_Masjid r ON t.Id_Reservasi = r.Id_Reservasi
        LEFT JOIN Akun a ON t.Id_Akun = a.Id_Akun
        LEFT JOIN Tabungan_Masjid tb ON t.Id_Tabungan = tb.Id_Tabungan
        LEFT JOIN Status_Pembayaran sp ON t.Id_Status = sp.Id_Status
        ORDER BY t.Id_Transaksi ASC
        """

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql_query(sql, conn)

        print(tabulate(df, headers="keys", tablefmt="grid"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat membaca data Transaksi: {error}")
    finally:
        if conn is not None:
            conn.close()


def update_transaksi():
    from fitur.akun import read_data_akun_staff
    from fitur.tabungan import read_data_tabungan
    from fitur.status_lokasi import read_data_status_pembayaran

    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)

        id_transaksi = int(input("Masukkan ID Transaksi yang ingin diedit: "))

        print("Masukkan nilai baru (kosongkan jika tidak ingin mengubah):")
        read_data_akun_staff()
        id_akun = input("Masukkan Staff Penanggungjawab: ")
        tanggal_pembayaran = input("Tanggal Pembayaran (YYYY-MM-DD HH:MM): ")
        read_data_tabungan()
        id_tabungan = input("ID Tabungan: ")
        read_data_status_pembayaran()
        id_status = input("ID Status Pembayaran: ")

        cur = conn.cursor()
        cur.execute("SELECT * FROM Transaksi WHERE Id_Transaksi = %s", (id_transaksi,))
        data_lama = cur.fetchone()

        if data_lama is None:
            print("Data transaksi tidak ditemukan.")
            input("Klik enter untuk mengulang...")
            os.system("cls")
            return

        sql = """
        UPDATE Transaksi
        SET Id_Akun = %s,
            Tanggal_Pembayaran = %s,
            Id_Tabungan = %s,
            Id_Status = %s
        WHERE Id_Transaksi = %s
        """

        cur.execute(
            sql,
            (
                int(id_akun) if id_akun.strip() else data_lama[2],
                tanggal_pembayaran if tanggal_pembayaran.strip() else data_lama[3],
                int(id_tabungan) if id_tabungan.strip() else data_lama[4],
                int(id_status) if id_status.strip() else data_lama[5],
                id_transaksi,
            ),
        )

        conn.commit()
        cur.close()
        print("Transaksi berhasil diperbarui.")
    except (Exception, psycopg2.DatabaseError, ValueError) as error:
        print(f"Error saat mengedit transaksi: {error}")
        input("Klik enter untuk mengulang...")
        os.system("cls")
    finally:
        if conn is not None:
            conn.close()


################################### MENU RESERVASI DAN TRANSKASI ################################################
