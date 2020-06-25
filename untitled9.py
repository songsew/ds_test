#!/usr/bin/env python
# coding: utf-8

# ## 포스트 코로나 시대의 경제 상황을 국민연금 가입자 오픈데이터를 통해 알아보자?!!

# - 데이터셋: 공공 데이터 포털
# - 형태: 파일데이터 (csv)
# - 다운로드: https://www.data.go.kr/data/3046071/fileData.do

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


warnings.filterwarnings('ignore')
plt.rc('font', family='NanumBarunGothic') 
plt.rcParams['figure.figsize'] = (10, 7)

pd.set_option('display.float_format', lambda x: '%.2f' % x)

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df = pd.read_csv('./data/national-pension-202006.csv')


# In[3]:


df.head()


# ## Column 정리 (Clean)

# In[4]:


df.columns


# In[5]:


columns = ['자료생성년월', '사업장명', '사업자번호', '가입상태', '우편번호', '지번주소', '도로명주소', '법정주소코드', 
           '행정주소코드', '광역시코드', '시군구코드', '읍면동코드', '사업장형태', '업종코드', '업종코드명', 
           '적용일', '재등록일', '탈퇴일', '가입자수', '고지금액', '신규', '상실',
          ]


# In[6]:


len(df.columns)


# In[7]:


len(columns)


# In[8]:


df.columns = columns


# In[9]:


df.head()


# ## 핵심 데이터 column 추출

# In[10]:


df_main = df[['사업장명', '가입자수', '신규', '상실', '고지금액']]


# In[11]:


df_main.head()


# ## 데이터 통계

# In[12]:


df_main['신규'].mean()


# In[13]:


df_main['상실'].mean()


# In[14]:


df_main['가입자수'].mean()


# In[15]:


df_main['고지금액'].mean()


# ## 월급, 연봉 추정

# In[16]:


(df_main['고지금액'] / df_main['가입자수']).head()


# In[17]:


df_main['인당고지금액'] = df_main['고지금액'] / df_main['가입자수']
df['인당고지금액'] = df['고지금액'] / df['가입자수']


# In[18]:


df_main['인당고지금액'].head()


# **국민연금 정보로 어떻게 연봉정보를 계산하나요?**
# 
# 
# 국민연금 보험률은 9%입니다. 쉽게 이야기 하면 급여(신고소득월액)의 9%를 국민연금으로 내는 것입니다. 
# 
# 하지만 이를 절반으로 나누어 **4.5%는 회사가, 나머지 절반은 개인이 부담하는 구조**입니다. 회사는 급여 외에 추가로 금액을 부담합니다.
# 
# 국민연금 보험료는 **소득 상한선과 하한선이 설정되어 있어 소득 전체가 아닌 일부 소득에만 부과**됩니다.
# 
# 이를 역산하면 신고소득월액의 계산이 가능합니다. 하지만 **상한선과 하한선이 설정되어 있어 실제보다 과소계산**될 수 있습니다

# [수식]
# 
# - 임직원 평균 월급 = 인당고지금액 / 9% * 100%
# - 임직원 평균 연봉 = 임직원 평균 월급 * 12개월

# In[19]:


df_main['평균월급'] = df_main['인당고지금액'] / 9 * 100
df['평균월급'] = df['인당고지금액'] / 9 * 100


# In[20]:


df_main['평균연봉'] = df_main['평균월급'] * 12
df['평균연봉'] = df['평균월급'] * 12


# In[21]:


df_main['평균월급'].notnull().sum()


# In[22]:


plt.figure(figsize=(10, 7))
sns.distplot(df_main.loc[df_main['평균연봉'].notnull(), '평균연봉'])
plt.title('평균연봉', fontsize=18)
plt.show()


# In[23]:


plt.figure(figsize=(10, 7))
sns.distplot(df_main.loc[df_main['평균월급'].notnull(), '평균월급'])
plt.title('평균월급', fontsize=18)
plt.show()


# ## 정렬(Order)

# ### 연봉 King!

# In[24]:


df_main.sort_values(by='가입자수', ascending=False).head(20)


# ### 신규 채용 King!

# In[25]:


df_main.sort_values(by='신규', ascending=False).head(20)


# ### 상실 King!

# In[26]:


df_main.sort_values(by='상실', ascending=False).head(20)


# ## 300인 이하 기업

# In[27]:


people_limit = 300


# In[28]:


small = df_main.loc[(df_main['가입자수'].notnull()) & (df_main['가입자수'] < people_limit)]


# In[29]:


small['가입자수'].isnull().sum()


# In[30]:


plt.figure(figsize=(10, 7))
sns.distplot(small['가입자수'])
plt.title('가입자', fontsize=18)
plt.show()


# In[31]:


small.sort_values(by='상실', ascending=False)


# ## 사업장명 데이터 정제 (Cleansing)

# In[32]:


import re

# 괄호안 문자열 제거
pattern_1 = '\(.*\)'
pattern_2 = '\（.*\）'
pattern_3 = '주식회사'


# ### (주), (주식회사) 문자열 제거

# In[33]:


re.sub(pattern_1, '', '브레인크루(주)')


# In[34]:


re.sub(pattern_1, '', '브레인크루(주식회사)')


# In[35]:


re.sub(pattern_1, '', '(주)브레인크루')


# In[36]:


re.sub(pattern_2, '', '（주）타워홀딩스')


# ### 주식회사 문자열 제거

# In[37]:


re.sub(pattern_2, '', '브레인크루 주식회사')


