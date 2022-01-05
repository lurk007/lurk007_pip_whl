import hashlib
import base64
from lurk007_pip_whl.decorators.decorator import logger, lissen_time


class BaseDecode(object):
    """
    基础编码解码
    """

    def __init__(self):
        pass

    @staticmethod
    def encode_base64(s='admin', action_count=1, encoding='utf-8'):
        """
        base64编码
        s:字符串
        action_count:编码次数，默认一次
        :return: str
        """
        for i in range(action_count):
            s = bytes(s, 'utf-8')
            s = str(base64.b64encode(s), encoding)
        return s

    @staticmethod
    def decode_base64(s='YWRtaW4=', action_count=1, encoding='utf-8'):
        """
        base64解码
        s:字符串
        action_count:编码次数
        :return: str
        """
        for i in range(action_count):
            s = bytes(s, 'utf-8')
            s = str(base64.b64decode(s), encoding)
        return s

    @staticmethod
    def encode_md5(s='admin', action_count=1, encoding='utf-8'):
        """
        md5加密
        s:字符串
        action_count:加密次数
        :return: str
        """
        for i in range(action_count):
            input_name = hashlib.md5()
            input_name.update(s.encode(encoding))
            s = input_name.hexdigest()
        return s

    @staticmethod
    def encode_buffer(s="admin", action_count=1, *funcs):
        """
        功能： 对字符串执行 任意算法 任意次数
        s: 字符串: 默认:admin
        action_count: 算法执行次数
        funcs：依次执行的算法
        return: 算法执行结果
        """
        res = s
        if len(funcs) == 0:
            funcs = [BaseDecode.encode_md5, BaseDecode.encode_base64]
        for i in range(action_count):
            for j in funcs:
                res = j(res)
        return res


class MyMath(object):
    """
    数学计算
    """

    @staticmethod
    def b16(x):
        """
        16进制转10进制
        :param x: 16进制
        :return:
        """
        return int(x, 16)

    @staticmethod
    def b8(x):
        """
        8进制转10进制
        :param x: 8进制
        :return:
        """
        return int(x, 8)

    @staticmethod
    def b2(x):
        """
        2进制转10进制
        :param x: 2进制
        :return:
        """
        return int(x, 2)

    @staticmethod
    def to16(x, bit):
        """
        10进制转16进制
        :param x: 10进制数
        :param bit: 16进制左边补0后长度
        :return:
        """
        s = hex(x)[2:]
        s = F"{'0' * (bit - len(s))}{s}"
        return s

    @staticmethod
    def to8(x, bit):
        """
        10进制转8进制
        :param x: 10进制数
        :param bit: 8进制左边补0后长度
        :return:
        """
        s = oct(x)[2::]
        # print(s)
        s = F"{'0' * (bit - len(s))}{s}"
        return s

    @staticmethod
    def to2(x, bit):
        """
        10进制转2进制
        :param x:10进制数
        :param bit:二进制左边补0后长度
        :return:
        """
        s = bin(x)[2:]
        s = F"{'0' * (bit - len(s))}{s}"
        return s

    @staticmethod
    def displacement(x, bit):
        """
        二进制0，1换位并逆序
        :param x: 二进制字符串
        :param bit: 二进制结果长度
        :return:
        """
        s = ''
        l = len(x)
        x = F"{'0' * (bit - l)}{x}"
        for i in x:
            if i == '1':
                s += '0'
                continue
            s += '1'
        return s


