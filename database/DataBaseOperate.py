#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
@Time: 2019/12/31 19:43
@Author: hengxin
"""


import pymysql
import datetime
import decimal
import json
from config.Config import Log


class DataBaseOperate(object):
    L = Log("DataBaseOperate")

    def operate(self, host, sql):
        if host == "192.168.62.244":
            user, password, port = "farm", "HEFAWW", 3306
        elif host == "39.104.65.76":
            user, password, port = "qa", "eYKvb5LXczUh7285UJt2T8070NkP", 3306
        # elif host == "132.232.47.119":
        #     user, password, port = "ms", "MiaoShu@2018", 3306
        elif host == "39.104.28.40":
            user, password, port = "ms", "ms@test_2019", 3306
        elif host == "161.117.1.134":
            user, password, port = "root", "jj8ePh5ZHnb3dmtGaPl2", 3306
        elif host == "47.88.222.252":
            user, password, port = "qa", "vFLDbvhvxhR.4uK26fLa0lLnVS44S0", 3306
        elif host == "192.168.62.73":
            user, password, port = "root", "Knight01", 3306
        elif host == "192.168.62.211":
            user, password, port = "farm", "WorldFarm", 3306
        elif host == "203.6.234.220":
            user, password, port = "xinheng", "v1LDwAUWzEgWM", 3306
        elif host == "47.74.225.79":
            user, password, port = "qa", "vFLDbvhvxhR.4uK26fLa0lLnVS44S0", 3306
        else:
            raise Exception("IP域名错误")

        db = pymysql.connect(host=host,
                             port=port,
                             user=user,
                             passwd=password)
        con = db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # 此处新增 单次连接执行多条SQL的功能, 兼容书写时首尾多输入空格的情况
            sql_list = sql.strip().split(";")
            try:
                # 此处兼容以分号结尾的单句SQL仍返回一维列表
                sql_list.remove('')
            except ValueError as e:
                self.L.logger.error(e)
                raise Exception("SQL请以分号 ; 结束")
            if len(sql_list) < 2:
                con.execute(sql)
                self.L.logger.debug(sql)
                effect_row = con.rowcount
                if sql.lower().startswith('select'):
                    self.L.logger.debug(sql)
                    # if effect_row != 1:
                    #     self.L.logger.info(sql)
                    # else:
                    #     pass
                    self.L.logger.debug("影响行数 %s" % effect_row)
                else:
                    pass
                results = con.fetchall()
                db.commit()
                # print(results)
                for result in results:
                    for fields in result:
                        if isinstance(result[fields], datetime.datetime):
                            result[fields] = str(result[fields].strftime('%Y-%m-%d %H:%M:%S'))
                        elif isinstance(result[fields], datetime.date):
                            result[fields] = str(result[fields].strftime('%Y-%m-%d'))
                        elif isinstance(result[fields], decimal.Decimal):
                            result[fields] = float(result[fields])
            else:
                results = []
                for sql in sql_list:
                    if sql != '':
                        con.execute(sql)
                        self.L.logger.debug(sql)
                        effect_row = con.rowcount
                        if sql.lower().startswith('select'):
                            self.L.logger.debug(sql)
                            # if effect_row != 1:
                            #     self.L.logger.info(sql)
                            # else:
                            #     pass
                        else:
                            pass
                        self.L.logger.debug("影响行数 %s" % effect_row)
                        results.append(con.fetchall())
                        db.commit()
                    else:
                        pass
                for result in results:
                    for r in result:
                        for fields in r:
                            if isinstance(r[fields], datetime.datetime):
                                r[fields] = str(r[fields].strftime('%Y-%m-%d %H:%M:%S'))
                            elif isinstance(r[fields], datetime.date):
                                r[fields] = str(r[fields].strftime('%Y-%m-%d'))
                            elif isinstance(r[fields], decimal.Decimal):
                                r[fields] = float(r[fields])
            con.close()
            # if sql.lower().startswith('select'):
            self.L.logger.debug("\n" + json.dumps(results, ensure_ascii=False,
                                                  sort_keys=True, indent=2, separators=(',', ': ')))
            # else:
            #     pass
            return results
        except Exception as e:
            db.rollback()
            self.L.logger.error(e)
            raise KeyError(e)
