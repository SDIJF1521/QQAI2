import requests
import config.yml_DATA
print(requests.get(config.yml_DATA.music_API))