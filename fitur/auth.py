import os
import psycopg2
from config import config


################################### LOGIN ################################################
def login(username, password):
    from main import allfitur_Bph
    from main import allfitur_Staff
    from main import allfitur_Jamaah

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


def register():
    import os
    import psycopg2
    from config import config

    os.system("cls")
    print("=== Registrasi Akun ===")

    username = input("Masukkan Username: ").strip()
    password = input("Masukkan Password: ").strip()

    if not username or not password:
        print("Username dan password tidak boleh kosong.")
        return

    try:
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * FROM akun WHERE username = %s", (username,))
        if cur.fetchone():
            print("Username sudah digunakan. Coba yang lain.")
        else:
            sql = "INSERT INTO akun (username, password, id_role) VALUES (%s, %s, %s)"
            cur.execute(sql, (username, password, 3))
            conn.commit()
            print("Registrasi berhasil! Akun Jamaah telah dibuat.")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saat registrasi: {error}")
    finally:
        if conn is not None:
            conn.close()


################################### LOGIN ################################################
