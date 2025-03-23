import requests
import json
from bs4 import BeautifulSoup as bs




class devil_arm:
    __name=''
    __url=''

    def __init__(self,name:str,url:str):
        self.__url=url
        self.__name=name

    @property
    def name(self):
        return self.__name
    
    @property
    def  url(self):
        return self.__url
    
    def __str__(self):
        return f'name: {self.name}; url: {self.url}'


def get_arms()->list[devil_arm]:
    base_url = "https://devilmaycry.fandom.com/wiki/Weapons_in_the_Devil_May_Cry_series"
    response = requests.get(base_url)

    page = bs(response.text, 'html.parser')
    arms_headers = page.find_all('h4')
    arms = []

    for cur_h in arms_headers:
        link = cur_h.find('a', href=True)
        weapon_name = link.get('title')
        weapon_url = 'https://devilmaycry.fandom.com' + str(link.get('href'))

        if weapon_name and weapon_url:
            arm=devil_arm(weapon_name,weapon_url)
            arms.append(arm)
            print(arm)

    return arms

#type,user,form,apearance
def get_arm_information(arm:devil_arm)->dict[str,list[str]]:
    response = requests.get(arm.url)

    pokemon_soup = bs(response.text, 'html.parser')

    weapon_card = pokemon_soup.find('aside')


    #print(weapon_card)
    head_sections = weapon_card.find_all('section', class_='pi-group')
    #print(head_sections[0])

    data = {}
    data['name']=arm.name
    intrested_headers=['Weapon information','Real-life information']
    intrested_columns=['Type','User','Form','Appearances']

    for col in intrested_columns:
        data[col]=None

    for head in head_sections:
        chck=head.find('h2')

        if chck.text in intrested_headers:

            header_divs=head.find_all('div')
            for header_div in header_divs:
                div_name=header_div.find('h3')
                if div_name is not None and div_name.text in intrested_columns:
                    div_content=header_div.find('div')
                    content_links=div_content.find_all('a')
                    lines=[]
                    if content_links:
                        for link in content_links:
                            if link.text=='DF' or link.text=='SE':
                                continue
                            lines.append(link.text)
                        #print(lines)
                    else:
                        lines=div_content.encode_contents(encoding='utf-8').decode()
                        lines=lines.split('<br/>')
                        if (len(lines)==1):
                            lines=lines[0].split(',')
                        #print(lines)

                    if len(lines)==1:
                        lines=lines[0].replace('<i>','')
                        lines=lines.replace('</i>','')
                    elif len(lines)==0:
                        lines=None
                    else:
                        for i,line in enumerate(lines):
                            lines[i]=lines[i].replace('<i>','')
                            lines[i]=lines[i].replace('</i>','')
                    data[div_name.text]=lines
    #print(data)

    return data

def get_information_all(arms:list[devil_arm])->dict[str,dict[str,list[str]]]:
    data=[]
    for arm  in arms:
        
        data.append(get_arm_information(arm))
        print(arm.name,data[-1])
    return data

def save(data:dict[str,dict[str,list[str]]]):
    with open('devil_arms.json','w') as out:
        json.dump(data,out)

def main():
    arms=get_arms()
    data=get_information_all(arms)
    print(json.dumps(str(data)))
    save(data)

    return data


main()
