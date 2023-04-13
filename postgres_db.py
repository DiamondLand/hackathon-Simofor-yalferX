import asyncio
import psycopg2
import configparser
from loguru import logger
from base64 import b16encode as enc64
config = configparser.ConfigParser()
config.read("settings.ini")

async def db_connection():
    connection = psycopg2.connect(
        user=config["Database"]["user"], 
        password=config["Database"]["password"],
        database=config["Database"]["database"], 
        host=config["Database"]["host"]
    )
    connection.autocommit = True
    try:
        
        connection.cursor().execute("DROP TABLE IF EXISTS staff")
        connection.cursor().execute("DROP TABLE IF EXISTS progress")
        connection.cursor().execute("DROP TABLE IF EXISTS messages")
        
        connection.cursor().execute(
            "CREATE TABLE staff (key SERIAL NOT NULL PRIMARY KEY, name VARCHAR(100), surname VARCHAR(100), years BIGINT, years_on_company BIGINT, description TEXT, status VARCHAR(10))"
        )
        connection.cursor().execute(
            "CREATE TABLE progress (key SERIAL NOT NULL PRIMARY KEY, member_id BIGINT, acquaintance BIGINT, acquaintance_teory BIGINT, ofice_acquaintance BIGINT, ofice_acquaintance_teory BIGINT, products INT, stash INT)"
        )
        connection.cursor().execute(
            "CREATE TABLE messages (key SERIAL NOT NULL PRIMARY KEY, sender_id BIGINT, recipient_id BIGINT, message VARCHAR(1000))"
        )
        '''
        connection.cursor().execute(
            "CREATE TABLE images (key SERIAL NOT NULL PRIMARY KEY, name TEXT, binary_code BYTEA)"
        )

        choices = "bathroom", "director", "installation-department", "meeting-room", "project-main-staff"
        with open("assests/ofice-plan.png", "rb") as photo:
            binary = enc64(photo.read())
        connection.cursor().execute(
            "INSERT INTO images (name, binary_code) VALUES (%s, %s)",
            (
                "ofice-plan",
                binary
            )
        )
        '''
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    try:
        asyncio.run(db_connection())
    except:
        pass