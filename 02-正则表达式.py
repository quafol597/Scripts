"""
compile         根据包含正则表达式的字符串创建模式对象
search          在字符串中寻找模式
match           在字符串的开始处匹配模式
split           根据模式的匹配项来分割字符串
findall         列出字符串中模式的所有匹配项
sub             将字符串中所有的pat的匹配项用repl替换
escape          将字符串中所有特殊正则表达式字符转义

.   表示任意字符
^   表示字符串开头
$   表示字符串结尾
\   特殊字符转义
[]  匹配一个字符, 特殊字符失去意义(除了 ^ - ] \)
|   或者, 如果未在()中, 则包含整个表达式

贪婪匹配: 取max
*   重复匹配前一个字符(0~无限)次
+   重复匹配前一个字符(1~无限)次
?   重复匹配前一个字符(0~1)次

非贪婪匹配: 取min下面三种的匹配次数分别(0, 1, 0, m)
*? / +? / ?? / {m, n}?

\A	只在字符串开头进行匹配。
\b	匹配位于开头或者结尾的空字符串
\B	匹配不位于开头或者结尾的空字符串
\d	匹配任意十进制数，相当于 [0-9]
\D	匹配任意非数字字符，相当于 [^0-9]
\s	匹配任意空白字符，相当于 [ \t\n\r\f\v]
\S	匹配任意非空白字符，相当于 [^ \t\n\r\f\v]
\w	匹配任意数字和字母，相当于 [a-zA-Z0-9_]
\W	匹配任意非数字和字母的字符，相当于 [^a-zA-Z0-9_]
\Z	只在字符串结尾进行匹配

"""
import re

a = 'ab123cd'
print(re.sub('\d+', '222', a))  # ab222cd
print(re.split('\d+', a))  # ['ab', 'cd']
print(re.findall('\d+', a))  # ['123']
print(re.match('\d+', a))  # None match会从头匹配
print('='*50)

# re.Match实例的四种方法
re_match = re.search('\d+', a)  # <re.Match object; span=(2, 5), match='123'>
print(re_match.group())  # 123
print(re_match.span())  # (2, 5)
print(re_match.start())  # 2
print(re_match.end())  # 5
print('='*50)


b = 'ab123cd'
re_match2 = re.match('ab(?P<num>\d+)(?P<alp>[a-z]+)', b)
print(re_match2.group())  # ab123cd
print(re_match2.group(1))  # 123
print(re_match2.group('num'))  # 123
print(re_match2.group('alp'))  # cd
print('='*50)

c = '  abc'
re_match3 = re.match('\s*abc', c)
print(re_match3.group())  #   abc
print('='*50)

text = "JGood is a handsome boy, he is cool, clever, and so on..."
regex = re.compile('\w*oo\w*')  # re.Pattern: re.compile('\\w*oo\\w*')
print(regex.findall(text))
re_match4 = re.findall('\w*oo\w*', text)
print(re_match4)
print('='*50)


"""简易计算器"""
def f1(ex):
    return eval(ex)  #测试用 真实中要自己编写四则运算

a = '1*2+(5/6)+(12*23)/15'
while True:
    ret = re.split('\(([^()]+)\)', a, 1)
    if len(ret) == 3:
        a,b,c = re.split('\(([^()]+)\)', a, 1)
        rec = f1(b)
        a = a + str(rec) + c
    else:
        red = f1(a)
        print(red)
        break


"""计算器"""
def md(date_list,symbol):
    '''

    :param date_list: 匹配到的表达式
    :param symbol: 符号
    :return: 乘数计算得到的值
    '''
    a = date_list.index(symbol)  #取到符号
    if symbol == '*' and date_list[a + 1] != '-': #如果是乘号并且索引的下一个位置不是负号计算
        k = float(date_list[a - 1]) * float(date_list[a + 1])
    elif symbol == '/' and date_list[a + 1] != '-':  #如果是除号并且索引的下一个位置不是负号计算
        k = float(date_list[a - 1]) / float(date_list[a + 1])
    elif symbol == '*' and date_list[a + 1] == '-': #如果是乘号并且索引的下一个位置是负号计算
        k = -(float(date_list[a - 1]) * float(date_list[a + 2]))
    elif symbol == '/' and date_list[a + 1] == '-': #如果是除号并且索引的下一个位置是负号计算
        k = -(float(date_list[a - 1]) / float(date_list[a + 2]))
    del date_list[a - 1], date_list[a - 1], date_list[a - 1] #删除列表里参与计算的索引位置
    date_list.insert(a - 1, str(k))  #把新的值插入到列表中
    return date_list

#处理混乱的四则，按照先算加减后乘除的原则
def fun(s):
    '''

    :param s: 去除括号后的表达式
    :return: 表达式的返回值
    '''
    list_str = re.findall('([\d\.]+|/|-|\+|\*)',s) #匹配表达式
    sum=0
    while 1:
        if '*' in list_str and '/' not in list_str:  #判断乘是否在表达式内
            md(list_str, '*')
        elif '*' not in list_str and '/' in list_str: #判断乘是否在表达式内
            md(list_str, '/')                   #调用md函数处理除号
        elif '*' in list_str and '/' in list_str:
            a = list_str.index('*')
            b = list_str.index('/')
            if a < b:
                md(list_str, '*')
            else:
                md(list_str, '/')
        else:
            if list_str[0]=='-':   #判断是否是负号
                list_str[0]=list_str[0]+list_str[1]
                del list_str[1]
            sum += float(list_str[0])
            for i in range(1, len(list_str), 2):
                if list_str[i] == '+' and list_str[i + 1] != '-':
                    sum += float(list_str[i + 1])
                elif list_str[i] == '+' and list_str[i + 1] == '-':
                    sum -= float(list_str[i + 2])
                elif list_str[i] == '-' and list_str[i + 1] == '-':
                    sum += float(list_str[i + 2])
                elif list_str[i] == '-' and list_str[i + 1] != '-':
                    sum -= float(list_str[i + 1])
            break
    return sum



a='1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )'

#循环去除括号
while True:
    ret = re.split('\(([^()]+)\)', a, 1)
    if len(ret) == 3:
        a,b,c = re.split('\(([^()]+)\)', a, 1)
        rec = fun(b)
        a = a + str(rec) + c

    else:
        red = fun(a)
        print(red)
        break
