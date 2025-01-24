from database import get_db_connection, create_tables, insert_data

conn = get_db_connection()
create_tables(conn)

with open('whitelist.txt', 'r') as file:
    for line in file:
        user_id = line.strip() 
        insert_data(conn, user_id)

conn.close()