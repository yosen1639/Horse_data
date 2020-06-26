import requests
import bs4
import pandas as pd
import data_collect

#検索ページから該当レースの抜き出し
def get_url(url, result, racename):
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    #転移先のurlを取得したい、該当箇所を抜きだし
    elem = soup.select('#contents_liquid tr td a')

    sites = []
    for i in elem:
        site = i.get('href')
        if len(site) == 19:
            #サイト名が省略されているので足す
            sites.append('https://db.netkeiba.com/'+ site)

    df = pd.read_html(url)[0]
    #該当レースの番号を抜き出し
    a = df[df['レース名'] == racename].index
    for i in a:
        result.append(sites[i])
    return result

#それぞれの年のレースから各馬のページに移動
def get_url2(url):
    global horse_url
    horse_url = []
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    # 転移先のurlを取得したい、該当箇所を抜きだし
    elem = soup.select('a')
    for i in elem:
        t = i.get('href')
        if t[1:6] == 'horse':
            horse_url.append('https://db.netkeiba.com/' + t)

def race_result(period, goal, racename):
    year = 2019
    for i in range(period):
        df = pd.read_html(goal[i])[0]
        result = pd.DataFrame(columns=['馬名', '性別', '馬齢'])
        result['馬名'] = df['馬名']
        result['性別'] = df['性齢'].str[0]
        result['馬齢'] = df['性齢'].str[1].astype(int)

        get_url2(goal[i])
        h_summury = pd.DataFrame(columns=['タイム','着順','馬場','人気','騎手','馬番','馬体重',
                                          '馬体重増減','脚質','前走レース名','前走着順','前走5走着順',
                                          '前走5走上り','コース適正','血統'])
        for j in range(len(horse_url)):
            h = data_collect.main(horse_url[j], year, racename)
            if len(h) == 1:
                h_new = h.rename(index={h.index[0]:j})
                h_summury = pd.concat([h_summury, h_new])
            print(h_summury)

        result = pd.merge(result, h_summury, left_index=True, right_index=True)
        if i == 0:
            final = result
        else:
            final = pd.concat([final, result], ignore_index=True)
        year -= 1

    return final

def main():
    url_move_1 = 'https://db.netkeiba.com/?pid=race_list&word=%5E%CA%F5%C4%CD%B5%AD%C7%B0'

    goal = []
    goal = get_url(url_move_1, goal, '宝塚記念(G1)')
    #goal = get_url(url_move_2, goal, '有馬記念(G1)')

    final = race_result(10, goal, '宝塚記念(G1)')
    return final

if __name__ == '__main__':
    main()
