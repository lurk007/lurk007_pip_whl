import hashlib
import base64

# 编码解码
from lurk007_pip_whl.decorators.decorators import log


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
        assert self.__bit % 6 == 0, 'bit必须是12的倍数'
        self.__ciphertext = ciphertext
        self.__plaintext = plaintext
        # self.__keys = ['000', '001', '010', '011', '100', '101', '110', '111']
        self.__keys = ['000', '001', '010', '011', '100', '101', '110', '111'] + [F'{i}' for i in range(99)]
        # self.__values = ['🗜', 'Æ', 'Ì', 'Ü', 'Ù', 'Õ', '.', '🕒']
        self.__values = [chr(i) for i in range(5010, 20000 + 99)]
        # self.__values = [chr(110000), chr(100100), chr(100009), chr(100600), chr(102000), chr(100200), chr(100040), chr(100001)]
        # self.__values = ['坤', '震', '坎', '兑', '艮', '离', '巽', '乾']
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


# @timer
@log
def main():
    s = '春天来了，春姑娘提着一篮子鲜花来到了小草的身旁，她摸过的地方都变成绿色了。小草就在春风中生长，嫩绿的新叶挂满枝头。' \
        '春姑娘刚走，热情的夏哥哥就来了。他一来，大地就被烤的炙热炙热的，小草都快被烤焦了。这个时候，人们最喜欢吃西瓜了！小草有了充分的水分，所以长得更绿了，为夏天添上了一抹碧绿。' \
        '夏哥哥刚要离开，秋妈妈就随着秋风飘来了。小草都变成金黄金黄的了，树上成熟的果子都噼里啪啦掉了下来，准备过冬的小动物们都来采摘新鲜的果子啦！' \
        '秋妈妈刚准备与我们再见，冬爷爷就乘着一阵寒风过来了。天上的雪花像云朵一样飘了下来，像棉被一样盖在小草上面，静静地等着第二年的春天。当第二年春天来临的时候，小草又从泥土里伸出头来了。这真如唐朝大诗人白居易说的野火烧不尽，春风吹又生呀！'
    ed = EightDiagrams(plaintext=s, b=18)
    mw = ed.encode()
    mingwen = ed.decode()
    return mw, mingwen
    # s = '𘛈𘚡𘣸𚶰𚶰𘛈𘚡𘚡𘛈𘝨𘚩𘚡𘹰𚶰𘚡𘚡𘚡𘚡𚶰𘚩𘛈𘚡𘚡𘚡𘚩𘜄𘛈𘚡𘚡𘚡𘛈𘜄𘛈𘚡𘚡𘚡𘣸𘣸𘛈𘚡𘚡𘚡𘝨𘜄𘛈𘚡𘚡𘚡𘜄𘣸𘚡𘚡𘚡𘚡𚶰𘹰𘣸𘝨𚶰𘚡𘚡𘛈𚶰𘛈𘚩𘚡𘛈𚶰𘚡𘝨𘚩𘚡𘜄𘛈𘹰𘣸𘛈𘛈𘚩𘣸𘚡𘹰𘜄𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚩𚶰𘚡𘜄𘚩𘚡𘚩𘛈𘚡𚶰𘣸𘚡𚶰𘣸𘹰𘚡𚶰𘚡𘹰𘚩𘛈𘚡𚶰𘚡𘜄𘛈𚶰𘚡𘛈𘛈𘹰𚶰𘚡𘚡𘚡𘚡𚶰𘚩𘛈𘚡𘚡𘚡𘚩𘜄𘛈𘚡𘚡𘚡𘛈𘜄𘛈𘚡𘚡𘚡𘣸𘣸𘛈𘚡𘚡𘚡𘣸𘚩𘛈𘚡𘚡𘚡𘜄𘣸𘚡𘚡𘚡𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘜄𚶰𘚩𘚡𘛈𘹰𘝨𘚡𘹰𘜄𘚡𘚩𘚡𘛈𘜄𘚩𘚡𘚩𚶰𘛈𘹰𚶰𘚡𘝨𚶰𘝨𚶰𘣸𘚡𚶰𘝨𚶰𘚩𘚡𘛈𚶰𘣸𘣸𘣸𘚩𘚡𘚩𘹰𘣸𘹰𘜄𘚡𘚡𘝨𘣸𘝨𘚩𘚡𘝨𘚡𘜄𘣸𘚩𘚡𚶰𘹰𘣸𘹰𚶰𘚡𘛈𘹰𚶰𚶰𘚡𘛈𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘣸𘜄𘣸𘣸𘚩𘚡𘝨𚶰𚶰𘚡𘚩𘚡𘚡𚶰𘣸𚶰𘣸𘚡𘣸𘛈𚶰𘚡𘛈𘛈𚶰𘹰𘣸𘹰𘚩𘚡𘚩𘣸𘹰𘜄𘜄𘚡𘜄𘛈𘹰𚶰𘣸𘚡𘚡𘛈𚶰𘛈𘚩𘚡𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘛈𘹰𘚡𘚡𘚩𘚡𘜄𘜄𚶰𘝨𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘜄𘚡𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘛈𘚩𘣸𘣸𘚩𘚡𘚩𘣸𘚡𘹰𘜄𘚡𘣸𘜄𘛈𚶰𘚩𘚡𘣸𘛈𘝨𚶰𘣸𘚡𘣸𘚩𘣸𘚩𚶰𘚡𘹰𘝨𘚩𚶰𘚩𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘛈𘚩𘣸𘣸𘚩𘚡𘚩𘣸𘚡𘹰𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘜄𘛈𚶰𘚩𘚡𘣸𘛈𘝨𚶰𘣸𘚡𘣸𘚩𘣸𘚩𚶰𘚡𘚡𘚡𘚩𘹰𚶰𘚡𘛈𘛈𘚩𘚩𚶰𘚡𘚡𘜄𘣸𘹰𘚩𘚡𘛈𘹰𘚩𘹰𘛈𘛈𘛈𘹰𘚩𘹰𘛈𘛈𘣸𘛈𘣸𚶰𚶰𘛈𘝨𘣸𘚩𘹰𘛈𘛈𘝨𘛈𘚡𚶰𘣸𘚡𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘚡𘚩𘣸𘹰𘚩𘚡𘜄𘝨𘹰𘹰𚶰𘚡𚶰𘜄𘚡𘣸𘜄𘚡𘚡𘚡𘚡𚶰𘣸𘚡𘹰𘚩𘝨𘣸𘚡𘛈𘛈𘛈𘹰𘣸𘜄𘚡𚶰𘛈𘹰𘚡𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚩𘣸𘚩𘹰𘜄𘚡𘹰𘛈𘚡𚶰𘣸𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚡𘹰𘹰𘣸𘛈𘛈𚶰𘜄𘚡𘣸𘜄𘚡𘚡𘚡𘚡𚶰𘣸𘚡𘚩𘜄𘣸𘹰𘜄𘚡𘛈𘝨𘝨𚶰𘣸𘚡𚶰𘛈𘹰𘚡𘚩𘚡𘛈𘜄𘝨𘛈𘚡𘛈𘝨𘚩𘹰𘹰𘛈𘛈𘣸𘚡𘝨𘹰𚶰𘚡𘝨𘛈𘚡𚶰𘣸𘚡𘛈𘚩𘣸𘣸𘚩𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𚶰𘚡𚶰𚶰𘚡𘛈𘜄𘛈𘹰𘣸𘛈𘛈𘝨𘝨𚶰𘚩𘚩𘚡𘚩𘜄𘚡𘹰𘛈𘛈𘚡𘚡𘚡𚶰𘣸𘚡𘚡𘚡𘚩𘹰𚶰𘚡𘚡𘹰𘛈𚶰𘣸𘚡𘛈𘜄𘚡𘜄𘚩𘚡𚶰𘜄𘚡𘛈𚶰𘚡𚶰𘜄𘚡𘛈𚶰𘚡𘣸𘚩𘜄𘚡𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘛈𘚡𚶰𘣸𘚡𘛈𘚩𘛈𘜄𘚡𘚩𘚡𘣸𘚩𘹰𚶰𘣸𘚡𘛈𘝨𘚡𘛈𘜄𘚡𘜄𘛈𘚡𚶰𘣸𘚡𚶰𘚡𘣸𘣸𘚩𘚡𘜄𘚡𚶰𘚡𘚩𘚡𘝨𘹰𘚡𘛈𘚩𘚡𘚡𘛈𘜄𘣸𘚩𘚡𘚡𘛈𘜄𘣸𘚩𘚡𘹰𘛈𚶰𘣸𚶰𘚡𘛈𘚡𘣸𚶰𚶰𘛈𘜄𘣸𘚩𘝨𘚩𘚡𘚡𘝨𘚩𘚩𘚩𘚡𘣸𘹰𘜄𘹰𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘹰𘝨𘜄𘛈𘛈𘚡𘜄𘜄𘝨𘜄𘚡𘚡𘹰𘛈𘝨𘜄𘚡𚶰𘚡𚶰𘚡𘛈𘛈𘚩𘣸𘚩𘹰𘜄𘚡𘚩𚶰𘹰𘚡𘛈𘛈𘣸𘚩𘹰𚶰𘣸𘚡𘛈𘚩𘛈𘛈𚶰𘚡𘚡𘚩𘝨𘛈𘚩𘚡𚶰𘛈𘚡𘜄𘚩𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘚩𘜄𘚡𘚩𘚡𚶰𘚡𚶰𚶰𘚡𘛈𚶰𘚡𘣸𘣸𘚩𘚡𘜄𘚡𚶰𘚡𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚩𘣸𘚩𘹰𘜄𘚡𘹰𘛈𘚡𚶰𘣸𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘛈𘛈𘜄𘛈𘜄𘚡𘹰𚶰𘚡𘚡𘚡𘚡𚶰𘚩𘛈𘚡𘚡𘚡𘚩𘜄𘛈𘚡𘚡𘚡𘛈𘜄𘛈𘚡𘚡𘚡𘣸𘣸𘛈𘚡𘚡𘚡𘝨𘜄𘛈𘚡𘚡𘚡𘜄𘣸𘚡𘚡𘚡𘚡𘜄𘣸𘚩𘝨𘚩𘚡𘝨𘚩𘚩𘝨𘚩𘚡𘣸𘛈𚶰𘚡𘛈𘛈𘣸𚶰𘛈𘹰𘚩𘚡𘹰𚶰𘚡𘚡𘚡𘚡𚶰𘚩𘛈𘚡𘚡𘚡𘚩𘜄𘛈𘚡𘚡𘚡𘛈𘜄𘛈𘚡𘚡𘚡𘣸𘣸𘛈𘚡𘚡𘚡𘣸𘚩𘛈𘚡𘚡𘚡𘜄𘣸𘚡𘚡𘚡𘚡𘚩𚶰𘹰𘚡𘛈𘛈𘚡𘝨𘚩𘚩𘚩𘚡𘣸𘹰𘜄𘹰𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𚶰𘹰𘜄𘚡𚶰𘚡𘚡𘝨𘚡𘛈𘜄𘚡𘝨𘛈𘚡𚶰𘣸𘚡𘛈𘝨𘚡𘣸𘜄𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘜄𘚡𘝨𚶰𘣸𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘚡𘹰𚶰𘛈𘛈𘛈𘝨𚶰𘚡𘛈𘛈𘣸𘚡𘹰𚶰𘛈𘛈𘛈𘝨𚶰𘚡𘛈𘛈𘚡𘝨𘚡𘛈𘜄𘚡𘚡𘹰𚶰𘛈𘚩𘚡𘚩𚶰𘹰𘚡𘛈𘛈𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘚡𘹰𘹰𘣸𘛈𘛈𘜄𘛈𘹰𘣸𘛈𘛈𘹰𘛈𚶰𘣸𚶰𘚡𘚡𘚡𘚩𘹰𚶰𘚡𚶰𘛈𘝨𘹰𘛈𘛈𘛈𘜄𘚡𘜄𘚩𘚡𘚡𘛈𘜄𘣸𘚩𘚡𘚡𘛈𘜄𘣸𘚩𘚡𘹰𘛈𚶰𘣸𚶰𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚡𘚡𘣸𚶰𘚩𘚡𘹰𚶰𘜄𘣸𚶰𘚡𘛈𘚡𘜄𘣸𘚡𘛈𘝨𘹰𘚡𘛈𘚩𘚡𘚩𘣸𘹰𘝨𘚩𘚡𘚩𘣸𘹰𘝨𘚩𘚡𚶰𘛈𘣸𘣸𘚩𘚡𘝨𘚡𘚡𘚡𘹰𘚡𚶰𚶰𘹰𚶰𚶰𘚡𚶰𘣸𘝨𘣸𚶰𘚡𘛈𚶰𘝨𘛈𘜄𘚡𘚡𘚡𘚡𚶰𘣸𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘝨𘛈𘚡𚶰𘣸𘚡𘹰𚶰𚶰𘜄𘜄𘚡𘛈𘚩𘣸𘣸𘚩𘚡𚶰𘛈𘣸𘣸𘚩𘚡𘝨𚶰𘚡𚶰𘣸𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘜄𘚡𘝨𚶰𘣸𘚡𚶰𚶰𘹰𚶰𚶰𘚡𘣸𘜄𘹰𘹰𘜄𘚡𚶰𘝨𘜄𚶰𘚩𘚡𚶰𚶰𘚩𘝨𘛈𘛈𘚩𘣸𘹰𚶰𘣸𘚡𘚡𘚡𘛈𘛈𘜄𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘜄𘚡𘚡𘛈𘚩𘚡𘣸𘜄𘚡𘜄𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘜄𘚡𘚡𘛈𘚩𘚡𘚩𘚡𘚩𘚡𘚩𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘛈𘛈𘣸𘹰𘜄𘚡𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘛈𘚡𘣸𚶰𚶰𘛈𘜄𘚡𘝨𚶰𘣸𘚡𘣸𘹰𘹰𘝨𚶰𘚡𚶰𚶰𘚩𘣸𘚡𘛈𘹰𘚡𘚡𘝨𘚩𘚡𘝨𘣸𘣸𘚩𘜄𘚡𘣸𘹰𘜄𘝨𘚩𘚡𘚡𘚡𘣸𘹰𘜄𘚡𘣸𘚩𘹰𚶰𘣸𘚡𘝨𚶰𘝨𚶰𘣸𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘛈𘹰𘚡𘚡𘚩𘚡𘜄𘜄𚶰𘝨𘜄𘚡𘝨𘚩𘚡𚶰𘣸𘚡𘛈𘹰𚶰𚶰𘚡𘛈𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘜄𘣸𘣸𘚡𚶰𘚡𘣸𘣸𘹰𘚡𚶰𘚡𘹰𘚩𘝨𘣸𘚡𘛈𘹰𘚩𚶰𚶰𘚩𘚡𘚩𚶰𘹰𘚡𘛈𘛈𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘣸𘚡𘝨𘹰𚶰𘚡𘚩𘚩𘹰𘚡𚶰𘚡𘛈𘹰𘝨𘚡𚶰𘚡𘚩𘚩𘹰𘚡𚶰𘚡𘛈𘹰𘝨𘚡𚶰𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘣸𘣸𘹰𘚡𚶰𘚡𘹰𘚩𘝨𘣸𘚡𘛈𘛈𘜄𘚡𘜄𘚩𘚡𘚡𘜄𘣸𘹰𘚩𘚡𚶰𘣸𘣸𘣸𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚩𘣸𘚩𘹰𘜄𘚡𘚡𘚡𘚡𚶰𘣸𘚡𘜄𘝨𘹰𚶰𘣸𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘛈𘜄𘚡𘜄𘚩𘚡𘚩𘣸𘹰𘝨𘚩𘚡𘚩𘣸𘹰𘝨𘚩𘚡𚶰𘛈𘣸𘣸𘚩𘚡𘣸𘚡𘝨𘹰𚶰𘚡𘚩𘚡𘹰𘚡𘜄𘚡𘚩𘚩𘹰𘚡𚶰𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘚡𘜄𘚩𘜄𘚡𘛈𘝨𘹰𘚡𘛈𘚩𘚡𘚡𘹰𘚡𘚩𘚩𘚡𘛈𘝨𚶰𘣸𘚩𘚡𘚩𘣸𘚡𘹰𘜄𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘣸𘜄𘣸𘣸𘚩𘚡𘚩𘹰𘜄𘹰𘜄𘚡𘛈𘣸𘹰𚶰𘜄𘚡𘝨𘚡𘣸𘛈𘜄𘚡𘜄𘜄𚶰𘛈𘚩𘚡𘚡𘜄𘜄𘝨𘜄𘚡𘣸𘚡𘝨𘹰𚶰𘚡𚶰𚶰𘹰𚶰𚶰𘚡𘛈𘚩𘹰𘚩𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𚶰𚶰𘚩𘝨𘛈𘛈𚶰𘹰𘣸𘝨𚶰𘚡𘚩𘚩𘚡𚶰𘣸𘚡𘜄𘛈𘹰𘣸𘛈𘛈𘚩𘣸𘚡𘹰𘜄𘚡𘚡𘚩𘣸𘹰𘚩𘚡𘛈𘜄𘚡𘜄𘚩𘚡𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘝨𘚡𘚡𘚡𘹰𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘝨𘜄𘛈𘛈𘚡𘛈𚶰𚶰𘹰𚶰𚶰𘚡𘚡𘝨𘚡𘛈𘜄𘚡𘚡𘹰𚶰𘛈𘚩𘚡𘚩𚶰𘹰𘚡𘛈𘛈𘛈𚶰𘜄𘝨𘜄𘚡𘚡𘜄𘣸𘹰𘚩𘚡𘣸𘚡𘝨𘹰𚶰𘚡𚶰𘚡𚶰𚶰𘚡𘛈𘚡𚶰𘛈𘝨𘜄𘚡𘛈𚶰𘚩𘣸𘚩𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘛈𘚡𚶰𘝨𘜄𘚡𘹰𘚩𘝨𚶰𘚡𘛈𘣸𘚡𘝨𘹰𚶰𘚡𘛈𘛈𘚩𘛈𘚡𘛈𚶰𘛈𘚡𘜄𘚩𘚡𘜄𘚡𘝨𚶰𘣸𘚡𘚡𘜄𘚡𘛈𘚩𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘛈𘜄𘝨𘛈𘚡𘛈𘣸𘹰𘝨𘜄𘛈𘛈𘚡𘝨𘚩𘚩𘚩𘚡𘜄𘚩𚶰𘚩𚶰𘚡𘚡𘚡𘚡𚶰𘣸𘚡𘚡𘚡𘚩𘹰𚶰𘚡𘚡𘝨𚶰𘛈𘜄𘚡𘚡𘹰𘚡𘚩𘚩𘚡𘛈𘝨𚶰𘣸𘚩𘚡𘚩𘣸𘚡𘹰𘜄𘚡𘣸𘛈𘣸𚶰𚶰𘛈𘜄𘚡𘝨𚶰𘣸𘚡𘚩𘣸𘚩𘹰𘜄𘚡𘛈𘚩𘣸𘣸𘚩𘚡𘚩𘣸𘚡𘹰𘜄𘚡'
    # ed = EightDiagrams(ciphertext=s, b=18)
    # ed.decode()


if __name__ == '__main__':
    """"""
    # print([chr(i) for i in range(127, 127 + 99)])
    main()
