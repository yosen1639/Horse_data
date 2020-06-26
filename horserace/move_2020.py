import requests
import bs4
import pandas as pd
import data_collect

#'馬名', '性別', '馬齢'の取得、基本データフレームの作成
def first(url):
    df = pd.read_html(url)[0]
    result = pd.DataFrame(columns=['馬名', '性別', '馬齢'])
    result['馬名'] = df['馬名']
    result['性別'] = df['性齢'].str[0]
    result['馬齢'] = df['性齢'].str[1]
    return result

def get_url_2020(url):
    global horse_url
    horse_url = []
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    # 転移先のurlを取得したい、該当箇所を抜きだし
    elem = soup.select('.Shutuba_Table a')
    for i in elem:
        t = i.get('href')
        if t[24:29] == 'horse':
            horse_url.append(t)
    return horse_url

def race_result(goal):
    year = 2019
    for i in range(period):
        df = pd.read_html(goal[i])[0]
        result = pd.DataFrame(columns=['馬名', '性別', '馬齢'])
        result['馬名'] = df['馬名']
        result['性別'] = df['性齢'].str[0]
        result['馬齢'] = df['性齢'].str[1]

        get_url2(goal[i])
        h_summury = pd.DataFrame(columns=['タイム','着順','馬場','人気','騎手','馬番','馬体重',
                                          '馬体重増減','脚質','前走レース名','前走着順','前走5走着順',
                                          '前走5走上り','コース適正','血統'])
        for j in range(len(horse_url)):
            h = data_collect.main(horse_url[j],year,racename)
            if len(h) == 1:
                h_new = h.rename(index={h.index[0]:j})
                h_summury = pd.concat([h_summury,h_new])
            print(h_summury)

        result = pd.merge(result, h_summury, left_index=True, right_index=True)
        if i == 0:
            final = result
        else:
            final = pd.concat([final,result],ignore_index=True)
        year -= 1


def main():
    url_first = 'https://race.netkeiba.com/race/shutuba.html?race_id=202006020511'
    result = first(url_first)
    goal_2020 = get_url_2020(url_first)


main()