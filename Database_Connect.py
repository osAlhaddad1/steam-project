import psycopg2

connection_string = "host='20.162.218.244' dbname='steamdatabase' user='postgres' password='Diana112????'"

conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

query = """INSERT INTO Klant (klantnr, gebruikersnaam, wachtwoord) 
           VALUES (001, 'lotfi', 'password');"""

cursor.execute(query)

conn.commit()
conn.close()

