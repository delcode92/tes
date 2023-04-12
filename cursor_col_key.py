import psycopg2

try:
    conn = psycopg2.connect(
        database="parkir", user="Admin", password="", host="127.0.0.1", port= "5432"
    )
    conn.autocommit = True
    db_cursor = conn.cursor()

    q = "select * from tarif;"

    db_cursor.execute(q)

    # data = db_cursor.description()
    colnames = [desc[0] for desc in db_cursor.description]
    # name_idx = colnames.index('rules')

    print(colnames)

    
    # column_names = [row[0] for row in data]

    # print the column names
    # print(data)


    # for row in data:
    #     # Access the values by column name
    #     # print(type(row))
    #     print(row[0])

except Exception as e:
    print(str(e))