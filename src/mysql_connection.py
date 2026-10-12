import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="39257",
        database="student_performance"
    )

    if connection.is_connected():
        print("Successfully connected to MySQL!")
        print("Database: student_performance")

except mysql.connector.Error as error:
    print("MySQL connection failed:", error)

finally:
    if "connection" in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")