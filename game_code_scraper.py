import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup


def get_all_dates(start_date, end_date):
    # start_date = date(1996, 11, 1) 
    # end_date = date(2020, 5, 28)

    dates = []
    delta = end_date - start_date
    for i in range(delta.days + 1):
        date_ = str(start_date + timedelta(days=i)).split("-")
        dates.append(
            {
                "day" : date_[2],
                "month" : date_[1],
                "year" : date_[0]
            }
        )
    
    return dates


def get_game_codes_from_date(day, month, year):
    # day=1
    # month=11
    # year=1996

    try:
        url = f"https://www.basketball-reference.com/boxscores/?month={month}&day={day}&year={year}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        game_codes = [tag.find("a")["href"][11:-5] for tag in soup.findAll("td", {"class" : "right gamelink"})]
        return game_codes
    except Exception as e:
        print(e, r)
        return []
    

def get_game_codes_from_date_rage(start_date, end_date, file_name):
    dates = get_all_dates(start_date, end_date)

    for i, d in enumerate(dates):
        game_codes = get_game_codes_from_date(d["day"], d["month"], d["year"])

        with open(file_name, "a") as file:
            for game_code in game_codes:
                file.write(game_code+"\n")

        date_str = d["day"]+"-"+d["month"]+"-"+d["year"]
        print(f"Date: {date_str} | Num. Downloaded: {len(game_codes):02} | PCT Complete: {round(((i+1)/len(dates))*100, 2)}%")

if __name__ == "__main__":
    # start = start_date=date(1996, 11, 1)
    start = start_date=date(2021, 10, 15)
    today = end_date=date(2022, 5, 28)
    file_name = "1996_1997_plus_game_codes.txt"

    get_game_codes_from_date_rage(start, today, file_name)
