import config
import mysql.connector

DB = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	password = config.DB_PASSWORD,
	port = '3306',
	database = 'deliveryappproject'
)