import requests

url = input('enter your url: ')
content = requests.get(url)
content = content.text

print(content)

