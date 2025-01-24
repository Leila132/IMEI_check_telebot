from database import get_db_connection, create_tables, insert_data

conn = get_db_connection()
create_tables(conn)

insert_data(conn, "1")
conn.close()