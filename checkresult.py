# -*- coding: utf-8 -*-
# @Author: E-NoR
# @Date:   2022-10-09 06:25:44
# @Last Modified by:   E-NoR
# @Last Modified time: 2022-10-15 00:32:14
from collections import namedtuple
from json import loads
import pandas as pd
from datetime import datetime

# md5List = ('ed0be53097a9da90ee037896396142c2','09eaae1844ccbafcbdb2a5ed2a2f79c3')
md5List = ("2022", "2023")


# nid = '14718'
def get_holiday(md5List):
    # fixDate = lambda x: ''.join(v if i == 0 else v.zfill(2) for i,v in enumerate(x.split('/')))
    for idx, md5 in enumerate(md5List):
        # yearData = loads(requests.get(f'https://data.gov.tw/qc_download/dq_download_json.php?nid={nid}&md5_url={md5}').text)
        with open(f"./yearData/{md5}.json", "r", encoding="utf-8") as f:
            yearData = loads(f.read())
        if idx == 0:
            # holiday2021 = tuple(fixDate(i['Start Date']) for i in yearData if i['All Day Event'] == 'TRUE')
            holiday2022 = tuple(i["西元日期"] for i in yearData if i["是否放假"] == "2")
        elif idx == 1:
            holiday2023 = tuple(i["西元日期"] for i in yearData if i["是否放假"] == "2")
    return {*holiday2022, *holiday2023}


def dateList(beginDate, range=30):
    date = {
        datetime.strftime(x, "%Y%m%d")
        for x in list(pd.date_range(start=str(beginDate), periods=range))
    }
    return sorted(date) if range == 7 else date


def main(checkDate, money, customHolidays):
    # checkDate = '20211008'
    yearData = get_holiday(md5List)
    suggestType = namedtuple("建議日期", "起始日, 省下費用, 區間自費, 總費用")
    suggest, normal, currentMoney = (), (), -1000
    outputFMT = lambda x: pd.DataFrame(x, columns=suggestType._fields).to_markdown(
        tablefmt="pretty", showindex=False
    )

    startCheck = tuple(dateList(checkDate, 7))
    print("------------------------------------------------------------------")
    print("未來七日價格參考")
    result = "未來七日價格參考"
    for startDay, 起始日 in enumerate(startCheck, start=1):
        dateRange = dateList(起始日)
        payDate = (
            startDay - len(set(startCheck[:startDay]) & yearData) - 1 - customHolidays
        )
        省下費用 = (
            1280 - ((30 - len(yearData & dateRange) - customHolidays) * money << 1)
        ) * -1
        區間自費 = 區間自費 if (區間自費 := (money << 2) * payDate) > 0 else 0
        起始日 = f"{起始日[:4]}/{起始日[-4:-2]}/{起始日[-2:]}"
        if (最高省下 := 省下費用 - 區間自費) >= currentMoney:
            if 最高省下 > currentMoney:
                suggest = tuple()
            currentMoney = 最高省下
            suggest += (suggestType(起始日, 省下費用, 區間自費, 最高省下),)
        normal += (suggestType(起始日, 省下費用, 區間自費, 最高省下),)
    result = "\n".join(
        (
            result,
            norOutput := outputFMT(normal),
            "七日內建議起始日",
            sugOutput := outputFMT(suggest),
        )
    )
    print(norOutput)
    print("七日內建議起始日")
    print(sugOutput)
    return result


if __name__ == "__main__":
    while (checkDate := input("請輸入起始日期: ")).isdigit() != True or len(checkDate) != 8:
        print("請輸入數字，日期為必填，參照格式：20211008")
    while (money := input("請輸入單程費用: ")).isdigit() != True and money in range(25, 61, 5):
        print("請輸入數字，費用為必填，區間為 25~60")
    while (
        customHolidays := input("請輸入自訂假日天數: ")
    ).isdigit() != True and customHolidays in range(11):
        if not customHolidays:
            customHolidays = 0
    main(int(checkDate), int(money), int(customHolidays))
