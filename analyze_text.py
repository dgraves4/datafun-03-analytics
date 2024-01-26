import requests

# Fetching the text
url = 'https://gutenberg.org/cache/epub/1513/pg1513-images.html'
response = requests.get(url)
text = response.text.lower()

print(text)







