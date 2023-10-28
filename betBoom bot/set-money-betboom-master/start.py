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
        u"\U0001F1E0-\U0001FEFF"  # флаги стран
        u"\U0000231B"
                           "]+", flags=re.UNICODE)
    
    cleaned_text = emoji_pattern.sub(r'', text)
    return cleaned_text




if page.ok:
    soup = BeautifulSoup(page.content, "html.parser")
    post_list = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")

    team_list =[]
    #team_name_regex = r'([^\s]+) VS ([^\s]+)Карта \d+.*?([0-9]+\.[0-9]+)%'
    for msg in post_list:
        
        text = '\n'.join(msg.stripped_strings).split("Канал Ботяры")[1].split("Ставь только то,")[0]
        text = remove_emojis(text)
        text = re.sub(r'\n+', '\n', text)
        if "Статистика" in text or "время на обучение" in text:
            continue
        
        if "Матчи сегодня такие" in text:
            text = '\n'.join(msg.stripped_strings).split("Ставь только то,")[0].split(r"\d{2}:\d{2} МСК\n")
            print(text[:1])

        
        
        

        
        
        


        team_list.append(text)
        #print(text)


        



print(team_list)


        
        






        