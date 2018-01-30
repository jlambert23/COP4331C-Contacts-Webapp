#!/usr/bin/env python3
# coding: utf-8

import json

def login(json):
    import pymysql

    try:
        user = json['userName']
        password = json['password']
    except:
        throwErr("JSON incorrectly configured.\n%s" % json)
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

        sql = "SELECT id FROM user WHERE userName='%s' AND password='%s';" % (user, password)
        cursor.execute(sql)
        result = cursor.fetchone()
        
        sendjson(result[0])
        conn.close()
    except:
        throwErr("Incorrect login information.")
        return

    # try:
    #     sql = "SELECT * FROM contact;"
    #     #WHERE userName='"+parsed_json['username']+"' AND password='"+parsed_json['password']+"';"
    #     cursor.execute(sql)

    #     columns = cursor.description 
    #     result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

    #     sendjson(result)
    #     conn.close()
    # except:
    #     sendjson('{"error":"Unable to retrieve contacts."}')

def getjson():
    import sys
    return json.load(sys.stdin)

def sendjson(message):
    header = "Content-type: application/json\n\n"
    print(header + json.dumps(message))

def throwErr(message):
    sendjson('{"error":"%s"}' % message)

parsed_json = getjson()
login(parsed_json)
