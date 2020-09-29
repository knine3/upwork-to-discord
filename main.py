import time
import json
import requests
from html2text import html2text
from datetime import datetime, timedelta
from rss import RSSManager

with open('webhook.json', mode='r') as json_file:
	webhook_url = json.load(json_file)['WEBHOOK_URL']

try:
	with open('urls.txt', 'r') as f:
		urls = f.readlines()
		urls = [url.rstrip() for url in urls]

except FileNotFoundError as err:
	print('[-] urls.txt not found!')

	with open('urls.txt', 'w+') as f:
		print('[+] urls.txt created')

	urls = []


def url_is_new(url_str):
    if url_str in urls:
        return False
    else:
        return True


def get_feed_data():
	rss = RSSManager()
	rss.parse_feed()

	feeds = rss.feed

	for entry in feeds['entries']:
		url = entry['id']

		if url_is_new(url):
			urls.append(url)
			project_title = entry['title'].split(' - Upwork')[0]

			data = {}
			data['content'] = f'**{project_title}**\n' #+ 39*' - ' 
			data['embeds'] = []

			embed = {}
			embed['color'      ] = 7330372
			embed['title'      ] = project_title
			embed['url'        ] = entry['id']
			embed['description'] = html2text(entry['summary'])
			embed['timestamp'  ] = datetime(*entry['published_parsed'][:6]).isoformat()
		  # embed['footer'     ] = {'text': 'This is a sample footer'}

			data['embeds'].append(embed)

			result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

			with open('urls.txt', 'a') as f:
				f.write('{}\n'.format(url))


if __name__ == '__main__':
	while(True):
		print(f'[+] Check @{datetime.now().isoformat()}')
		get_feed_data()
		time.sleep(60)