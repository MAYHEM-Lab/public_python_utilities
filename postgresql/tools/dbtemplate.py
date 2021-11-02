"""
    Example utility to access dbiface.py in ../DB
    Access a postgresql database
python3 dbtemplate.py args.json
see args.json for details concerning its content and format
"""

from __future__ import print_function
import argparse, datetime, six, os, sys, time, exiftool, shutil, unicodedata, json
import socket, random
from pathlib import Path
#import the db interface in the DB directory in parent dir
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DB'))
import dbiface

DEBUG=False

parser = argparse.ArgumentParser(description='python3 dbtemplate.py see_args.json')
parser.add_argument('json', help='file containing all of the arguments')

##############################
def main():
    """Main program.
    """
    global DEBUG

    #process the arguments
    pargs = parser.parse_args()
    #sanity check
    if not os.path.isfile(pargs.json):
        print("Unable to open json file {}. \nUSAGE: python3 dbtemplate.py args.json".format(pargs.json))
        sys.exit(1)
   
    try: 
        with open(pargs.json, "r") as jfile:
            args = json.load(jfile)
        dbname = args["dbinfo"]["db"]
        tname = args["dbinfo"]["table"]
        dbuser = args["dbinfo"]["user"]
        dbpwd = args["dbinfo"]["pwd"]
        dbhost = args["dbinfo"]["host"]
        DEBUG = args["DEBUG"]
    except Exception as e:
        print(e)
        print("Unable to parse json file as expected. \nUSAGE: python3 dbtemplate.py args.json")
        sys.exit(1)

    #instantiate the database
    db = dbiface.DBobj(dbname,dbpwd,dbhost,dbuser)
    #check that we can access the DB
    if DEBUG:
        sql = 'SELECT version()'
        cur = db.execute_sql(sql)
        ver = cur.fetchone()
        print(ver)

    #create the table if it doesn't exist
    #the schema (called image) is setup in ../DB/dbiface.py
    exists = db.table_exists(tname)
    if not exists:
      retn = db.create_table('temp',tname) #table type template (temp), table name; returns T/F

    cur = db.get_cursor()
    value = (
        datetime.datetime.now(),
        float(random.random())
    )
    cur.execute("INSERT INTO {} (dt,temp) VALUES ( %s, %s) ON CONFLICT (dt) DO NOTHING".format(tname), value)  #names in ()s after {} must match db scheme set above in create ("temp" in this case)
    db.commit()

    cur = db.get_cursor() #start of table
    cur.execute("SELECT dt,temp FROM {}".format(tname))
    rows = cur.fetchall() #fetch all answers from query
    for row in rows:
        print(row)

    db.closeConnection()

if __name__ == '__main__':
    main()
