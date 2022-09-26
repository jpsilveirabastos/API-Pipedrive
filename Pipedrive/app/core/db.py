from .config import DBNAME, USER, PASSWORD, HOST
import psycopg2

class Db:

    def connect():
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST)
        cur = conn.cursor()
        return cur,conn

    def disconnect(cur, conn):
        cur.close()
        conn.close()

    def tables():
        pipedrive_m = 'pipedrive_metrics'
        return pipedrive_m
