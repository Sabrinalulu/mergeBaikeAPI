#!/usr/bin/python
#coding:utf-8
# 本篇為Python3代碼
from urllib.request import urlopen
import urllib.parse
import urllib.error
import requests
from bs4 import BeautifulSoup

global redirect
global finalLinkZ
finalLinkZ=""
global finalLinkZ1
finalLinkZ1=""
global finalLinkZ2
finalLinkZ2=""
global infoLinkZ
infoLinkZ=""
global infoLinkZ1
infoLinkZ1=""
global infoLinkZ2
infoLinkZ2=""
redirect = "pageRedirects"
inputString = input("輸入要查詢的字詞：");
outputBaike = input("選擇要取用的百科資料(zhwiki,baidubaike,hudongbaike)：");
out = outputBaike.split(",");
prepare=[]
prepare.append(inputString);
prepare.extend(out);
print (prepare);

if "zhwiki" in prepare:
    # linkP = "http://zhishi.me/zhwiki/resource/"
    # linkZ = linkP+inputString
    # print linkZ
    linkP="http://zhishi.me/api/entity/"
    linkP_1="?baike="
    links1="<"+linkP+inputString+linkP_1+"zhwiki>"
    finalLinkZ=linkP+urllib.parse.quote(inputString)+linkP_1+"zhwiki"
    print ("A given entity:"+links1);
    print ("URL:"+finalLinkZ);

#     linkI="http://zhishi.me/api/entity/"
#     linkI_1="?property=infobox"
#     infoLinkZ=linkI+urllib.parse.quote(inputString)+linkI_1
#     print ("URL:"+infoLinkZ);

if "baidubaike" in prepare:
    linkP="http://zhishi.me/api/entity/"
    linkP_1="?baike="
    links2="<"+linkP+inputString+linkP_1+"baidubaike>"
    finalLinkZ1=linkP+urllib.parse.quote(inputString)+linkP_1+"baidubaike"
    print ("A given entity:"+links2);
    print ("URL:"+finalLinkZ1);

#     linkI="http://zhishi.me/api/entity/"
#     linkI_1="?property=infobox"
#     infoLinkZ1=linkI+urllib.parse.quote(inputString)+linkI_1
#     print ("URL:"+infoLinkZ1);

if "hudongbaike" in prepare:
    linkP="http://zhishi.me/api/entity/"
    linkP_1="?baike="
    links3="<"+linkP+inputString+linkP_1+"hudongbaike>"
    finalLinkZ2=linkP+urllib.parse.quote(inputString)+linkP_1+"hudongbaike"
    print ("A given entity:"+links3);
    print ("URL:"+finalLinkZ2);

#     linkI="http://zhishi.me/api/entity/"
#     linkI_1="?property=infobox"
#     infoLinkZ2=linkI+urllib.parse.quote(inputString)+linkI_1
#     print ("URL:"+infoLinkZ2);

def queryInfobox(s):

    try:
        strHtml = s
        revise = strHtml.replace("{","").replace("}","").replace("[","").replace("]","").replace("“”","")
        # print type(strHtml) string
        # 條列元素
        words = revise.split(",")
        print(words);
        for i in range(len(words)):
            print(words[i]);
            infoBo = urllib.request.urlopen(words[i]).read().decode('utf8');
            print(infoBo);

    except urllib.error.HTTPError as e:
        print(e.code);
        print(e.reason);
        print(e.geturl());
        print(e.read());

def queryRedirect(s):

    try:
        strHtml1 = urllib.request.urlopen(s).read().decode('utf8')
        revise1 = strHtml1.replace("{","").replace("}","").replace("[","").replace("]","").replace("“”","")
        #print revise1 將讀到的資料做處理才能進一步用逗號分開，而不是一串很長的字串
        words1 = revise1.split(",")
        #print(type(words1)); list
        for i in range(len(words1)):
            print(words1[i]);
            if redirect in words1[i]:
                newLine =words1[i].lstrip('"pageRedirects": ').rstrip('""')
                print(newLine);
                http = newLine.split("resource/");
                print (http[1]);
                wholeHttp = http[0]+ "resource/" + urllib.parse.quote(http[1]);
                print (wholeHttp);
                resp = requests.get(wholeHttp);
                soup = BeautifulSoup(resp.text, 'html.parser');
