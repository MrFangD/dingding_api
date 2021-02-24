# -*- coding: utf-8 -*-
"""
    @Version: V1.0
    @Time: 2020-11-07 13:43
    @Author: 全脂老猫
    @Describe:1、python连接SqlServer数据库的工具类
              2、需要注意的是：读取数据的时候需要decode('utf-8')，写数据的时候需要encode('utf-8')，这样就可以避免烦人的中文乱码或报错问题。
              3、Python操作SQLServer需要使用pymssql模块，使用pip install pymssql安装
"""
import pymssql


class Mssql:
    def __init__(self):
        # 数据库连接参数
        # self.host = '192.168.1.51'
        # self.user = 'lc0129999'
        # self.pwd = 'lst123698'
        # self.db = 'cwbase21'
        self.host = '192.168.1.14'
        self.user = 'lc0129999'
        self.pwd = 'lst123698'
        self.db = 'cwbase21'

    def getConnect(self):
        if not self.db:
            raise(NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cursor = self.conn.cursor()
        if not cursor:
            raise(NameError, "连接数据库失败")
        else:
            return cursor

    # sql查询
    def execQuery(self, sql):
        cursor = self.getConnect()
        cursor.execute(sql)
        resList = cursor.fetchall()  # 获取查询的所有数据
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    # 流水号处理
    def execQueryLsh(self, sql):
        cursor = self.getConnect()
        cursor.execute(sql)
        resList = cursor.fetchall()  # 获取查询的所有数据
        # 查询完毕后必须关闭连接
        self.conn.commit()
        self.conn.close()
        return resList

    # 增删改
    def execNonQuery(self, sql):
        cursor = self.getConnect()
        try:
            cursor = cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()
            self.conn.close()
            return False
        else:
            self.conn.commit()
            self.conn.close()
            return True