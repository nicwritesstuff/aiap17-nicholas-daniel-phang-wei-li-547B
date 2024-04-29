import sqlite3
import pandas as pd

#directory_str = 'data/calls.db'

def connectToDataBase(directory_str):

    conn = sqlite3.connect(directory_str)
    query = "SELECT * FROM calls"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df