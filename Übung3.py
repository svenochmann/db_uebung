# -*- coding: utf-8 -*-
"""
Created on Thu May 11 23:16:03 2023

@author: dimag
"""



import cx_Oracle
import random

# Establish a connection to the Oracle database
connection = cx_Oracle.connect("user037/ccjxbpyt@195.37.239.139/poradb")

if connection:
    print("Connection established successfully.")
else:
    print("Failed to establish connection.")
#%%
# Cursor erstellen
cursor = connection.cursor()

# Aufgabe 1a: Anzahl der Benutzertabellen ermitteln
cursor.execute("SELECT COUNT(*) FROM user_tables")
tables_count = cursor.fetchone()[0]
print("Anzahl der Benutzertabellen:", tables_count)

# Aufgabe 1b: Befehl zum Anzeigen aller Attribute einer Tabelle
table_name = 'YOUR_TABLE_NAME'
cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name}'")
columns = cursor.fetchall()
for column in columns:
    print(column[0])

# Aufgabe 2a: Tabelle erstellen
create_table_sql = """
CREATE TABLE Test (
    ID NUMBER(10),
    Messdaten1 NUMBER(10),
    Messdaten2 NUMBER(10),
    Messdaten3 NUMBER(10),
    Sensortyp VARCHAR2(50))
"""

# Execute the create table statement
cursor.execute(create_table_sql)
connection.commit()
print("Table created successfully.")

# Aufgabe 2b: Spalten hinzufügen
table_name = 'TEST1'
cursor.execute(f"CREATE TABLE {table_name} (id NUMBER, wert NUMBER)")

anzahl_spalten = 5  # Anzahl der gewünschten Spalten

for spalten_nr in range(1, anzahl_spalten + 1):
    spaltenname = f"spalte_{spalten_nr}"
    cursor.execute(f"ALTER TABLE {table_name} ADD {spaltenname} NUMBER")
connection.commit()

# Aufgabe 3a: Datensätze hinzufügen (manuell)
daten = [
    (1, 10.5, 20.3, 15.2, 'Sensor1'),
    (2, 5.8, 12.7, 8.9, 'Sensor2'),
    (3, 18.6, 14.2, 7.3, 'Sensor3')
]

cursor.executemany("""
    INSERT INTO Test (ID, Messdaten1, Messdaten2, Messdaten3, Sensortyp)
    VALUES (:1, :2, :3, :4, :5)
""", daten)
connection.commit()

# Aufgabe 3b: Datensätze hinzufügen (dynamisch)
anzahl_datensaetze = 10  # Anzahl der gewünschten Datensätze
anzahl_werte = 4  # Anzahl der Spaltenwerte pro Datensatz

for i in range(anzahl_datensaetze):
    daten = [random.randint(1, 9) for _ in range(anzahl_werte)]
    spalten = ', '.join([f"spalte_{j}" for j in range(1, anzahl_werte + 1)])
    werte = ', '.join(str(wert) for wert in daten)
    cursor.execute(f"INSERT INTO {table_name} (id, wert, {spalten}) VALUES ({i+1}, 0, {werte})")

#%%
connection.commit()


# Aufgabe 4a: Tabelle löschen
cursor.execute("DROP TABLE TEST")
connection.commit()

# Aufgabe 4b: Alle Spalten löschen
#table_name = 'TEST'
#cursor.execute(f"ALTER TABLE TEST DROP COLUMN TEST1")
#connection.commit()


# Aufgabe 4c: Datensätze löschen
#where_condition = "spalte IS NULL"
#cursor.execute(f"DELETE FROM TEST WHERE {where_condition}")
#connection.commit()

cursor.close()
connection.close()

#%%

# Establish a connection to the Oracle database
connection = cx_Oracle.connect("user037/ccjxbpyt@195.37.239.139/poradb")


if connection:
    print("Connection established successfully.")
else:
    print("Failed to establish connection.")

# Cursor erstellen
cursor = connection.cursor()

# a) Tabelle mit 1000 Attributen des Typs Number (1000 ind zuviele daten daher 999)
create_table_sql = "CREATE TABLE AdvancedTask ("
for i in range(1, 1000):
    create_table_sql += f"Spalte_{i} NUMBER(10), "
create_table_sql += "Zeile_Name VARCHAR2(20))"
cursor.execute(create_table_sql)
connection.commit()
print("Table created successfully.")

# b) Datensatz mit 100 Einträgen mit je 1000 Spalten mit zufälligen Werten zwischen 1-1000
daten = []
for i in range(1, 101):
    values = [random.randint(1, 1000) for _ in range(1000)]
    daten.append(values)

# c) Datensatz der Tabelle hinzufügen
for values in daten:
    placeholders = ', '.join([':{}'.format(i) for i in range(1, 1001)])
    insert_query = "INSERT INTO AdvancedTask VALUES ({})".format(placeholders)
    cursor.execute(insert_query, values)
connection.commit()
print("Data inserted successfully.")

# d) Tabelle mit einer Spalte vom Typ VarChar erweitern
cursor.execute("ALTER TABLE AdvancedTask ADD Zeile_Name VARCHAR2(20)")
for i in range(1, 101):
    cursor.execute(f"UPDATE AdvancedTask SET Zeile_Name = 'Zeile_{i}' WHERE rowid = '{i}'")
connection.commit()
print("Table extended and names assigned successfully.")

# e) Spalten 1-100 weg
alter_table_sql = "ALTER TABLE AdvancedTask"
for i in range(1, 101):
    alter_table_sql += f" DROP COLUMN Spalte_{i},"
alter_table_sql = alter_table_sql.rstrip(',')
cursor.execute(alter_table_sql)
connection.commit()
print("Columns 1-100 removed successfully.")

# f)Datensatz, mit Wert 1 entfernen
cursor.execute("DELETE FROM AdvancedTask WHERE '1' IN (" + ','.join([f"Spalte_{i}" for i in range(1, 1001)]) + ")")
connection.commit()
print("Rows containing value 1 removed successfully.")

cursor.close()
connection.close()

