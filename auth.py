import sqlite3, requests, json
from sqlite3 import Error
from pprint import pprint
from datetime import datetime, timezone, timedelta

api_key = "SUdMkOldiHZ69WlZBwteQlMCgJtYLKoX"
api_secret = "eS0DRC5jRuasfK6Z"
database = r"./db.db"


def get_timestamp():
     now = datetime.now(tz=timezone.utc)
     return now.isoformat().split('.')[0]


def select(**kwargs):
     conn = sqlite3.connect(database)
     cursor = conn.cursor()

     _fields = kwargs.get('fields', '*')
     _table = kwargs.get('table')
     _where = kwargs.get('where', [1])

     if _fields == '*':
          select = '*'
     else:
          fields = []
          for f in _fields:
               fields.append('`' + f + '`')
          select = ','.join(fields)
     where = ' AND '.join(_where)

     query = f"""SELECT {select} FROM `{_table}` WHERE {where}"""
     cursor.execute(query)

     output = cursor.fetchall()

     conn.commit()
     conn.close()
     try:
          return output[0]
     except IndexError:
          return []


def insert(**kwargs):
     _table = kwargs.get('table')
     _data = kwargs.get('data')
     conn = sqlite3.connect(database)

     columns = []
     rows = []

     if not isinstance(_data, list):
          _data = [_data]

     for col in _data[0]:
          columns.append(col)

     for row in _data:
          _row = []
          for col in columns:
               _row.append(row[col])
          rows.append(_row)

     quoted_columns = map(lambda i: f"`{i}`", columns)
     query_columns = ','.join(quoted_columns)
     query_rows = []
     for row in rows:
          quoted_items = map(lambda i: f"'{i}'", row)
          query_rows.append("(" + ','.join(quoted_items) + ")")

     query = f"""INSERT INTO `{_table}` ({query_columns}) VALUES {','.join(query_rows)}"""
     r = conn.execute(query).lastrowid

     conn.commit()
     conn.close()

     return r

def get_stored_auth():
     return select(fields=['access_token'],
                   table='auth',
                   where=[f"expires_at > '{get_timestamp()}'"])[0]


def get_new_auth():
     url = "https://test.api.amadeus.com/v1/security/oauth2/token"
     headers = {
          "Content-Type": "application/x-www-form-urlencoded"
     }
     params = {
          "grant_type": "client_credentials",
          "client_id": api_key,
          "client_secret": api_secret
     }

     r = requests.post(url, data=params, headers=headers)
     response = r.json()

     now = datetime.now(tz=timezone.utc)
     expires_at = now + timedelta(seconds=response['expires_in'])

     expires_at = expires_at.isoformat().split('.')[0]
     client_id = response['client_id']
     access_token = response['access_token']

     data = {
          "client_id": client_id,
          "access_token": access_token,
          "expires_at": expires_at
     }
     return insert(table='auth', data=data)

     return access_token
