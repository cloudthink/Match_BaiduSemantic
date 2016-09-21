__author__ = 'zhangyuanchen'
#-*- coding: UTF-8 -*-
#原始核心文档
import jieba
import re
import jieba.posseg as pseg
from math import sqrt

road_2='C:/Users/think/Desktop/baiduthink/'
input_data_1=open(road_2+"baiduread/DATA/opendata.txt",'r',encoding='utf-8',errors='ignore')
out_data_1=open(road_2+"baiduread/DATA/opendata_clean.txt",'w',encoding='utf-8',errors='ignore')
for one_line in input_data_1.readlines():
    try:
        print(one_line)
        for one in one_line:
            if one!=' ':
                out_data_1.write(one)
    except:
        for one in one_line:
            try:
                print(one)
                if one!=' ':
                    out_data_1.write(one)
            except:
                out_data_1.write('')


input_data_2=open(road_2+"baiduread/DATA/opendata_20w.txt",'r',encoding='utf-8',errors='ignore')
out_data_2=open(road_2+"baiduread/DATA/opendata_20w_clean.txt",'w',encoding='utf-8',errors='ignore')
for one_line in input_data_2.readlines():
    try:
        print(one_line)
        for one in one_line:
            if one!=' ':
                out_data_2.write(one)
    except:
        for one in one_line:
            try:
                print(one)
                if one!=' ':
                    out_data_2.write(one)
            except:
                out_data_2.write('')


input_data=open(road_2+"baiduread/DATA/opendata_20w_clean.txt",'r',encoding='utf-8',errors='ignore')
learn_data=open(road_2+"baiduread/DATA/opendata_clean.txt",'r',encoding='utf-8',errors='ignore')
out_data=open(road_2+"baiduread/out/outdata_20w_main_tijiao_8_29.txt",'w',encoding='utf-8',errors='ignore')

#加载自定义词典
jieba.load_userdict(road_2+"baiduread/DATA/weizhi1.txt")
jieba.load_userdict(road_2+"baiduread/DATA/jiaba2.txt")
jieba.load_userdict(road_2+"baiduread/DATA/n3605.txt")


print('开始')
line_number=0
grade=0
tingyongci=['。','，',' ','（',')','(','年','1','2','3','4','5','6','7','8','9','0','的','了','!','、',' ']
def xiangsidu(key,core_entity):
    file_words = {}
    ignore_list = [u'的',u'了',u'和',u'呢',u'啊',u'哦',u'恩',u'嗯',u'吧',u' ',u''];
    try:
        seg_list=[]
        all_the_text = key
        for one in all_the_text:
            seg_list.append(one)
        #print(seg_list)
        for s in seg_list:
            if  s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [1,0]
                else:
                    file_words[s][0] += 1
    finally:
        pass
    try:
        seg_list=[]
        all_the_text = core_entity
        for one in all_the_text:
            seg_list.append(one)
        #print(seg_list)
        for s in seg_list:
            if  s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [0,1]
                else:
                    file_words[s][1] += 1
    finally:
        pass
    sum_2 = 0.001
    sum_file1 = 0.001
    sum_file2 = 0.001
    for word in file_words.values():
        sum_2 += word[0]*word[1]
        sum_file1 += word[0]**2
        sum_file2 += word[1]**2

    rate = sum_2/(sqrt(sum_file1*sum_file2))
    #print ('rate',rate)
    #返回两个词语的余弦相似度
    return rate
feature_list_right={}
feature_list_left={}
feature_list_all={}
def learn(content_list,core_entity):
    if core_entity not in content_list:
        max_xiangsidu=0
        for one in content_list:
            if xiangsidu(one,core_entity)>max_xiangsidu:
                max_xiangsidu=xiangsidu(one,core_entity)
                new_core_entity=one
        key_nu=content_list.index(new_core_entity)
    else:
        key_nu=content_list.index(core_entity)

    if feature_list_right.get(content_list[key_nu+1])==None:
        feature_list_right[content_list[key_nu+1]]=0
    else:
        #print(feature_list_right,feature_list_right.get(content_list[key_nu+1]))
        feature_list_right[content_list[key_nu+1]]=feature_list_right[content_list[key_nu+1]]+1

    if key_nu!=0:
        if feature_list_left.get(content_list[key_nu-1])==None:
            feature_list_left[content_list[key_nu-1]]=0
        else:
            feature_list_left[content_list[key_nu-1]]=feature_list_left[content_list[key_nu-1]]+1
    for one in content_list:
        if feature_list_all.get(one)==None:
            feature_list_all[one]=1
        else:
            feature_list_all[one]=feature_list_all[one]+1
#核心算法
#global max_nu_left
#global max_nu_right

