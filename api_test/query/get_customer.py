from connection import PostgresDBManager
import json

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_customer():
    query = "SELECT * FROM customer.mst_customer limit 10"
    with PostgresDBManager(query,None,False) as cursor:
        data= dictfetchall(cursor)
        return data