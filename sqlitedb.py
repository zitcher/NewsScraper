import sqlite3


class Database(object):
    '''Generic functions for a database'''

    def __init__(self, path):
        self.path = path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def close(self):
        self.connection.close()

    def execute(self, sql_command):
        self.connection.execute(sql_command)

    def commit(self):
        self.connection.commit()

    def executemany(self, sql_command, array):
        self.connection.executemany(sql_command, array)


class Sql_Commands(object):
    '''Generic commands for sql database'''
    def __init__(self):
        return

    '''
        string name: name
        string properties: (name type, .... ,  name type)
    '''
    def create_table(self, name, properties):
        sql = "CREATE TABLE " + name + " " + properties
        return sql

    '''
    input:
    string table_name,
    list data:
    [
        properties to insert
    ]
    '''
    def create_insert(self, table_name, data):
        sql = "INSERT INTO " + table_name + " VALUES ("
        vals = map(self.stock_data_to_string_list, data)
        sql += ', '.join(vals)
        sql += ")"
        return sql

    '''
    input:
    string/float
    output:
    string if input is float
    string surrounded by '' if input is string
    '''
    def stock_data_to_string_list(self, data):
        if isinstance(data, str):
            return "'" + data + "'"
        return str(data)

    '''
    input:
    table_name, index_name, column_name

    CREATE INDEX index_name ON table_name (column_name)
    '''
    def create_sql_index(self, table_name, index_name, column_name):
        return "CREATE INDEX " + index_name + " ON " + table_name + "(" + column_name + ")"
