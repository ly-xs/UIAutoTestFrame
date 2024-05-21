import os
import sys
import configparser

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config as cf
from pymysql import connect, cursors
from pymysql.err import OperationalError

# --------- 读取config.ini配置文件 ---------------
config = configparser.ConfigParser()
config.read(cf.CONFIG_FILE, encoding='UTF-8')
host = config.get("mysqlconf", "host")
port = config.get("mysqlconf", "port")
user = config.get("mysqlconf", "user")
password = config.get("mysqlconf", "password")
db = config.get("mysqlconf", "db_name")


class DB:
    """
    MySQL基本操作
    """

    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(user=user,
                                password=password,
                                host=host,
                                port=int(port),
                                database=db,
                                cursorclass=cursors.DictCursor
                                )
        except OperationalError as e:
            print(f"Mysql Error {e.args[0]}: {e.args[1]}")

    # 清除表数据
    def clear(self, table_name):
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            # 取消表的外键约束
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = f"INSERT INTO {table_name} ({key}) VALUES ({value})"

        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    def query(self, table_name, table_key):
        with self.conn.cursor() as cursor:
            execute_sql = f"SELECT {table_key} FROM {table_name}"
            cursor.execute(execute_sql)
            result = cursor.fetchall()
        return result

    # 关闭数据库
    def close(self):
        self.conn.close()

    # 初始化数据
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()
