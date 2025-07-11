#code 1
import psycopg2

# Replace 'yourpassword' with the one you used in the docker command
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="yourpassword" #change pwd here
)

print("Connected to PostgreSQL!")
conn.close()
