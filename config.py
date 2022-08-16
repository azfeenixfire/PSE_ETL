import snowflake.connector
import pandas as pd
import os
from snowflake.connector.pandas_tools import write_pandas


def query_snowflake(query, schema):
    conn = snowflake.connector.connect(
        # Secret: SNOWFLAKE_USER
        user=os.getenv('SNOWFLAKE_USER'),
        # Secret: SNOWFLAKE_PASSWORD
        password=os.getenv('SNOWFLAKE_PASSWORD'),

        account='strongmind',
        warehouse='DEVELOPMENT',
        database='researchdb',
        schema='ess'
    )
    cur = conn.cursor()
    try:
        cur.execute(query)
        df = cur.fetch_pandas_all()
    finally:
        cur.close()
    return df


def write_to_snowflake_with_trunc(changes_df, acnt, wrhs, db, schm, target_table):
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=acnt,
        warehouse=wrhs,
        database=db,
        schema=schm
    )
    sql_trunc = 'truncate table ' + db + '.' + schm + '.' + target_table

    try:
        #trunc table
        cur = conn.cursor()
        cur.execute(sql_trunc)
        # Write the data from the DataFrame to the table
        success, nchunks, nrows, _ = write_pandas(conn, changes_df, target_table)

    finally:
        conn.close()


def update_snowflake(query):
    conn = snowflake.connector.connect(
        # Secret: SNOWFLAKE_USER
        user=os.getenv('SNOWFLAKE_USER'),
        # Secret: SNOWFLAKE_PASSWORD
        password=os.getenv('SNOWFLAKE_PASSWORD'),

        account='strongmind',
        warehouse='DEVELOPMENT',
        database='researchdb',
        schema='ess'
    )
    cur = conn.cursor()
    try:
        cur.execute(query)
    finally:
        cur.close()