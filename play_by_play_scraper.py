from distutils.dir_util import copy_tree
import requests
from bs4 import BeautifulSoup

def import_game_codes():
    game_code_location = "1996_1997_plus_game_codes.txt"
    with open(game_code_location, 'r') as file:
        game_codes = [game_code[:-1] for game_code in file.readlines()]

    return game_codes


def convert_time_str_to_float(time_str, quater):
    time_floats = [float(component) for component in time_str.split(":")]
    
    time_float = ((quater-1)*12*60) + (12*60) - ((time_floats[0]*60)+time_floats[1])

    time_float = str(round(time_float / 2880, 6))

    return time_float
 

def is_score(score):
    if len(score) < 3 or len(score) > 7:
        return False
    
    score_lst = score.split("-")

    if len(score_lst) != 2:
        return False
    
    try:
        score_lst = [int(s) for s in score_lst]
        return True
    except:
        return False


def has_quarter_data(data):
    if "q1" in data or "q2" in data or "q3" in data or "q4" in data:
        return data


def get_quarter_data(raw_quarter_data, quarter):
    soup = BeautifulSoup(raw_quarter_data, features="html.parser")
    row_data = soup.findAll("tr")

    quarter_data = []
    for each in row_data:
        try:
            time_raw = each.find("td").text
            score_raw = each.find("td", {"class" : "center"}).text

            if is_score(score_raw):
                normalized_time = convert_time_str_to_float(time_raw, quarter)
                score = score_raw.replace("-", ",")
                row = normalized_time + "," + score
                quarter_data.append(row)
        except:
            continue
    
    return quarter_data

def get_game_data(game_code):
    url = f"https://www.basketball-reference.com/boxscores/pbp/{game_code}.html"
    r = requests.get(url)
    text_by_quarter = list(filter(has_quarter_data, r.text.split("<tr class='thead'")))[1:]

    data = []
    for quarter_idx, raw_quarter_data in enumerate(text_by_quarter):
        data += get_quarter_data(raw_quarter_data, quarter_idx+1)
    
    last_row = data[-1].split(",")
    if int(last_row[1]) > int(last_row[2]):
        winner = 0
    else:
        winner = 1

    data = [row+","+str(winner) for row in data]

    return data


def save_data(data, location):
    with open(location, 'w') as file:
        for row in data:
            file.write(row+"\n")

if __name__ == "__main__":
    game_codes = import_game_codes()
    num_of_codes = len(game_codes)

    for i, game_code in enumerate(game_codes):
        pbp_data = get_game_data(game_code)

        if len(pbp_data) > 30:
            save_data(pbp_data, f"play_by_play/{game_code}.txt")
        else:
            print(f"{game_code} not saved. Vector size: {len(len(pbp_data))}.")

        print(f"[{i+1}/{num_of_codes}] PCT Completed: {round(((i+1)/num_of_codes)*100, 2)}%")






