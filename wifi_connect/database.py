import micropg

# Databaseconfiguratie
DB_HOST = "20.162.218.244"  # IP-adres van de database-server
DB_PORT = 5432            # Standaard PostgreSQL-poort
DB_USER = "postgres"  # Databasegebruikersnaam
DB_PASSWORD = "Diana112????"  # Wachtwoord van de gebruiker
DB_NAME = "steamdatabase"  # Naam van de database

# Verbinden met PostgreSQL
def connect_database():
    try:
        conn = micropg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Verbinding met de database is gelukt!")
        return conn
    except Exception as e:
        print("Fout bij het verbinden met de database:", e)
        return None

    conn = connect_database()
    INSERT
    INTO
    test_tabel(naam, leeftijd)
    VALUES('Diana', 22);


# Query uitvoeren
def execute_query(conn, query):
    try:
        cursor = conn.cursor()  # Maak een cursor aan
        cursor.execute(query)   # Voer de query uit
        results = cursor.fetchall()  # Haal alle resultaten op
        for row in results:
            print(row)  # Print de rijen
    except Exception as e:
        print("Fout bij het uitvoeren van de query:", e)
    finally:
        cursor.close()  # Sluit de cursor


# # Start het programma
# conn = connect_database()
#
# if conn:
#     query = "SELECT * FROM jouw_tabel;"  # Vervang door je eigen SQL-query
#     execute_query(conn, query)
#     conn.close()  # Sluit de databaseverbinding
