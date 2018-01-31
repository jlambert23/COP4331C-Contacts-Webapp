#!/usr/bin/python3
# coding: utf-8

import json
print("Content-Type: application/json\n\n")

def getjson():
    import sys
    return json.load(sys.stdin)

def throwErr(message):
    print(json.dumps({'error': "" + message + ""}))
    
def login(jsonPayload):
    import pymysql

    try:
        user = jsonPayload['username']
        password = jsonPayload['password']
    except:
        throwErr("JSON incorrectly configured.\n" + str(jsonPayload))
        return

    try:
        # Import connection settings.
        from dbsettings import connection_properties
        conn = pymysql.connect( **connection_properties )
        cursor = conn.cursor()
    except:
        throwErr("Server was unable to be reached.")
        return

    try:
        # Throw before accessing database if non-alphanumeric characters are used.
        import re
        if not re.match('^[\w-]+$', user) is not None:
            raise Exception
        
        #
        sql = "SELECT id FROM user WHERE username='%s' AND password='%s';" % (user, password)
        cursor.execute(sql)        
        userid = cursor.fetchone()[0]
        
        if not userid:
            raise Exception
        
        # 
        sql2 = "SELECT * FROM `contact` WHERE userid='%d';" % userid
        cursor.execute(sql2)        
        columns = cursor.description
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
		
        result = [userid] + result
        print(json.dumps(result))
        conn.close()
        
    except Exception as e:
        throwErr(str(e) + "\nIncorrect login information.")
        return

parsed_json = json.loads('{"username":"user", "password":"password"}')
parsed_json = getjson()
login(parsed_json)
