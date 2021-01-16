def get_corpcode_file(file_name):

    import zipfile

    api_key="7946dcde119af7656afc01157071c0ab9488b9ad" #api key
    url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key="+api_key
    download(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zipObj:
        file_list = zipObj.namelist()
        target = file_list[0]
        print(target)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(".")
    return target


def download(url, file_name):
    from requests import get
    with open(file_name, "wb") as file:   # open in binary mode
        response = get(url)               # get request
        file.write(response.content)      # write to file



def find_corp_code(firmname):
    import xml.etree.ElementTree as ET
    xml = ET.parse(get_corpcode_file("corp_code.zip"))
    root = xml.getroot()

    lists = root.findall('list')

    for list in lists:
        if (list.find('corp_name').text == firmname):
            return (list.find('corp_code').text)

def find_rcept_no(firmname, year):

    from requests import get

    corp_code = find_corp_code(firmname)
    crtfc_key = "7946dcde119af7656afc01157071c0ab9488b9ad"

    bgn_de = year+"0531"
    end_de = year+"0601"
    pblntf_ty = "J"

    url = "https://opendart.fss.or.kr/api/list.json?corp_code=" + corp_code + "&crtfc_key=" + crtfc_key + "&bgn_de=" + bgn_de + "&end_de=" + end_de + "&pblntf_ty=" + pblntf_ty

    response = get(url)
    json = response.json()
    rcept_no = json["list"][0]["rcept_no"]

    return rcept_no

def get_shares_url(firmname, year):

    from selenium import webdriver

    rcept_no = find_rcept_no(firmname, year)

    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3)
    url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + rcept_no

    driver.get(url)

    driver.find_element_by_css_selector('#ext-gen10 > div > li:nth-child(4) > ul > li:nth-child(1) > div > a > span').click()

    shares_url = driver.find_element_by_id('ifrm').get_attribute('src')

    return shares_url

def parse_table(firmname, year):

    import numpy as np
    import pandas as pd

    # parse raw html table with designated headers
    url = get_shares_url(firmname, year)
    header = ['소속회사명1', '소속회사명2', '동일인과의 관계1', '동일인과의 관계2', '동일인과의 관계3', '성명',
              '보통주 주식수', '보통주 지분율', '우선주 주식수', '우선주 지분율', '합계 주식수', '합계 지분율']
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = header

    # convert dtype of '합계 주식수' column from str to int
    df['합계 주식수'] = df['합계 주식수'].replace(["-"], '0')
    df['합계 주식수'] = df['합계 주식수'].astype(int)

    # get shares ratio
    sum = df[df['동일인과의 관계1'] == '총계']
    sum2 = pd.DataFrame({'소속회사명2': sum['소속회사명2'], 'divisor': sum['합계 주식수']})
    df = pd.merge(df, sum2)
    df['shares'] = df['합계 주식수'] / df['divisor']

    # categorize '동일인과의 관계3' variable

    df['type'] = df['동일인과의 관계3']
    df['type2'] = df['동일인과의 관계3']

    df['type'] = df['type'].apply(rel3_categorize)
    df['type2'] = df['type2'].apply(rel3_categorize2)

    # calc values 'own', 'own2', and 'ownername' variable

    own = df.groupby(['소속회사명2', 'type'])['shares'].sum().rename('own').reset_index()
    df = pd.merge(df, own, how='left')

    own2 = df.groupby(['소속회사명2', 'type2'])['shares'].sum().rename('own2').reset_index()
    df = pd.merge(df, own2, how='left')

    for i in df.index:
        val = df.loc[i, 'type']
        if (val == '1'):
            df.at[i, 'own'] = df.loc[i, 'shares']
        elif (val == '-1'):
            df.at[i, 'own'] = df.loc[i, 'shares']
        elif (val == '50'):
            df.at[i, 'own'] = np.nan

    for i in df.index:
        val = df.loc[i, 'type2']
        if (val == '1'):
            df.at[i, 'own2'] = df.loc[i, 'shares']
        elif (val == '-1'):
            df.at[i, 'own2'] = df.loc[i, 'shares']
        elif (val == '50'):
            df.at[i, 'own2'] = np.nan

    df['ownername'] = ''

    for i in df.index:
        val = df.loc[i, 'type2']
        if (val == '1'):
            df.at[i, 'ownername'] = df.loc[i, '성명']

    # erase '㈜' or '(주)'
    df = df.replace(['^(주)', '^㈜', '(주)$', '㈜$', '^(주) ', '^㈜ ', ' (주)$', ' ㈜$'],
                               ['', '', '', '', '', '', '', ''], regex=True)

    # discard unwanted rows

    discard = []
    for i in df.index:
        val = df.loc[i, 'type2']
        if (val == '0'):
            if (df.loc[i, '동일인과의 관계2'] != '동일인'):
                discard.append(i)
        elif (val == '50'):
            discard.append(i)
        elif (val == '99'):
            if (df.loc[i - 1, 'type2'] == '99'):
                discard.append(i)

    df.drop(discard, axis=0, inplace=True)

    # discard unwated columns and change the column names
    df = df[['소속회사명2', 'own', 'own2', 'type2', 'ownername']]
    df.columns = ['firmname', 'own', 'own2', 'type', 'ownername']

    return df

def rel3_categorize(rel3):
    if ((rel3 == '동일인') | (rel3 == '친족 합계')):
        return '0'
    elif (rel3 == '계열회사(국내+해외)'):
        return '1'
    elif ((rel3 == '기타') | (rel3 == '동일인측이 아닌 최다주주')):
        return '99'
    elif (rel3 == '기타 동일인관련자'):
        return '-1'
    else:
        return '50'

def rel3_categorize2(rel3):
    if ((rel3 == '동일인') | (rel3 == '친족 합계') | (rel3 == '비영리법인') | (rel3 == '등기된 임원') | (rel3 == '자기주식')):
        return '0'
    elif (rel3 == '계열회사(국내+해외)'):
        return '1'
    elif ((rel3 == '기타') | (rel3 == '동일인측이 아닌 최다주주')):
        return '99'
    elif (rel3 == '기타 동일인관련자'):
        return '-1'
    else:
        return '50'

def get_chaebol_data(firmname: str, year: str):
    df = parse_table(firmname, year)
    check_data = df.groupby(['firmname']).sum('own2')
    check_file_name = firmname+year+'check.csv'
    check_data.to_csv(check_file_name)
    print(check_data)
    out = firmname+year+'.csv'
    df.to_csv(out)