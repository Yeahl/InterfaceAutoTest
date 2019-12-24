# coding=utf-8

import requests
import json


class Key:

    def __init__(self):
        # session管理
        self.session = requests.session()
        # 结果解析
        self.result = None
        self.jsonres = None
        # 保存基础uri
        self.uri = None
        # 保存关联数据的字典
        self.relations = {}

    def post(self, path, params=None):
        """
        http post请求
        :param path: 接口地址
        :param params: 请求参数（键对值及字典）
        :return:
        """
        params = self.__get_relations(params)
        self.result = self.session.post(self.__seturl(path), data=self.__getparams(params))
        self.jsonres = json.loads(self.result.text)
        print(self.jsonres)

    def addheaders(self, key, value):
        """
        构造 session 请求头
        :param key: 头的键值
        :param value: 头的值
        :return: 无
        """
        value = self.__get_relations(value)
        self.session.headers[key] = value

    def delheaders(self, key):
        """
        删除请求头
        :param key: 头的键值
        :return: 无
        """
        del self.session.headers[key]

    def seturi(self, uri):
        '''
        设置基础uri
        :param uri: uri地址
        :return: 基础uri
        '''
        self.uri = uri
        return self.uri

    def __seturl(self, path):
        """
        组装接口地址
        :param path: 接口路径
        :return: 接口地址
        """
        return self.uri + path

    def __getparams(self, params):
        """
        构造请求参数
        :param params: 字符串参数
        :return: 转换后的字典
        """
        if params is None or params == '':
            return None
        elif type(params) == dict:
            return params
        else:
            # 定义一个空字典用来保存处理后的数据
            params_dict = {}
            #分割参数字符串的键值对(name="张三"&pwd="123456")
            list_params = params.split('&')
            for items in list_params:
                # 如果键值对里面有'='，那么我们就取=左边为键，=右边为值
                # 主要是规范传值方式
                if items.find("=") >= 0:
                    params_dict[items[0:items.find('=')]] = items[items.find('=') + 1:]
                else:
                    # 如果没有=，处理为键，值为空
                    params_dict[items] = None
            return params_dict

    def savejson(self, key, param_name):
        """
        保存关联参数
        :param key: 保存json结果的键
        :param param_name: 保存后的参数名称
        :return:无
        """
        self.relations[param_name] = self.jsonres[key]

    def __get_relations(self, params):
        """
        替换关联的值
        :param params: 关联前的参数
        :return: 关联后的值
        """
        if params is None or params == '':
            return None
        else:
            #遍历保留关联参数的字典
            #将参数中存在{key}形式的字符串都替换为 relations 这个字典里面keys这个键的值
            for keys in self.relations:
                params = params.replace('{' + keys + '}', self.relations[keys])
        return params

if __name__ == '__main__':
    # 创建一个http请求库的实例对象
    k = Key()
    # 定义基础请求地址
    k.seturi('http://112.74.191.10:80/inter/HTTP/')
    # 获取token
    k.post('auth', '')
    #保存 token
    k.savejson('token', 'token')
    # 添加token到头里面
    # k.addheaders('token', k.jsonres['token'])
    k.addheaders('token', '{token}')
    # 登录
    k.post('login', 'username=Will&password=123456')
    # 保存userid
    k.savejson('userid', 'userid')
    # 获取用户信息
    # k.post('getUserInfo', 'id={}'.format(k.jsonres['userid']))
    k.post('getUserInfo', 'id={userid}')
    # 退出登录
    k.post('logout')
    print("========================注册用户========================")
    # 获取token
    k.post('auth', '')
    # 添加token到头里面
    k.addheaders('token', k.jsonres['token'])
    # 删除头
    # k.delheaders('token')
    # 注册用户
    k.post('/register', 'username=sanshia&pwd=123456&nickname=sanshia&describe=sanshia')
    # 登录
    k.post('login', 'username=sanshia&password=123456')
    # 获取用户信息
    k.post('getUserInfo', 'id={}'.format(k.jsonres['userid']))
    # 退出登录
    k.post('logout')
