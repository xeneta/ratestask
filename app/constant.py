import configparser


PROPERTIES_PATH = 'rate.properties'
print(f"The properties values are fetched from this file: {PROPERTIES_PATH}")


config = configparser.ConfigParser()
config.read(PROPERTIES_PATH)


HOST = config.get("db_conf", "host")
PORT = config.get("db_conf", "port")
DATABASE = config.get("db_conf", "database")
USER = config.get("db_conf", "user")
PASSWD = config.get("db_conf", "password")
