#!/usr/bin/python
import os
import settings

db = 'db_data'
python="python"

args = os.sys.argv[1:]

if len(args) == 1:
    python = os.sys.argv[1]
apps = 'prompt game player'

cmd = python+' manage.py sqlclear '+apps+' | sqlite3 '+db
os.system(cmd)

cmd = python+' manage.py sqlreset '+apps+' | sqlite3 '+db
os.system(cmd)

cmd = python+' manage.py syncdb'
os.system(cmd)

