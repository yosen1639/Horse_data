import numpy as np
import pandas as pd

def search(url):
    global df1,df2,df3
    scr = pd.read_html(url)
    if len(scr[3]) < 4:
        df1 = scr[4]
    else:
        df1 = scr[3]
    df2 = scr[2]
    df3 = scr[1]

#出走取り消しの馬を除外
def remove_horse(df,racename,year):
    global past_data
    past_data = df[df['レース名'] == racename]
    past_data = past_data[df['日付'].str[:4] == str(year)]

    if past_data['着順'].values[0] != '取':
        return True

#'タイム','着順','馬場','人気','騎手','馬番','馬体重','馬体重増減','脚質'
def make():
    #検索対象レース名についてのデータを抜き出し
    summury = past_data[['タイム','着順','馬場','人気','騎手','馬番','馬体重']]

    #タイムを秒表記に変換
    time = summury['タイム'].values[0]
    retime = float(time[0])*60 + float(time[2:4]) + float(time[5])/10
    summury['タイム'] = retime

    #馬体重を馬体重と増減に変換
    weight = summury['馬体重'].values[0]
    reweight = int(weight[:3])
    summury['馬体重'] = reweight

    #馬体重増減ゼロの場合を除外
    if weight[4] == '0':
        weight_change = 0
    else:
        weight_change = weight[-4:-1]
        weight_change = int( weight_change.strip('(') )
    summury['馬体重増減'] = weight_change

    #脚質、データ取ってきて加工
    go = past_data['通過'].values[0][0:2].rstrip('-')
    #1-3を0、4-8を1、9-13を2、14-18を3
    if int(go) <= 3:
        summury['脚質'] = 0
    if int(go) >= 4 and int(go) <= 8:
        summury['脚質'] = 1
    if int(go) >= 9 and int(go) <= 13:
        summury['脚質'] = 2
    if int(go) >= 14:
        summury['脚質'] = 3
    return summury

#前走レース名、着順・前走5走順位、上がり
def make2(df,summury):
    #対象レースの行のindexを取得
    now_place = past_data.index
    next_place = now_place[0] + 1
    summury['前走レース名'] = df.at[next_place,'レース名']
    summury['前走着順'] = df.at[next_place,'着順']

    #前走5走の着順、上がり
    start = int(past_data.index[0]) + 1
    total_rank = 0
    total_end = 0
    for i in range(min(5,len(df)-start)):
        if df.at[start + i, '着順'] != df.at[start + i, '着順']:
            start += 1
        if df.at[start+i,'着順'] == '取' or df.at[start+i,'着順'] == '中':
            start += 1
        total_rank += int(df.at[start + i,'着順'])

    start = int(past_data.index[0]) + 1
    for i in range(min(5,len(df)-start)):
        #Nanを飛ばす
        while(df.at[start + i,'上り'] != df.at[start + i,'上り']):
            start += 1
        total_end += int(df.at[start + i, '上り'])
    summury['前走5走着順'] = total_rank / 5
    summury['前走5走上り'] = total_end / 5

    #コース適正、、、開催地求めてから3着内割合
    held = past_data['開催'].values[0][1:3]
    held_list = df['開催'].values
    similar = []
    for i in range(len(held_list)):
        #Nanを除く
        if held_list[i] == held_list[i]:
            if held_list[i][1:3] == held:
                similar.append(i)
    total_suit = 0
    for i in df.loc[similar,'着順'].values:
        if i != '取' and i != '中':
            total_suit += int(i)
    summury['コース適正'] = total_suit/len(df.loc[similar,'着順'].values)
    return summury

#血統、
def make3(df,summury):
    summury['血統'] = df[0][0]
    return summury

def main(url_past,year,racename):
    search(url_past)
    if remove_horse(df1,racename,year):
        collect_data = make()
        collect_data = make2(df1,collect_data)
        collect_data = make3(df2,collect_data)
        return collect_data
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    main()

