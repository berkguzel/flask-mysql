from flask import Flask, request, jsonify
from configparser import ConfigParser
import requests
import logging
import os
from mysql.connector import errorcode
import mysql.connector


dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/db.cfg')
logging.basicConfig(filename=config['DEFAULT']['log_file'], level=config['DEFAULT']['log_level'])

app = Flask(__name__)

@app.route('/SELECT', methods=['GET'])
def select():

    for i in request.args:
        req = request.args.get(i)
        if i == "name":
            sql = "SELECT * FROM userx WHERE name = %s"
            val = (req,)
        elif i == "lastName":
            sql = "SELECT * FROM userx WHERE lastName = %s"
            val = (req, )
        elif i == "mail":
            sql = "SELECT * FROM userx WHERE mail = %s"
            val= (req, )



    try:
        mysqldb =  connect()
        cursor =  mysqldb.cursor(buffered=True)
        cursor.execute(sql, val)
        response = cursor.fetchall()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        else:
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))

    return jsonify(response)

@app.route('/INSERT', methods=['POST'])
def insert():
    name = request.args.get("name")
    lastName = request.args.get("lastName")
    mail = request.args.get("mail")
    try:
        mysqldb =  connect()
        cursor =  mysqldb.cursor(buffered=True)
        sql = """INSERT INTO userx (name, lastName, mail) VALUES(%s, %s, %s)"""
        values = (name, lastName, mail)
        cursor.execute(sql, values)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        else:
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
    return jsonify(Success=True)


@app.route('/DELETE', methods=['DELETE'])
def delete():
    for i in request.args:
        req = request.args.get(i)
        if i == "name":
            sql = "DELETE FROM userx WHERE name = %s"
            val = (req,)
        elif i == "lastName":
            sql = "DELETE FROM userx WHERE lastName = %s"
            val = (req, )
        elif i == "mail":
            sql = "DELETE FROM userx WHERE mail = %s"
            val= (req, )

    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        cursor.execute(sql, val)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
        else:
            logging.error(str(e))
            return jsonify(Success=False, Error=str(e))
    return jsonify(Success=True)

def connect():
    return mysql.connector.connect(
        user=config['DEFAULT']['mysql_user'],
        password=config['DEFAULT']['mysql_password'],
        host=config['DEFAULT']['mysql_host'],
        database=config['DEFAULT']['mysql_database'],
        auth_plugin='mysql_native_password')  

if __name__=="__main__":
    app.run(host=config['APISERVER']['api_host'], port=config['APISERVER']['api_port'])