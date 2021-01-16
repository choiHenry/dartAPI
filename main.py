# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

import get_chaebol_data
# get_chaebol_data.get_chaebol_data("삼성전자", "2020")
# get_chaebol_data.get_chaebol_data("삼성전자", "2019")

group_dict = {'기업집단': ['삼성', '현대자동차', '에스케이', '엘지', '롯데', '포스코', '한화', '지에스', '현대중공업', '농협', '신세계',
                       '케이티', '씨제이', '한진', '두산', '엘에스', '부영', '대림', '미래에셋', '금호아시아나', '에쓰-오일', '현대백화점',
                       '카카오', '한국투자금융', '교보생명보험', '효성', '하림', '영풍', '대우조선해양', '케이티앤지', '에이치디씨', '케이씨씨',
                       '코오롱', '대우건설'],
              '대표회사': ['삼성전자', '현대자동차', 'SK', 'LG', '롯데지주', '포스코', '한화', 'GS', '현대중공업', '농협경제지주', '신세계',
                       '케이티', 'CJ', '대한항공', '두산', 'LS', '부영', '대림산업','미래에셋캐피탈', '금호산업', 'S-Oil', '현대백화점',
                       '카카오', '한국금융지주', '교보생명보험', '효성', '하림지주', '영풍', '대우조선해양', '케이티앤지', 'HDC', '케이씨씨',
                       '코오롱', '대우건설']}

import pandas as pd
match = pd.DataFrame(group_dict)
print(match.head(34))