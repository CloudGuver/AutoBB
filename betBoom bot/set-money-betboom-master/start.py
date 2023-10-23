from bs4 import BeautifulSoup
import requests
import re

url = "https://t.me/s/dota2_robot"

page = requests.get(url)
page.encoding = "utf-8"
post_list =[]




def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # смайлики
        u"\U0001F300-\U0001F5FF"  # символы и пиктограммы
        u"\U0001F680-\U0001F6FF"  # транспорт и картинки
        u"\U0001F1E0-\U0001F1FF"  # флаги стран
                           "]+", flags=re.UNICODE)
    
    cleaned_text = emoji_pattern.sub(r'', text)
    return cleaned_text




if page.ok:
    soup = BeautifulSoup(page.content, "html.parser")
    post_list = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")

    text_list =[]
    #team_name_regex = r'([^\s]+) VS ([^\s]+)Карта \d+.*?([0-9]+\.[0-9]+)%'
    for msg in post_list:
        text = ' '.join(msg.stripped_strings).split("Канал Ботяры")[1].split("Ставь только то,")[0]
       
        text = remove_emojis(text) 
        #print(extract_info(text))
        text_list.append(text)
        #print(text)
    



#print(text_list)




        
        




teams = []
maps = []
odds = []
for item in text_list:
    team_match = re.search(r'(?i)([a-zA-Z\s]+) VS ([a-zA-Z\s]+)', item)
    map_match = re.search(r'(?i)Карта (\d+)', item)
    odds_match = re.findall(r'(?i)([a-zA-Z\s]+):\s([\d.]+)%', item)
    print(team_match.group(1),team_match.group(2),map_match.group(1),odds_match)
    
    if team_match:
        teams.append([team_match.group(1), team_match.group(2)])
    
    if map_match:
        maps.append(map_match.group(1))
        
    if odds_match:
        odds.append(odds_match)

print("Команды:", teams)
print("Номера карт:", maps)
print("Коэффициенты:", odds)

        