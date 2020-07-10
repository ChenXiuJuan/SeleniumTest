from tools.Config import Log


class Tool(object):
    L = Log('Tool')

    @staticmethod
    def parse_int(num):
        """
        数字串从后往前每隔三个数字加一个逗号， 例如:1234567 ---> 1,234,567
        :param num:数字串
        :return:
        """
        to_str = str(num)
        count = 0
        sumstr = ''
        for one_str in to_str[::-1]:
            count += 1
            if count % 3 == 0 and count != len(to_str):
                one_str = ',' + one_str
                sumstr = one_str + sumstr
            else:
                sumstr = one_str + sumstr
        return sumstr





