import pandas as pd
import numpy as np
from konlpy.tag import Kkma
import re

rawdata_path = './rawdata.csv'
kkma = Kkma()
df = pd.read_csv(rawdata_path)
#영상제목 토큰화 하는 과정
noun_final = []
del_line = []
for text in range(len(df)):
    print(df['title'].iloc[text])
    try:
        noun0=kkma.pos(df['title'].iloc[text])
    except:
        del_line.append(text)
        continue
    noun=[]
    for i,j in noun0:
        if j=='NNG':
            if i == '딩고':
                pass
            else:
                noun.append(i)
    noun_final.append(noun)
df=df.drop(del_line)
df.reset_index(drop=True)
df.view = df.view.str.extract('(\d+)').astype(float)# 조회수 정리
likes_thousand=df['like'].str.contains('\d+천')
likes_tenthousand = df['like'].str.contains('\d+만')
df['like'] = df['like'].str.extract('(\d+)', expand=False).astype(float)
df.loc[likes_thousand, 'like'] *= 1000
df.loc[likes_tenthousand, 'like'] *= 10000

likes_thousand=df['unlike'].str.contains('\d+천')
likes_tenthousand = df['unlike'].str.contains('\d+만')
df['unlike'] = df['unlike'].str.extract('(\d+)', expand=False).astype(float)
df.loc[likes_thousand, 'unlike'] *= 1000
df.loc[likes_tenthousand, 'unlike'] *= 10000

df['token'] = noun_final

#토큰화 작업을 거친 뒤에 단어가 하나인 것은 제외하기
noun_ls = []
for i in range(len(df)):
    noun_ls0=[]
    for j in range(len(df['token'].iloc[i])):
        if len(df['token'].iloc[i][j]) == 1:
            pass
        else:
            noun_ls0.append(df['token'].iloc[i][j])
    noun_ls.append(list(set(noun_ls0))) #중복제거
df['token'] = noun_ls
df.to_csv('./preprocessed.csv',encoding='utf-8-sig')

token_df = pd.DataFrame({'token':[]})
for i in range(len(df)):
    insert_data = pd.DataFrame({'token': df['token'].iloc[i]})
    insert_data['view'] = df['view'].iloc[i]

    token_df = token_df.append(insert_data)

token_df2 = token_df.groupby('token')['view'].sum().reset_index()  # 키워드별 조회수 합
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['view'].tolist()  # 각 키워드의 갯수
# 키워드별 조회수의합 / 갯수 - 동등하게 만들어야 하기 때문에
view_count = []
for i in range(len(token_df2)):
    a = token_df2['view'].iloc[i] / token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['view_count'] = view_count
# del_keyword = ['열애','미드라','바보','다이','질주','은하','어깨','거지','정류장','그레이','준일','종신','방탄','형식','민서','악동','뮤지션','소어','주행','바램','노력','포박','자격지심','시티','푸스','게다리','라마','분노','행복']
del_keyword = ['청하','경리','니트','남우','용사','할아버지','이병기','너와','현우','고수','자존','동갑내기','벚꽃','생존','장애','자수성가','호텔','사장님','역전','민박','나이','스토리','세정','재인','스쿨','유정','세정','구구단','호시','아이오','벨벳','레드','선미','고생','오의','어부','식당','하자',]
for keyword in del_keyword:
    token_df2=token_df2.drop(token_df2[token_df2['token']==keyword].index)
print(token_df2.sort_values(by='view_count',ascending=False).head(30))

token_df2.to_csv('./count.csv',encoding='utf-8-sig')

