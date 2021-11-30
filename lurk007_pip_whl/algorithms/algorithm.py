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


@lissen_time
@logger
def main():
    s = '春天来了，春姑娘提着一篮子鲜花来到了小草的身旁，她摸过的地方都变成绿色了。小草就在春风中生长，嫩绿的新叶挂满枝头。' \
        '春姑娘刚走，热情的夏哥哥就来了。他一来，大地就被烤的炙热炙热的，小草都快被烤焦了。这个时候，人们最喜欢吃西瓜了！小草有了充分的水分，所以长得更绿了，为夏天添上了一抹碧绿。' \
        '夏哥哥刚要离开，秋妈妈就随着秋风飘来了。小草都变成金黄金黄的了，树上成熟的果子都噼里啪啦掉了下来，准备过冬的小动物们都来采摘新鲜的果子啦！' \
        '秋妈妈刚准备与我们再见，冬爷爷就乘着一阵寒风过来了。天上的雪花像云朵一样飘了下来，像棉被一样盖在小草上面，静静地等着第二年的春天。当第二年春天来临的时候，小草又从泥土里伸出头来了。这真如唐朝大诗人白居易说的野火烧不尽，春风吹又生呀！'
    ed = EightDiagrams(plaintext=s, b=18)
    mw = ed.encode()
    mingwen = ed.decode()
    return mw, mingwen


if __name__ == '__main__':
    """"""
    main()