# In[38]:


re.sub(pattern_2, '', '브레인크루주식회사')


# In[39]:


re.sub(pattern_2, '', '주식회사브레인크루주식회사')


# In[40]:


def text_preprocess(text):
    text = re.sub(pattern_1, '', text)
    text = re.sub(pattern_2, '', text)
    text = re.sub(pattern_3, '', text)
    return text


# In[41]:


df_main['사업장명'] = df_main['사업장명'].apply(text_preprocess)


# In[42]:


df_main[df_main['사업장명'] == '패스트캠퍼스']


# In[43]:


df['사업장명'] = df['사업장명'].apply(text_preprocess)


# In[44]:


df.columns


# In[45]:


plt.figure(figsize=(16, 6))
sns.barplot(x=df.groupby('시군구코드')['가입자수'].mean().index, y=df.groupby('시군구코드')['가입자수'].mean())
plt.title('시군구 별 가입자수')
plt.xticks(rotation=90)
plt.show()


# In[46]:


plt.figure(figsize=(16, 6))
sns.barplot(x=df.groupby('시군구코드')['신규'].mean().index, y=df.groupby('시군구코드')['신규'].mean())
plt.title('시군구 별 신규인력')
plt.xticks(rotation=90)
plt.show()


# In[47]:


plt.figure(figsize=(16, 6))
sns.barplot(x=df.groupby('시군구코드')['상실'].mean().index, y=df.groupby('시군구코드')['상실'].mean())
plt.title('시군구 별 신규인력')
plt.xticks(rotation=90)
plt.show()


# In[48]:


df.head()


# ## 신규 인력이 많은 시군구코드

# **경기도 평택시**에서 최근 국민연금 가입자 신규인력이 가장 많이 발생했음
# 
# 주로 건축 인력 혹은 건설사 인력들이 신규로 편입되면서 국민연금 가입자 발생이 가장 많이 일어난 것으로 집계 됐다.

# In[49]:


df.loc[df['시군구코드'] == 220][['사업장명','지번주소','신규']].sort_values(by='신규', ascending=False).head(20)


# **서울특별시 영등포구**에서 가장 많은 상실 인력이 발생했다.
# 
# 하지만, 효성ITX, 엘지전자와 같이 굵직한 기업들이 인력 감소를 함으로써 **본 주소인 영등포구 에서 상실 인력**이 많이 발생한 것으로 집계됐다.

# In[50]:


df.loc[df['시군구코드'] == 560][['사업장명','지번주소','상실']].sort_values(by='상실', ascending=False).head(20)


# ## 업종별 신규 인력 현황

# In[51]:


df.groupby('업종코드명')['신규'].mean()


# In[52]:


df_1 = df.groupby('업종코드명')['신규'].mean()


# In[53]:


df_1.sort_values(ascending=False).count()


# 총 출력할 갯수(업종=1121개)가 너무 많다...ㅠ

# 상위 50 개 **업종** 출력하도록 하겠습니다.

# In[54]:


df_top100 = df_1.sort_values(ascending=False).head(50)


# In[55]:


plt.figure(figsize=(16, 6))
sns.barplot(x=df_top100.index, y=df_top100)
plt.title('업종별 신규인력')
plt.xticks(rotation=90)
plt.show()


# - 코로나 바이러스 이전 사태와는 면밀한 비교를 위하여 이전 데이터가 필요합니다.
# - 하지만, 포스트 코로나 현상황에서는 **음료품배달업, 포장 검수 및 계량 서비스업, 수산동물 훈제 조리 및 유사 조제식품 제조업** 순으로 채용이 증가되었음을 확인할 수 있습니다.

# In[56]:


df_2 = df.groupby('업종코드명')['상실'].mean()


# In[57]:


df_bot100 = df_2.sort_values(ascending=False).head(50)


# In[58]:


plt.figure(figsize=(16, 6))
sns.barplot(x=df_bot100.index, y=df_bot100)
plt.title('업종별 상실인력')
plt.xticks(rotation=90)
plt.show()


# 업종별 상실 인력에 대한 **TOP 50 결과**입니다.

# 여기서 재밌는 점은, 이전에 신규인력이 가장 많은 업종도 **음료품배달원** 이었다는 점입니다. 
# 
# 좀 더 구체적인 데이터를 통해서 신규와 상실이 동시에 많이 일어난 이유에 대한 분석이 면밀히 필요합니다.
# 
# 때론, 한 기업이 M&A를 진행된 후 타 회사로 인력이 **상실 -> 편입 되면서 데이터 인사이트에 대한 왜곡 현상**이 생길 수 있습니다.

# ## 업종별 단일 회사 연봉 비교 차트 그리기

# In[98]:


def compare_and_visualize(company):
    code = df[df['사업장명'] == company]['업종코드']
    cols = ['가입자수', '평균월급', '평균연봉', '신규', '상실', '업종코드']
    filtered = df.loc[df['업종코드']==code.item()][cols]
    df_company = df.loc[df['사업장명'] == company][cols]
    df_company = df_company.append(pd.Series(filtered.mean()), ignore_index=True)
    
    compare_cols = ['가입자수', '평균월급', '평균연봉', '신규', '상실']
    for col in compare_cols:
        plt.figure(figsize=(10, 5))
        sns.barplot(x=[company, '업종평균'], y=col, data=df_company)
        plt.title('{} vs 업종평균'.format(col), fontsize=18)
        plt.show()


# In[101]:


compare_and_visualize('패스트캠퍼스')


# In[ ]:





