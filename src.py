# encoding=UTF-8
'''
Created on 2017年2月17日

@author: 27999
'''
from PIL import Image
import sys
import requests
import codecs
from bs4 import BeautifulSoup
import os
import tempfile
import msvcrt
import random
import time
def logoin(user,pw,headers,URL):
    session=requests.session()   
    session.get('http://electsys.sjtu.edu.cn/edu/',headers=headers)
    html=BeautifulSoup(session.get('http://electsys.sjtu.edu.cn/edu/login.aspx',headers=headers).text,'html5lib')
    form_list=html.find('form',{'action':'ulogin'}).find_all('input',{'type':'hidden'})
    sid=form_list[0]['value']
    returl=form_list[1]['value']
    se=form_list[2]['value']
    v=form_list[3]['value']
    img_url=html.find('img',{'onclick':"this.src='captcha?'+Date.now()+Math.random()"})['src']
    open('picture.jpeg','wb').write(session.get(URL+img_url).content)
    m=Image.open('picture.jpeg')
    mode=True
    try:
        captcha=getText('picture.jpeg')
    except:
        mode=False
    m.show()
    if mode:
        print u'\n验证码:'+captcha+u'(正确回车跳过，错误输入正确的验证码)'
    else:
        print u'\n验证码:'
    cap=raw_input()
    m.close()
    if cap !='':
        captcha=cap
    data={
        'user':user,
        'pass':pw,
        'captcha':captcha,
        'sid':sid,
        'returl':returl,
        'se':se,
        'v':v
        }
    session.post('https://jaccount.sjtu.edu.cn/jaccount/ulogin',data,headers=headers)
    html=BeautifulSoup(session.get(URL+'jalogin?'+'sid='+sid+'&returl='+returl+'&se='+se+'&v='+v,headers=headers).text,'html5lib')
    try:
        url=html.find('meta',{'http-equiv':'refresh'})['content'].split('url=')[1]
    except Exception:
        return session,0
    session.get('http://electsys.sjtu.edu.cn/edu/login.aspx'+url,headers=headers)
    session.get('http://electsys.sjtu.edu.cn/edu/login.aspx',headers=headers)
    session.get('http://electsys.sjtu.edu.cn/edu/student/sdtinfocheck.aspx',headers=headers)
    time.sleep(0.3)
    res=session.get('http://electsys.sjtu.edu.cn/edu/student/sdtleft.aspx',headers=headers)
    try:
        
        html=BeautifulSoup(res.text,'html5lib')
#        print html
        name=html.find('span',{'id':'lblXm'}).getText()
        major=html.find('span',{'id':'lblZy'}).getText()
        year=html.find('span',{'id':'lblXn'}).getText()
        t=html.find('span',{'id':'lblXq'}).getText()
        print u'Welcome !'
        print u'{name}'.format(name=name)
        print u'{major}'.format(major=major)
        print u'{year}'.format(year=year)
        print u'{t}'.format(t=t)
        print u'------'
        print u'登陆成功 !'
        print u''
        print u'------'
        return session,1
    except:
        return session,2
    

def getText(name):
    tmpfile = tempfile.NamedTemporaryFile(prefix="tess_")
    output_file_name_base=tmpfile.name
    output_file_name = '%s.txt' % output_file_name_base
    oscommand=sys.path[0]+'/Tesseract-OCR/tesseract '+name+' '+output_file_name_base
    os.system(oscommand)
    f = open(output_file_name)
    return f.read().strip()

def pwd_input():
    chars=[]
    while True:
        try:
            new_char=msvcrt.getch().decode(encoding="utf-8")
        except:
            return ''
        if new_char in '\r\n':
            break
        elif new_char=='\b':
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))
                msvcrt.putch( ' '.encode(encoding='utf-8'))
                msvcrt.putch('\b'.encode(encoding='utf-8'))
        else:
            chars.append(new_char)
            msvcrt.putch('*'.encode(encoding='utf-8'))
    return(''.join(chars))
                
Agent=[
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
    ]


def main():
    agent=random.choice(Agent)
    URL='https://jaccount.sjtu.edu.cn/jaccount/'
    headers={
        'User-Agent':agent,
        }
    f='y'
    while f=='y':
        f='n'
        print u'jaccount账户:'
        user=raw_input()
        print u'密码:'
#        pw=raw_input()
        pw=pwd_input()
        if pw=='':
            pw=raw_input()
        session,sta=logoin(user, pw, headers, URL)
        if sta==0:
            print u"登录失败,用户名，密码或验证码错误,重新登陆?(y/n)"
            f=raw_input()
            if f=='n':
                sys.exit()
        if sta==2:
            print u'登陆失败，其他因素，再次尝试?(y/n)'
            w=raw_input()
            if w=='n':
#                break
                sys.exit()
            else:
                f='y'
        if f!='y':
            break
    ddlXN=['2015-2016','2016-2017']
    ddlXQ=['1','2']
    txtDM=''
    btnSearch=" 查 询 "
    kc_kz='rdbKC'
    print u'等待5秒钟---'    
    time.sleep(5)
    for year in ddlXN:
        for t in ddlXQ:
            html=BeautifulSoup(session.get('http://electsys.sjtu.edu.cn/edu/StudentScore/StudentScoreQuery.aspx',headers=headers).text,'html5lib')
            __VIEWSTATE=html.find('input',{'id':'__VIEWSTATE'})['value']
            __VIEWSTATEGENERATOR=html.find('input',{'name':'__VIEWSTATEGENERATOR'})['value']
            __EVENTVALIDATION=html.find('input',{'name':'__EVENTVALIDATION'})['value']
            data={
                '__VIEWSTATE':__VIEWSTATE,
                '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
                '__EVENTVALIDATION':__EVENTVALIDATION,
                'ddlXN':year,
                'ddlXQ':t,
                'txtDM':txtDM,
                'btnSearch':btnSearch,
                'kc_kz':kc_kz
                }
            html=BeautifulSoup(session.post('http://electsys.sjtu.edu.cn/edu/StudentScore/StudentScoreQuery.aspx',data,headers=headers).text,'html5lib')
            try:
                courses=html.find('table',{'id':'dgScore'}).find('tbody').find_all('tr')
                with codecs.open(year+'_'+t+'.csv','wb',encoding='UTF-8') as fp:
                    for i in courses:
                        item=i.find_all('td')
                        mes=item[1].getText()+','+item[2].getText()+','+item[3].getText()+','+item[4].getText()+','+item[5].getText()+'\n'
                        fp.write(u'{mes}'.format(mes=mes)) 
                        print item[1].getText()+'\t'+item[2].getText()+'\t'+item[3].getText()+'\t'+item[4].getText()+'\t'+item[5].getText()
            except:
                print year+'_'+t+':An error occurs'
            time.sleep(1)
                
            

if __name__ == '__main__':
    main()
    os.system("pause")
