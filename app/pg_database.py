# postgres imports
import psycopg2
from psycopg2.extras import RealDictCursor

# logic imports
import time

### postgres database connection (USE ORM ITS WAY BETTER)
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi-course',
#                                 user='postgres', password='NollieHeel360!',
#                                 cursor_factory=RealDictCursor) # returns column name
#         cursor = connection.cursor()
#         print("PG Database connection successful.")
#         break
#     except Exception as error:
#         print(f"PG Database connection failed. Error: {error}")
#         time.sleep(2)