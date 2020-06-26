import requests
import bs4
import pandas as pd
import data_collect_2020

#'馬名', '性別', '馬齢'の取得、基本データフレームの作成
def first(url):
    df = pd.read_html(url)[0]
    result = pd.DataFrame(columns=['馬名', '馬番', '性別', '馬齢', '騎手', '人気'])
    result['馬名'] = df['馬名']['馬名']
    result['馬番'] = df['馬番']['馬番']
    result['性別'] = df['性齢']['性齢'].str[0]
    result['馬齢'] = df['性齢']['性齢'].str[1].astype(int)
    result['騎手'] = df['騎手']['騎手']
    result['人気'] = df['人気']['人気']
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

def race_result(goal, result):
    h_summury = pd.DataFrame(columns=['脚質','前走レース名','前走着順','前走5走着順',
                                          '前走5走上り','コース適正','血統'])
    for i in range(len(goal)):
        h = data_collect_2020.main(goal[i], '阪神')
        if len(h) == 1:
            h_new = h.rename(index={h.index[0]:i})
            h_summury = pd.concat([h_summury, h_new])

    result = pd.merge(result, h_summury, left_index=True, right_index=True)

    return result


def main():
    url_first = 'https://race.netkeiba.com/race/shutuba.html?race_id=202006020511'
    result = first(url_first)
    goal_2020 = get_url_2020(url_first)
    final = race_result(goal_2020, result)
    return final

if __name__ == '__main__':
    main()