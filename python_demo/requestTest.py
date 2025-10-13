import requests

r = requests.get('https://api.github.com/events')
print(r.text)
print("="*50)
print(r.content)