def find_key(content_list):
    max_nu_left=max_nu_right=0
    max_nu_left_index=max_nu_right_index=0
    for one in content_list:
        if (one in feature_list_right) and feature_list_right.get(one)>=max_nu_right and (one not in tingyongci) and (feature_list_right.get(one)>1):
            max_nu_right=feature_list_right.get(one)
            max_nu_right_index=content_list.index(one)
            #print('right',one,max_nu_right)
        else:
            #print('rightt',one,feature_list_right.get(one))
            pass
    for one in content_list:
        if (one in feature_list_left) and (feature_list_left.get(one)>=max_nu_left) and (one not in tingyongci) and (feature_list_left.get(one)>1):
            max_nu_left=feature_list_left.get(one)
            max_nu_left_index=content_list.index(one)
            #print('left',one,max_nu_left)
        else:
            #print('leftt',one,feature_list_left.get(one))
            pass
    if max_nu_right>max_nu_left:
        key=content_list[max_nu_right_index-1]
    else:
        key=content_list[max_nu_left_index+1]

    p_line=[]
    for i in range(0,(len(content_list)+2)):
        p_line.append(0)
    #print(p_line,len(content_list),len(p_line))
    for one in content_list:
        if (feature_list_right.get(one)!=None) and (feature_list_left.get(one)!=None) and (feature_list_all.get(one)!=None) and ((one not in tingyongci)):
            #print(one,feature_list_left.get(one),feature_list_all.get(one),feature_list_right.get(one))
            if content_list.index(one)==0:
                p_line[0]=(feature_list_left.get(one)/float(feature_list_all.get(one)))
            else:
                p_line[content_list.index(one)]=p_line[content_list.index(one)-1]+float(feature_list_right.get(one)/float(feature_list_all.get(one)))
                p_line[content_list.index(one)+2]=p_line[content_list.index(one)-1]+float(feature_list_left.get(one)/float(feature_list_all.get(one)))
    #words =pseg.cut(content_list)
    #print(words)
    #print(p_line)
    #for j in content_list:
    #    print(j,p_line[content_list.index(j)+1])
    key=content_list[(p_line.index(max(p_line)))-1]
    #print(max_nu_right,max_nu_left,content_list[max_nu_right_index],content_list[max_nu_left_index],max(p_line),content_list[(p_line.index(max(p_line)))-1],key)
    if key in tingyongci:
        for one in content_list:
            p_line[content_list.index(one)+1]=0
        key=content_list[(p_line.index(max(p_line)))-1]
    return key
global nn
nn=0
def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        #uchar=uchar.encode('utf-8')
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def main_key_find(content, core_entity):
    #这里暂时不用搜索引擎模式
    seg_list = jieba.cut(content)  #
    words = pseg.cut(content)
    words_line={}
    words_line_line=[]
    for w in words:
        words_line[w.word]=w.flag
        words_line_line.append((w.word,w.flag))
    content_list=[]
    for one in seg_list:
        content_list.append(one)
    print(content_list)

    key = find_key(content_list)
    key_one_nu=0.0000000001
    key_notn_nu=0.0000000001
    key_add=0
    nline=['n','nr','ns','nt','nz','nl','ng','nw','nrt','nrfg']
    for one in pseg.cut(key):
        key_one_nu=key_one_nu+1
        if one.flag not in nline:
            key_notn_nu=key_notn_nu+1
            print(one.word,one.flag)
    if float(key_notn_nu/key_one_nu)>0.5:
        key=''
        for one in words_line_line:
            if (one[1] in nline) and (key_add<=1):
                key=key+one[0]
                key_add=key_add+1
                print('new',key)

    if ("《" in content) and ("》" in content):
        start=content.index("《")
        end=content.index("》")
        key=content[start+1:end]
        print(key)
    if key==("" or '\n' or ' '):
        key=content[0:3]
    content=content[:-1]
    print('[{"content":"'+ content+'","core_entity": ["'+key+'"]}]')
    out_data.write('[{"content":"'+ content+'","core_entity": ["'+key+'"]}]'+'\n')
    the_grade = 0
    the_grade=xiangsidu(key,core_entity)
    print(the_grade)
    return (content, key, core_entity, the_grade)
for one_line in learn_data.readlines():
    #print(one_line)
    try:
        (a, b) = re.search(r'"content": "', one_line, re.M | re.I).span()
        (c, d) = re.search(r'"core_entity"', one_line, re.M | re.I).span()
        content = one_line[b:c-3]
        core_entity = re.sub("\",\"","",one_line[d+4:-5])
        #print(content,core_entity)
        seg_list = jieba.cut(content)  #
        words = pseg.cut(content)
        content_list=[]
        for one in seg_list:
            content_list.append(one)
        learn(content_list,core_entity)
    except:
        print('data error:',one_line)
line_number=0
grade=0
for one_line in input_data.readlines():
    #print(one_line)
    line_number=line_number+1
    #(a, b) = re.search(r'"content": "', one_line, re.M | re.I).span()
    #(c, d) = re.search(r'"core_entity"', one_line, re.M | re.I).span()
    #content = one_line[b:c-3]
    #core_entity = re.sub("\",\"","",one_line[d+4:-5])
    #print(content,core_entity)
    content=one_line
    core_entity=one_line[0:3]
    (content,mykey,core_entity,one_grade)=main_key_find(content, core_entity)
    grade=grade+one_grade
    #print(grade)
#分词系统评分
print('Grade',grade/line_number)
#feature_list_right=sorted(feature_list_right,key=lambda d:(d[0],d[1]))
#feature_list_left=sorted(feature_list_left,key=lambda d:(d[0],d[1]))

for one in sorted( feature_list_left.keys() ):
    if feature_list_left[one]>50:
        print(one,feature_list_left[one])
for one in sorted( feature_list_right ):
    if feature_list_right[one]>50:
        print(one,feature_list_right[one])



