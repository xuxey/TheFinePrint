import requests
import urllib.parse
import time

url = "https://www.google.com/"
encoded_url = urllib.parse.quote(url)
print(encoded_url)

api_url = "http://172.22.152.6:6969/summarise"
args = "?access_code=access_code1&url=" + encoded_url
response = requests.post(api_url+args, data=open("llm_query/tnc_trial.txt", "r").read(),
                         headers={"Content-Type": "text/plain"})

print(response.status_code)
print(response.text)

if response.status_code != 200:
    time.sleep(2)

    api_url = "http://172.22.152.6:6969/summary"
    args = "?access_code=access_code1&url=" + encoded_url
    response = requests.get(api_url+args)

    print(response.status_code)
    print(response.text)