class EightDiagrams(object):
    def __init__(self, plaintext=None, ciphertext=None, b=12):
        """
        结合太极八卦组成的加密算法
        :param plaintext: 明文
        :param ciphertext: 密文
        :param b: 加密方式：6,12,18,24  只需要数字选6；12支持大小写英文字符以及字符符号；18,24支持中文，24+支持的会更多，只要是6的倍数即可，密钥生成长度与耗时与此项成正比
        """
        self.__bit = abs(b)  # 每个字符对应二进制字符串的长度
        assert self.__bit % 6 == 0, 'bit必须是6的倍数'
        self.__ciphertext = ciphertext
        self.__plaintext = plaintext
        # self.__keys = ['000', '001', '010', '011', '100', '101', '110', '111']
        self.__keys = ['000', '001', '010', '011', '100', '101', '110', '111'] + [F'{i}' for i in range(99)]
        # self.__values = ['🗜', 'Æ', 'Ì', 'Ü', 'Ù', 'Õ', '.', '🕒']
        self.__values = [chr(i) for i in range(5010, 20000 + 99)]
        self.__values = [chr(110000), chr(100100), chr(100009), chr(100600), chr(102000), chr(100200), chr(100040),
                         chr(100001)]
        self.__values = ['坤', '震', '坎', '兑', '艮', '离', '巽', '乾']
        self.__items = dict(zip(self.__keys, self.__values))

    def items(self):
        return self.__items

    def keys(self):
        return self.__keys

    def values(self):
        return self.__values

    def __tob2(self):
        self.__b2 = list()
        for i in self.__plaintext:
            self.__b2.append(
                MyMath.displacement(MyMath.to2(ord(i), self.__bit), self.__bit))  # 将字符转为ascci码 再转成二进制 随后1和1对调 存贮到__b2

    def __tochr(self, li):
        s = ''
        for i in li:
            # print(b2(displacement(i, self.__bit)))
            s += chr(MyMath.b2(MyMath.displacement(i, self.__bit)))
        return s

    def encode(self):
        """
        加密算法
        :return:
        """
        self.__tob2()
        li = []
        count = range(int(self.__bit / 3))  # 计算每个二进制字符串三个一组需要拆分的次数
        for i in self.__b2:
            for j in count:  #
                li += [i[j * 3:(j + 1) * 3:]]  # 三个数字一组拆分二进制自服从
        s = ''
        for i in li[::-1]:  # 将三位数二进制对应八卦卦象
            s += self.__items[i]  # {'101':'xxx','111':'xxx'}
        self.__ciphertext = s  # 保存密文
        print("密文:", s)
        return s

    def decode(self):
        """
        解密算法
        :return:
        """
        kv = dict(zip(self.__values, self.keys()))
        li = [kv[k] for k in self.__ciphertext][::-1]
        s = ''
        for i in li:
            s += i
        count = range(int(len(s) / self.__bit))
        li = [s[i * self.__bit:(i + 1) * self.__bit:] for i in count]
        s = self.__tochr(li)
        print("明文:", s)
        return s


@lissen_time
@logger
def main():
    s = '123456'
    ed = EightDiagrams(plaintext=s, b=18)
    mw = ed.encode()
    mingwen = ed.decode()
    return mw, mingwen


