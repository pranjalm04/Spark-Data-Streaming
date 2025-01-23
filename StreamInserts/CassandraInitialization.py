from cassandra.cluster import Cluster
from logger import logger
class CassandraInit:
    session=None
    def __init__(self):
        try:
            cluster = Cluster(['cassandra'],port=9042)
            self.session = cluster.connect()
        except Exception as e:
            logger.warning(f"Could not create cassandra connection due to {e}")

    def getSession(self):
        return self.session
    def create_keyspace(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS spark_streams
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """)

        logger.info("Keyspace created successfully!")

    def create_table(self):
        self.session.execute("""
        CREATE TABLE IF NOT EXISTS spark_streams.created_users (
            id UUID PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            address TEXT,
            post_code TEXT,
            email TEXT,
            username TEXT,
            registered_date TEXT,
            phone TEXT,
            picture TEXT);
        """)

        logger.info("Table created successfully!")

    def insert_data(self, **kwargs):
        logger.info("inserting data...")
        user_id = kwargs.get('id')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        gender = kwargs.get('gender')
        address = kwargs.get('address')
        postcode = kwargs.get('post_code')
        email = kwargs.get('email')
        username = kwargs.get('username')
        dob = kwargs.get('dob')
        registered_date = kwargs.get('registered_date')
        phone = kwargs.get('phone')
        picture = kwargs.get('picture')

        try:
            self.session.execute("""
                INSERT INTO spark_streams.created_users(id, first_name, last_name, gender, address, 
                    post_code, email, username, dob, registered_date, phone, picture)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, first_name, last_name, gender, address,
                  postcode, email, username, dob, registered_date, phone, picture))
            logger.info(f"Data inserted for {first_name} {last_name}")

        except Exception as e:
            logger.error(f'could not insert data due to {e}')

cassandra=CassandraInit()