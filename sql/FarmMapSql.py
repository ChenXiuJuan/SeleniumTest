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

    def query_swarm_info(self, plant_name, create_time, user_name):

        """
        外部蜂场信息
        :param plant_name: 当前蜜源名称
        :param create_time: 创建时间
        :param user_name: 采集人真实姓名
        :return:
        """
        sql = """SELECT
                    i.*
                FROM
                    `fc-bee`.t_swarm_info i
                    LEFT JOIN `world-user`.t_user u ON i.creator_id = u.id
                WHERE
                    i.is_delete = 0 
                    AND i.cur_nectar_type IN (SELECT sp.`code` FROM `fc-bee`.t_nectar_source_plant sp WHERE sp.is_delete = 0 AND sp.plant_name = '%s') 
                    AND i.create_time LIKE '%s%%%%'
                    AND u.username = '%s';""" %(plant_name, create_time, user_name)
        return self.db.operate(host_ip, sql)

    def query_config_value(self, code, value):

        """
        查询配置文件value
        :param code: 配置类型
        :param value:配置key
        :return:
        """
        sql = """SELECT
                    c.`value`
                FROM
                    `fc-bee`.t_config c
                WHERE
                    c.is_delete = 0
                    AND c.`code` = '%s'
                    AND c.`key` = '%s';""" %(code, value)
        return self.db.operate(host_ip, sql)

    def query_swarm_info_img(self, swarm_id):
        """
        查询外部蜂场照片信息
        :param swarm_id: 外部蜂场id
        :return:
        """
        sql = """SELECT
                    a.url
                FROM
                    `fc-bee`.t_swarm_attach a 
                WHERE
                    a.is_delete = 0
                    AND a.swarm_id = '%s';""" %swarm_id
        return self.db.operate(host_ip, sql)

    def query_swarm(self, swarm_name, address, expect_hive_num, create_time):
        """
        通过指定特殊字段值查询是否存在蜂场数据
        :param swarm_name: 蜂场名称
        :param address: 蜂场详细地址
        :param expect_hive_num: 预计投放箱数
        :param create_time: 创建时间
        :return:
        """
        sql = """SELECT
                    * 
                FROM
                    `fc-bee`.t_nectar_source
                WHERE
                    `name` = '%s' 
                    AND `address` = '%s' 
                    AND `expect_hive_num` = '%s'
                    AND `create_time` LIKE '%s%%%%';""" %(swarm_name, address, expect_hive_num, create_time)
        return self.db.operate(host_ip, sql)

    class Bee(object):
        L = Log("ConfigInformationSql")
        db = DataBaseOperate()
