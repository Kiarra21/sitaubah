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


################################### LOGIN ################################################
