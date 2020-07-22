from database.DataBaseOperate import DataBaseOperate
from config.Config import Config, Log

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

    def query_num_bee_friend_have_user_id(self):
        """
        累计蜂友总数，开通账号的蜂友只统计 蜂友\养蜂总监\老师, 所有未开通账号的蜂友(不区分账号来源，区分账号是否注销)
        有手机号的蜂友数量
        :return:
        """
        sql = """SELECT count(DISTINCT tbf.user_id) AS '有手机号的蜂友数量'
                 FROM `fc-bee`.t_bee_friend tbf
                    LEFT JOIN `fc-bee`.t_user_role AS tur ON tur.user_id = tbf.user_id AND tur.is_delete = 0
                 WHERE tbf.is_delete = 0
                    AND tbf.status <> 3
                    AND tbf.user_id IS NOT NULL
                    AND (tur.role_code IS NULL OR tur.role_code IN (1000, 1002, 1003));"""
        return self.db.operate(host_ip, sql)

    def query_num_bee_friend_not_user_id(self):
        """
        累计蜂友总数，开通账号的蜂友只统计 蜂友\养蜂总监\老师, 所有未开通账号的蜂友(不区分账号来源，区分账号是否注销)
        无手机号的蜂友数量
        :return:
        """
        sql = """SELECT count(1) AS '无手机号的蜂友数量'
                 FROM `fc-bee`.t_bee_friend
                 WHERE is_delete = 0
                   AND user_id IS NULL;"""
        return self.db.operate(host_ip, sql)

    def query_num_bee_friend_today(self):
        """
        今日新增蜂友（不包含注销的，有手机号的蜂友+无手机号的蜂友）
        :return:
        """
        sql = """SELECT count(1) AS '今日新增蜂友'
                 FROM `fc-bee`.t_bee_friend
                 WHERE is_delete = 0
                   AND status <> 3
                   AND to_days(now()) = to_days(create_time);"""
        return self.db.operate(host_ip, sql)

    def query_num_promotion_staff(self):
        """
        推广人员数量
        :return:
        """
        sql = """SELECT COUNT(*) # 推广人员数量
                 FROM `fc-bee`.t_bee_friend AS tbf
                          INNER JOIN `fc-bee`.t_user_role AS tur ON tbf.user_id = tur.user_id
                     AND tur.is_delete = 0
                     AND tur.role_code IN (1006)
                 # , 1004, 1005
                 WHERE
                 #       tbf.lat IS NOT NULL AND # 推广人员位置
                     tbf.is_delete = 0
                   AND tbf.status <> 3;"""
        return self.db.operate(host_ip, sql)

    def query_num_nectar(self):
        """
        自有蜂场总数（只统计待入驻/已完成的未删除的)
        :return:
        """
        sql = """SELECT count(1) AS '自有蜂场总数'
                 FROM `fc-bee`.t_nectar_source
                 WHERE is_delete = 0;"""
        return self.db.operate(host_ip, sql)

    def query_num_nectar_settled(self):
        """
        自有入驻蜂场数（只统计已入驻的未删除的)
        :return:
        """
        sql = """SELECT count(1) AS '自有入驻蜂场数'
                 FROM `fc-bee`.t_nectar_source
                 WHERE is_delete = 0
                   AND status = 2;"""
        return self.db.operate(host_ip, sql)

    def query_num_beekeeper_teacher(self):
        """
        自有养蜂人（不包含注销的，有手机号的蜂友）
        :return:
        """
        sql = """SELECT
                        count(1) AS '自有养蜂人'
                 FROM `fc-bee`.t_user_role tur
                          LEFT JOIN `fc-bee`.t_bee_friend tbf ON tbf.user_id = tur.user_id
                 WHERE tur.role_code IN (1002, 1003)
                   AND tbf.status <> 3
                   AND tbf.is_delete = 0
                   AND tur.is_delete = 0;"""
        return self.db.operate(host_ip, sql)
