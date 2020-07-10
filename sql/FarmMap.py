from tools.DataBaseOperate import DataBaseOperate
from tools.Config import Config, Log

host_ip = Config('config').data['database'][Config('config').data['run']]['host_ip']


class FarmMap(object):
    L = Log("ConfigInformationSql")
    db = DataBaseOperate()

    def query_swarm_count(self):
        """
        查询外部蜂场数量
        :return:
        """
        sql = """SELECT
                        Count( * ) 
                    FROM
                        `fc-bee`.t_swarm_info si 
                    WHERE
                        si.is_delete = 0;"""
        return self.db.operate(host_ip, sql)

    def query_today_new_swarm(self):
        """
        今日新增外部蜂场
        :return:
        """
        sql = """SELECT Count( * )
                 FROM `fc-bee`.t_swarm_info
                 WHERE is_delete = 0
                   AND lat IS NOT NULL
                   AND date_format(create_time, '%Y-%m-%d') = date_format(now(), '%Y-%m-%d');"""
        return self.db.operate(host_ip, sql)
