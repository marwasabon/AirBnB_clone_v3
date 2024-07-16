from sqlalchemy import create_engine ,MetaData , Table
class MySQLConnectionTester:
    def __init__(self, host, database, username='root', password=''):
        self.uri = f"mysql://silver:Password_12345@192.168.33.10/contact"

    def test_connection(self):
        try:
            engine = create_engine(self.uri)
            
            with engine.connect():
                print("Successfully connected to the database")

        except Exception as e:
            print("Error connecting to the database:", e)

    def query_all_users(self):
        try:
            engine = create_engine(self.uri)
            meta = MetaData()
            meta.reflect(bind=engine)

            users_table = Table('users', meta, autoload=True, autoload_with=engine)

            with engine.connect() as connection:
                select_query = users_table.select()
                result = connection.execute(select_query)

                for row in result:
                    print(row)

        except Exception as e:
            print("Error querying users table:", e)
# Usage example:
conn_tester = MySQLConnectionTester(host='localhost', database='test_db', username='root', password='')
conn_tester.test_connection()
conn_tester.query_all_users()
