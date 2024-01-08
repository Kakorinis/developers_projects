import psycopg2
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import time

# Connection parameters for the database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="1111",
    dbname="ka_clients"
)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

specs_dict = {

    "parameters": [
        {
            "name": "phone_str",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "The phone number of the client"
        }
    ],
    "responses": {
        "200": {
            "description": "OK"
        }
    }
}

class FullnameGetter(Resource):
    @swag_from(specs_dict)  
    def get(self, phone_str):
        with conn, conn.cursor() as cursor:
            query = f"SELECT * FROM all_clients WHERE phone = '{phone_str}'"
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            time.sleep(2)
        return df.to_dict('records')

api.add_resource(FullnameGetter, '/client/<string:phone_str>')

if __name__ == '__main__':
    app.run(debug=True)