from database import get_connection

try:
    connection = get_connection()
    print("CodePulse database connection successful!")
    connection.close()
except Exception as error:
    print("Database connection failed.")
    print(error)