#                 print(soup);
                rows = soup.find('table', {'cellspacing': 4});
#     Since None is the sole singleton object of NoneType in Python, we can use is operator to check if a variable has None in it or not.
                if rows is None:
                    print ("Not found!");
                else:
                    rows1 = soup.find('div',{'style':"font-size:14px;"});
                    rowTR = rows.find_all('tr');
#                 print (rowTR[0]);
                    print ("\nAbstract: \n");
                    print (rows1.text);
                    print ("InfoBox: \n");
                    for i in range(len(rowTR)):
                        value = rowTR[i].text;
                        print (value);
#                 strHtml2 = urllib.request.urlopen(wholeHttp).read();
#                 #完整html網站有排版，如果不加decode()就會亂碼、沒縮排
#                 c = strHtml2.decode('utf8');

    except urllib.error.HTTPError as e:
        print(e.code);
        print(e.reason);
        print(e.geturl());
        print(e.read());


if finalLinkZ=="" and finalLinkZ1=="":
    print ("\n[互動百科]\n");
    queryRedirect(finalLinkZ2)
elif finalLinkZ=="" and finalLinkZ2=="":
    print ("\n[百度百科]\n");
    queryRedirect(finalLinkZ1)
elif finalLinkZ1=="" and finalLinkZ2=="":
    print ("\n[中文維基百科]\n");
    queryRedirect(finalLinkZ)
elif (finalLinkZ!="" and finalLinkZ1!="" and finalLinkZ2!=""):
    print ("\n[中文維基百科]\n");
    queryRedirect(finalLinkZ);
    print ("\n[百度百科]\n");
    queryRedirect(finalLinkZ1);
    print ("\n[互動百科]\n");
    queryRedirect(finalLinkZ2);
elif (finalLinkZ!="" and finalLinkZ1!="") or (finalLinkZ!="" and finalLinkZ2!="") or (finalLinkZ1!="" and finalLinkZ2!=""):
    if finalLinkZ == "":
        print ("\n[百度百科]\n");
        queryRedirect(finalLinkZ1);
        print ("\n[互動百科]\n");
        queryRedirect(finalLinkZ2);
    if finalLinkZ1 == "":
        print ("\n[中文維基百科]\n");
        queryRedirect(finalLinkZ);
        print ("\n[互動百科]\n");
        queryRedirect(finalLinkZ2);
    if finalLinkZ2 == "":
        print ("\n[中文維基百科]\n");
        queryRedirect(finalLinkZ);
        print ("\n[百度百科]\n");
        queryRedirect(finalLinkZ1);

print ("\n\n");
i = 1
while (i >= 1):
    yesno = input("要查看網站提供的infobox JSON嗎：(y/n)");
    if yesno == "y":
        linkI="http://zhishi.me/api/entity/"
        linkI_1="?property=infobox"
        infoLinkZ=linkI+urllib.parse.quote(inputString)+linkI_1
        print ("URL:"+infoLinkZ);

        if infoLinkZ!="" or infoLinkZ1!="" or infoLinkZ2!="":
            queryInfobox(infoLinkZ);

#         if infoLinkZ=="" and infoLinkZ1=="":
#             queryInfobox(infoLinkZ2)
#         elif infoLinkZ=="" and infoLinkZ2=="":
#             queryInfobox(infoLinkZ1)
#         elif infoLinkZ1=="" and infoLinkZ2=="":
#             queryInfobox(infoLinkZ)
#         elif infoLinkZ!="" and infoLinkZ1!="" or infoLinkZ!="" and infoLinkZ2!="" or infoLinkZ1!="" and infoLinkZ2!="":
#             if infoLinkZ == "":
#                 queryInfobox(infoLinkZ1);
#                 queryInfobox(infoLinkZ2);
#             if infoLinkZ1 == "":
#                 queryInfobox(infoLinkZ);
#                 queryInfobox(infoLinkZ2);
#             if infoLinkZ2 == "":
#                 queryInfobox(infoLinkZ);
#                 queryInfobox(infoLinkZ1);

    elif yesno == "n":
        i = -1;
    else:
        print("請鍵入y/n!");

print ("Query Finish!");
