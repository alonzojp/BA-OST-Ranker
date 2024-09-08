import pip._vendor.requests as requests
from bs4 import BeautifulSoup # type: ignore
import re

url_soundtrack = 'https://bluearchive.fandom.com/wiki/Soundtrack'

def download_ogg(url):
    response = requests.get(url)
    url = url.split('/')[-1]
    url = ''.join(re.split(r"%..", url))
    if response.status_code == 200:
        with open('all_oggs/' + url, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url}")
    else:
        print(f"Failed to download {url}")

def save_audio_from_link(url, download_files):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        audio_links = []
        for audio_tag in soup.find_all('audio', src=True):
            src = audio_tag['src']
            audio_links.append(src[:-34])

        if(download_files):
            if len(audio_links) > 0:
                for link in audio_links:
                    download_ogg(link)
            else:
                print("No audio links found.")
    else:
        print("Failed to grab links.")
    
    return audio_links

def audio_links_to_ost_names(all_audio_links):
    ost_names = []
    for link in all_audio_links:
        processed_link = link.split('/')[-1][:-4]
        ost_names.append(''.join(re.split(r"%..", processed_link)))
    
    return sorted(ost_names)

# ----------------------------------------------------------------------------------------------------

all_audio_links = save_audio_from_link(url_soundtrack, True) # Last Scraped 9/8/2024 03:21 PM
all_ost_names = audio_links_to_ost_names(all_audio_links)
print(all_ost_names)