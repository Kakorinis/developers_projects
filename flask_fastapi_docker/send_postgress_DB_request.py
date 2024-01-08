from sqlalchemy import create_engine, text
import pandas as pd
import time


class DatabaseConnector:
    def __init__(self, database, host, port, username, password):
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.conn_str = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    def connect(self):
        engine = create_engine(self.conn_str)
        return engine.connect()

class FullnameGetter(DatabaseConnector):
    def __init__(self, database, host, port, username, password):
        super().__init__(database, host, port, username, password)
    def get_client_by_phone(self, phone_str):
        with self.connect() as connection:
            query = text(fr""" SELECT * FROM all_clients 
                               WHERE phone like '%{phone_str}%' """)
            df = pd.io.sql.read_sql(query, connection)
            #time.sleep(3)

            return df

start = time.time()

database = 'ka_clients'
host = "localhost" #localhost"
port = 5432
username = 'postgres'
password = '1111'

loader = FullnameGetter(database, host, port, username, password)
result = loader.get_client_by_phone('79891968094')
end = time.time() - start
print(result.to_dict('records'))
print(end)

