# Large Business Group

This repository contains large businesss group data package.

## How package is composed

1. scripts(main.py, dapi.py)

2. data(group list, raw data, cleansed data, confirm data, etc.)

## How to use

### data

Precisely, each [designated large business group(LBG)](https://www.egroup.go.kr/egps/wi/stat/kap/appnSttusList.do) submits the yearly report, whose name is '대규모기업집단현황공시[연1회공시및1/4분기용(대표회사)]' to KFTC. For example, Samsung Electronics who represents entire Samsung business group submitted a [대규모기업집단현황공시[연1회공시및1/4분기용(대표회사)]](http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200601000086) on 05/31/20.

Program scrapes Equity Ownership Status('소유지분현황') sections of these reports for 2019-2020 using [open dart api](https://www.egroup.go.kr/egps/wi/stat/kap/appnSttusList.do) and process data in accordance with the research purpose of [Research Center for Market and Government](rcmg.snu.ac.kr).

The lists of designated LBG and the representing firm are in 'group_list' directory.

The raw data sets for each firm parsed directly from web page are stored in 'raw' directory.

The final datasets are in 'out' directory.

The confirm datasets are in confirm directory.

### program

After cloning this repository in a local directory on your machine, install python(version >= 3.6).

[Set up virtual environments and install packages](https://docs.python.org/3/tutorial/venv.html) for running program in 'requirements.txt'.

Now you need to [request your open dart api key](https://opendart.fss.or.kr/uss/umt/EgovMberInsertView.do).

Then go to the local local repo, open up terminal, and type

```terminal
$ python3 main.py <your-open-dart-api-key>
```

Then program starts to download and process data for 2019 and 2020.

### If you want to get data for 2021

You need to insert LBG list to Dapi object in the dictionary form, e.g.,

```python
group20 = {'기업집단': ['삼성', '현대자동차', '에스케이', '엘지', '롯데', '포스코', '한화', '지에스', '현대중공업', '농협', '신세계',
                     '케이티', '씨제이', '한진', '두산', '엘에스', '부영', '대림', '미래에셋', '금호아시아나', '에쓰-오일', '현대백화점',
                     '카카오', '한국투자금융', '교보생명보험', '효성', '하림', '영풍', '대우조선해양', '케이티앤지', '에이치디씨', '케이씨씨',
                     '코오롱', '대우건설', '오씨아이', '이랜드', '태영', 'SM', 'DB', '세아', '네이버', '넥슨', '한국타이어', '호반건설',
                     '셀트리온', '중흥건설', '넷마블', '아모레퍼시픽', '태광', '동원', '한라', '삼천리', '에이치엠엠', '장금상선', 'IMM인베스트먼트',
                     '한국지엠', '동국제강', '다우키움', '금호석유화학', '애경', '하이트진로', '유진', 'KG', '삼양'],
           '대표회사': ['삼성전자', '현대자동차', 'SK', 'LG', '롯데지주', '포스코', '한화', 'GS', '한국조선해양', '농협경제지주', '신세계',
                     '케이티', 'CJ', '대한항공', '두산', 'LS', '부영', '대림산업', '미래에셋캐피탈', '금호산업', 'S-Oil', '현대백화점',
                     '카카오', '한국금융지주', '교보생명보험', '효성', '하림지주', '영풍', '대우조선해양', '케이티앤지', 'HDC', '케이씨씨',
                     '코오롱', '대우건설', 'OCI', '이랜드월드', '태영건설', '티케이케미칼', 'DB', '세아홀딩스', 'NAVER', '엔엑스씨',
                     '한국앤컴퍼니', '호반건설', '셀트리온홀딩스', '중흥건설', '넷마블', '아모레퍼시픽그룹', '태광산업', '동원엔터프라이즈', 
                     '한라홀딩스', '삼천리', 'HMM', '장금상선', '아이엠엠인베스트먼트', '한국지엠', '동국제강', '키움증권', '금호석유화학', 
                     'AK홀딩스', '하이트진로홀딩스', '유진기업', 'KG케미칼', '삼양홀딩스']}
```

To do this, first run

```python
from dart_api import DartApi
import sys
myAPIKey = <your-open-dart-api-key>
api = Dapi()
group20 = {'기업집단': ['삼성', '현대자동차', '에스케이', '엘지', '롯데', '포스코', '한화', '지에스', '현대중공업', '농협', '신세계',
                     '케이티', '씨제이', '한진', '두산', '엘에스', '부영', '대림', '미래에셋', '금호아시아나', '에쓰-오일', '현대백화점',
                     '카카오', '한국투자금융', '교보생명보험', '효성', '하림', '영풍', '대우조선해양', '케이티앤지', '에이치디씨', '케이씨씨',
                     '코오롱', '대우건설', '오씨아이', '이랜드', '태영', 'SM', 'DB', '세아', '네이버', '넥슨', '한국타이어', '호반건설',
                     '셀트리온', '중흥건설', '넷마블', '아모레퍼시픽', '태광', '동원', '한라', '삼천리', '에이치엠엠', '장금상선', 'IMM인베스트먼트',
                     '한국지엠', '동국제강', '다우키움', '금호석유화학', '애경', '하이트진로', '유진', 'KG', '삼양'],
           '대표회사': ['삼성전자', '현대자동차', 'SK', 'LG', '롯데지주', '포스코', '한화', 'GS', '한국조선해양', '농협경제지주', '신세계',
                     '케이티', 'CJ', '대한항공', '두산', 'LS', '부영', '대림산업', '미래에셋캐피탈', '금호산업', 'S-Oil', '현대백화점',
                     '카카오', '한국금융지주', '교보생명보험', '효성', '하림지주', '영풍', '대우조선해양', '케이티앤지', 'HDC', '케이씨씨',
                     '코오롱', '대우건설', 'OCI', '이랜드월드', '태영건설', '티케이케미칼', 'DB', '세아홀딩스', 'NAVER', '엔엑스씨',
                     '한국앤컴퍼니', '호반건설', '셀트리온홀딩스', '중흥건설', '넷마블', '아모레퍼시픽그룹', '태광산업', '동원엔터프라이즈', 
                     '한라홀딩스', '삼천리', 'HMM', '장금상선', '아이엠엠인베스트먼트', '한국지엠', '동국제강', '키움증권', '금호석유화학', 
                     'AK홀딩스', '하이트진로홀딩스', '유진기업', 'KG케미칼', '삼양홀딩스']}

group19 = {'기업집단': ['삼성', '현대자동차', '에스케이', '엘지', '롯데', '포스코', '한화', '지에스', '현대중공업', '농협', '신세계',
                     '케이티', '씨제이', '한진', '두산', '엘에스', '부영', '대림', '미래에셋', '금호아시아나', '에쓰-오일', '현대백화점',
                     '카카오', '한국투자금융', '교보생명보험', '효성', '하림', '영풍', '대우조선해양', '케이티앤지', '에이치디씨', '케이씨씨',
                     '코오롱', '대우건설', '오씨아이', '이랜드', '태영', 'SM', 'DB', '세아', '네이버', '넥슨', '한국타이어', '호반건설',
                     '셀트리온', '중흥건설', '넷마블', '아모레퍼시픽', '태광', '동원', '한라', '삼천리', '한국지엠', '동국제강', '다우키움', 
                     '금호석유화학', '애경', '하이트진로', '유진'],
           '대표회사': ['삼성전자', '현대자동차', 'SK', 'LG', '롯데지주', '포스코', '한화', 'GS', '한국조선해양', '농협경제지주', '신세계',
                     '케이티', 'CJ', '대한항공', '두산', 'LS', '부영', '대림산업', '미래에셋캐피탈', '금호산업', 'S-Oil', '현대백화점',
                     '카카오', '한국금융지주', '교보생명보험', '효성', '하림지주', '영풍', '대우조선해양', '케이티앤지', 'HDC', '케이씨씨',
                     '코오롱', '대우건설', 'OCI', '이랜드월드', '태영건설', '티케이케미칼', 'DB', '세아홀딩스', 'NAVER', '엔엑스씨',
                     '한국앤컴퍼니', '호반건설', '셀트리온홀딩스', '중흥건설', '넷마블', '아모레퍼시픽그룹', '태광산업', '동원엔터프라이즈', 
                     '한라홀딩스', '삼천리', '한국지엠', '동국제강', '키움증권', '금호석유화학', 'AK홀딩스', '하이트진로홀딩스', '유진기업']}

groupList = [group19, group20]
group21 = <group-dictionary-for-2010>
groupList.append(group21)
api.groupList = groupList
myAPIKey = "7946dcde119af7656afc01157071c0ab9488b9ad"  # api key
api.apiKey = myAPIKey
api.saveGroupListData()
api.getCBDataAll()

```

## Error handling

1. If "Chromedriver permission denied" message appears in terminal, go to [chromedriver download page](https://chromedriver.chromium.org/downloads) and download latest versions in accordance with your local os.

2. If 'Error: “chromedriver” cannot be opened because the developer cannot be verified' message shows up in the terminal, then refer this [stack overflow answer](https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de). To sum up, open up the terminal in the local directory where chromedriver is, and type

```terminal
$ xattr -d com.apple.quarantine chromedriver
```

## To be updated

It is not hard to find patterns in report typos.

1. '친족 합계' row value in '합계 주식수' column contains '합계 주식수' data of '동일인'
2. '기타' rows of a firm contains '합계' row

These common errors could be handled in a general algorithm.
