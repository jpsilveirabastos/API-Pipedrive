from .config import DBNAME, USER, PASSWORD, HOST
import psycopg2


class Db:

    def connect():
        '''Connect to Postgres'''
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST)
        cur = conn.cursor()
        return cur,conn

    def disconnect(cur, conn):
        '''Disconnect to Postgres'''
        cur.close()
        conn.close()

    def tables():
        '''Table used to save the data'''
        pipedrive_m = 'pipedrive_metrics'
        return pipedrive_m
