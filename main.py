from src.web_scrap import main


main()

import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import interact, interactive, fixed, interact_manual
import pandas as pd
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns

df=pd.read_json('devil_arms.json',orient='records')



def chck(x,game_type_sort=''):
  if not x:
    return False
  if isinstance(x,str):
    return x==game_type_sort
  if game_type_sort in x:
    return True  
  else: 
    return False

def show_dashboards(game_type_sort=None,cloud_character_sort=None,weapon_form_sort=None):
  plt.figure(figsize=(10,20))
  
  
  # гистограмма
  plt.subplot(311)
  if game_type_sort is not None:
    tmp_df=df.copy()
    k=lambda x,game_type_sort: True if game_type_sort in x else False
    tmp_df['Appearances']=tmp_df['Appearances'].apply(lambda x: chck(x,game_type_sort))
    tmp_df=tmp_df[tmp_df['Appearances']]
    tmp_df.groupby('Type').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
    plt.gca().spines[['top', 'right',]].set_visible(False)
  else:
    df.groupby('Type').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
    plt.gca().spines[['top', 'right',]].set_visible(False)




  #облако слов
  plt.subplot(312)
  tmp_df=df.copy()
  if cloud_character_sort:
    tmp_df['User']=tmp_df['User'].apply(lambda x: chck(x,cloud_character_sort))
    tmp_df=tmp_df[tmp_df['User']]
    #print(tmp_df)
  games=defaultdict(lambda:0)
  for i in tmp_df['Appearances']:
    if isinstance(i,str):
      games[i]+=1
    elif isinstance(i,list):
      for j in i:
        games[j]+=1

  wordcloud = WordCloud(background_color='white', # цвет фона
                        colormap = 'gist_heat',      # цветовая палитра
                        width = 600,
                        height = 300,
                        relative_scaling  =1,
                        collocations = False,     # рассматривает слова в отдельности
                        stopwords = STOPWORDS).generate_from_frequencies(games)

  plt.imshow(wordcloud)
  plt.axis('off')







  #круговая
  tmp_df=df.copy()
  if weapon_form_sort:
    tmp_df['Form']=tmp_df['Form'].apply(lambda x: chck(x,weapon_form_sort))
    tmp_df=tmp_df[tmp_df['Form']]
    print(tmp_df)
  characters=defaultdict(lambda:0)
  for i in tmp_df['User']:
    if isinstance(i,str):
      characters[i]+=1
    elif isinstance(i,list):
      for j in i:
        characters[j]+=1
    print(characters)


  new_chars=defaultdict(lambda:0)
  for i in characters:
    if characters[i]>2 or weapon_form_sort:
      new_chars[i]=characters[i]
  new_chars
  plt.subplot(313)
  plt.pie(x = new_chars.values(),
          labels = new_chars.keys(),
          colors = ['#990000','#dddd00','#000099','#990099','#0000dd',
                    '#660000','#660066','#999999'],
          autopct='%1.1f%%',)
  plt.show()







games=defaultdict(lambda:0)
for i in df['Appearances']:
  if isinstance(i,str):
    games[i]+=1
  elif isinstance(i,list):
    for j in i:
      games[j]+=1

games=list(games.keys())
games.append(None)



characters=defaultdict(lambda:0)
for i in df['User']:
  if isinstance(i,str):
    characters[i]+=1
  elif isinstance(i,list):
    for j in i:
      characters[j]+=1
characters=list(characters.keys())
characters.append(None)


forms=defaultdict(lambda:0)
for i in df['Form']:
  if isinstance(i,str):
    forms[i]+=1
  elif isinstance(i,list):
    for j in i:
      forms[j]+=1
forms=list(forms.keys())
forms.append(None)




game_type_sort = widgets.Dropdown(
    options = games,
    description = 'Фильтровать гистограмму по игре:'
)

cloud_character_sort=widgets.Dropdown(
    options=characters,
    description='Фильтровать облако слов по персонажу'
)

weapon_form_sort=widgets.Dropdown(
    options=forms,
    description='Фильтровать облако слов по персонажу'
)


#для изменения каждого параметра должны обновляться выходные
w = interactive(show_dashboards, game_type_sort = [None], cloud_character_sort = [None], weapon_form_sort=[None])
#сразу отображаем все параметры и таблицу
display(w)