if __name__ == '__main__':
    """"""
    # main()
    # s = "https://www.baidu.com/s?cl=3&tn=baidutop10&fr=top1000&wd=%E6%9B%BE%E5%85%89%3A%E8%A5%BF%E5%AE%89%E7%96%AB%E6" \
    #     "%83%85%E6%98%AF%E6%AD%A6%E6%B1%89%E5%90%8E%E6%9C%80%E4%B8%A5%E9%87%8D%E4%B8%80%E5%9B%9E&rsv_idx=2&rsv_dl" \
    #     "=fyb_n_homepage&sa=fyb_n_homepage&hisfilter=1 "
    # ed = EightDiagrams(plaintext=s, b=24)
    # ed.encode()
    s = "乾兑乾乾乾乾乾乾巽震乾乾乾乾乾乾坎坤乾乾乾乾乾乾离震巽乾乾乾乾乾坎兑巽乾乾乾乾乾兑震巽乾乾乾乾乾兑坎巽乾乾乾乾乾巽坎巽乾乾乾乾乾震兑巽乾乾乾乾乾艮震巽乾乾乾乾乾巽坎巽乾乾乾乾乾乾坎巽乾乾乾乾乾震兑乾乾乾乾乾乾坎兑巽乾乾乾乾乾坤兑巽乾乾乾乾乾巽兑巽乾乾乾乾乾乾震巽乾乾乾乾乾坎兑巽乾乾乾乾乾坎坎巽乾乾乾乾乾坤坎巽乾乾乾乾乾乾坎巽乾乾乾乾乾坤艮巽乾乾乾乾乾震坎巽乾乾乾乾乾坤艮巽乾乾乾乾乾离兑巽乾乾乾乾乾巽坤巽乾乾乾乾乾震兑巽乾乾乾乾乾坎坤乾乾乾乾乾乾巽兑巽乾乾乾乾乾艮震巽乾乾乾乾乾震兑乾乾乾乾乾乾坎兑巽乾乾乾乾乾坤兑巽乾乾乾乾乾巽兑巽乾乾乾乾乾乾震巽乾乾乾乾乾坎兑巽乾乾乾乾乾坎坎巽乾乾乾乾乾坤坎巽乾乾乾乾乾乾坎巽乾乾乾乾乾坤艮巽乾乾乾乾乾震坎巽乾乾乾乾乾坤艮巽乾乾乾乾乾离兑巽乾乾乾乾乾巽坤巽乾乾乾乾乾震兑巽乾乾乾乾乾坎坤乾乾乾乾乾乾兑坎巽乾乾乾乾乾兑兑巽乾乾乾乾乾坤艮巽乾乾乾乾乾震震巽乾乾乾乾乾艮震巽乾乾乾乾乾离震巽乾乾乾乾乾震兑乾乾乾乾乾乾离震乾乾乾乾乾乾坎坤乾乾乾乾乾乾乾坤巽乾乾乾乾乾兑兑巽乾乾乾乾乾巽坎巽乾乾乾乾乾坤艮巽乾乾乾乾乾震震巽乾乾乾乾乾艮震巽乾乾乾乾乾离震巽乾乾乾乾乾震兑乾乾乾乾乾乾坎乾巽乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾离乾巽乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾乾震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾乾坤乾乾乾乾乾乾离乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾兑震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾兑乾巽乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坤震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾巽坤乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾乾坤乾乾乾乾乾乾离乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾兑震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾乾震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾艮乾巽乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎乾巽乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾乾震乾乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾巽坤乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾巽震乾乾乾乾乾乾离乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾兑乾巽乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震乾巽乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾乾坤乾乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾艮震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾离乾巽乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坤震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾巽坤乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坎乾巽乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾震乾巽乾乾乾乾乾离乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾巽乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾巽乾巽乾乾乾乾乾艮震乾乾乾乾乾乾坎兑乾乾乾乾乾乾巽坤乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾乾坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾坎震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎乾巽乾乾乾乾乾离乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾离乾巽乾乾乾乾乾巽坤乾乾乾乾乾乾坎兑乾乾乾乾乾乾震震乾乾乾乾乾乾坎乾巽乾乾乾乾乾坎兑乾乾乾乾乾乾坎坤乾乾乾乾乾乾兑兑巽乾乾乾乾乾坤震巽乾乾乾乾乾震兑乾乾乾乾乾乾乾震乾乾乾乾乾乾乾震乾乾乾乾乾乾乾震乾乾乾乾乾乾巽震乾乾乾乾乾乾乾震巽乾乾乾乾乾坤坎巽乾乾乾乾乾兑震巽乾乾乾乾乾坎坤乾乾乾乾乾乾离震巽乾乾乾乾乾震兑巽乾乾乾乾乾震兑乾乾乾乾乾乾乾震乾乾乾乾乾乾巽震乾乾乾乾乾乾乾震巽乾乾乾乾乾坤坎巽乾乾乾乾乾兑震巽乾乾乾乾乾坎震巽乾乾乾乾乾兑兑巽乾乾乾乾乾巽坎巽乾乾乾乾乾巽兑巽乾乾乾乾乾离兑巽乾乾乾乾乾坎坤乾乾乾乾乾乾震坎巽乾乾乾乾乾兑震巽乾乾乾乾乾震兑乾乾乾乾乾乾艮震乾乾乾乾乾乾坎坤乾乾乾乾乾乾兑坎巽乾乾乾乾乾艮兑巽乾乾乾乾乾坤坤乾乾乾乾乾乾艮震巽乾乾乾乾乾坤坎乾乾乾乾乾乾坎坎巽乾乾乾乾乾坤坎巽乾乾乾乾乾艮兑巽乾乾乾乾乾震坎乾乾乾乾乾乾坎震巽乾乾乾乾乾兑兑巽乾乾乾乾乾巽坎巽乾乾乾乾乾巽兑巽乾乾乾乾乾离兑巽乾乾乾乾乾震坎乾乾乾乾乾乾坤震巽乾乾乾乾乾坤震巽乾乾乾乾乾坤震巽乾乾乾乾乾坤坎乾乾乾乾乾乾坤坎乾乾乾乾乾乾离坤乾乾乾乾乾乾艮震巽乾乾乾乾乾乾震巽乾乾乾乾乾兑震巽乾乾乾乾乾兑震巽乾乾乾乾乾乾坎巽乾乾乾乾乾"
    ed = EightDiagrams(ciphertext=s, b=24)
    ed.decode()
