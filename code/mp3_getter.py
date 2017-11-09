import urllib.request
import time
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import shutil

# from the accent.gmu website, pass in list of languages to scrape mp3 files and save them to disk
def mp3getter(lst):
    for j in range(len(lst)):
        for i in range(1,lst[j][1]+1):
            while True:
                try:
                    print("Downloading")
                    urllib.request.urlretrieve("http://accent.gmu.edu/soundtracks/{0}{1}.mp3".format(lst[j][0], i), '{0}{1}.mp3'.format(lst[j][0], i))
                    print("Downloaded")
                except:
                    time.sleep(2)
                else:
                    break

# from list of languages, return urls of each language landing page
def lang_pages(lst):
    urls=[]
    for lang in lst:
        urls.append('http://accent.gmu.edu/browse_language.php?function=find&language={}'.format(lang))
    return urls

#output:
#
# ['http://accent.gmu.edu/browse_language.php?function=find&language=amharic',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=arabic',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=bengali',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=bulgarian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=cantonese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=dutch',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=english',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=farsi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=french',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=german',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=greek',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=hindi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=italian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=japanese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=korean',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=kurdish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=macedonian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=mandarin',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=miskito',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=nepali',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=pashto',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=polish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=portuguese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=punjabi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=romanian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=russian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=serbian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=spanish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=swedish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=tagalog',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=thai',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=turkish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=ukrainian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=urdu',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=vietnamese']

# from each language whose url is contained in the above list, save the number of speakers of that language to a list
def get_nums(lst):
    nums = []
    for url in lst:
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        test = soup.find_all('div', attrs={'class': 'content'})
        nums.append(int(test[0].find('h5').text.split()[2]))
    return nums



def get_speaker_info(start, stop):
    '''
    Inputs: two integers, corresponding to min and max speaker id number per language
    Outputs: Pandas Dataframe containing speaker filename, birthplace, native_language, age, sex, age_onset of English
    '''

    user_data = []
    for num in range(start,stop):
        info = {'speakerid': num, 'filename': 0, 'birthplace':1, 'native_language': 2, 'age':3, 'sex':4, 'age_onset':5}
        url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={}".format(num)
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        body = soup.find_all('div', attrs={'class': 'content'})
        try:
            info['filename']=str(body[0].find('h5').text.split()[0])
            bio_bar = soup.find_all('ul', attrs={'class':'bio'})
            info['birthplace'] = str(bio_bar[0].find_all('li')[0].text)[13:-6]
            info['native_language'] = str(bio_bar[0].find_all('li')[1].text.split()[2])
            info['age'] = float(bio_bar[0].find_all('li')[3].text.split()[2].strip(','))
            info['sex'] = str(bio_bar[0].find_all('li')[3].text.split()[3].strip())
            info['age_onset'] = float(bio_bar[0].find_all('li')[4].text.split()[4].strip())
            user_data.append(info)
        except:
            info['filename'] = ''
            info['birthplace'] = ''
            info['native_language'] = ''
            info['age'] = ''
            info['sex'] = ''
            info['age_onset'] = ''
            user_data.append(info)
        df = pd.DataFrame(user_data)
        df.to_csv('speaker_info_{}.csv'.format(stop))
    return df

# copy files from one list of wav files to a specified location
def copy_files(lst, path):
    for filename in lst:
        shutil.copy2('{}.wav'.format(filename), '{}/{}.wav'.format(path, filename))


if __name__=="__main__":
    langauges=['hindi','kannada']
    a=lang_pages(langauges)
    print(a)
    b=get_nums(a)
    print(b)
    new_list=[['hindi',b[0]],['kannada',b[1]]]
    print(new_list)
    mp3getter(new_list)