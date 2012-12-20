#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   12/12/20 10:00:07
#   Desc    :   使用google进行英汉汉英翻译
#
import sys
import urllib2, urllib

class Translate(object):
    """ 使用google进行英->汉, 汉->英的翻译 """
    def __init__(self, text, src='zh-CN', dst = 'en'):
        self.url = 'http://translate.google.cn/translate_a/t'
        self.params = dict(client = "t", text=text,
                           hl = 'zh-CN', tl = dst,
                           multires = '1', prev = 'btn',
                           ssel = '0', sc = '1')
        if src != self.params.get('hl'):
            self.params.update(sl = src)

        return

    def loads(self, content):
        """ 加载翻译结果 """
        while ',,' in content:
            content = content.replace(',,', ',"",')
            content = content.replace('[,', '["",')
            #content = content.replace(',]', '"",]')
        content = eval(content)
        result = content[0][0]
        desc = content[1]
        pinyin = result[2] if result[2] else result[3]
        others = ''
        for d in desc:
            others += d[0] + '\n'
            for i in d[1]:
                others += "\t{0}\t".format(i)
                for s in d[2]:
                    if s[0] == i:
                        others +=','.join(s[1]) + '\n'
        r = dict(
            result = result[0],
            source = result[1],
            pinyin = pinyin,
            others = others,
        )
        return r

    def translate(self):
        """ 调用google翻译 """
        params = urllib.urlencode(self.params)
        req = urllib2.Request(self.url, params)
        req.add_header("User-Agent",
                       "Mozilla/5.0+(compatible;+Googlebot/2.1;"
                       "++http://www.google.com/bot.html)")
        res = urllib2.urlopen(req)
        result =  res.read()
        return self.loads(result)

def auto_translate(text):
    """ 自动检测当前语言进行翻译 """
    text = text.decode('utf-8')
    if text[0] > u'z':
        src = 'zh-CN'
        dst = 'en'
    else:
        src = 'en'
        dst = 'zh-CN'
    t = Translate(text.encode('utf-8'), src, dst)
    result = t.translate()
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = "Google Translate With Command")
    parser.add_argument("-o", "--only", action = "store_true", dest = "only",
                     default = False, help="Only Show Result")
    parser.add_argument("-zh2en", action = "store_const", dest = "lang",
                        default=False, const = "zh",
                        help = "Translate Chinese to English")
    parser.add_argument("-en2zh", action = "store_const", dest="lang",
                        default = False, const="en",
                        help = "Translate English to Chinese")
    parser.add_argument(dest = "content")
    arg = parser.parse_args()
    if arg.lang == "en":
        t = Translate(arg.content, "en", "zh-CN")
        result = t.translate()
    elif arg.lang == "zh":
        t = Translate(arg.content, "zh-CN", "en")
        result = t.translate()
    else:
        result = auto_translate(arg.content)
    if arg.only:
        print result.get("result")
        sys.exit(0)
    print "源词:", result.get("source")
    print "结果:", result.get("result")
    print "拼音:", result.get("pinyin")
    if result.get("others"):
        print "其他释义:"
        print result.get("others")
