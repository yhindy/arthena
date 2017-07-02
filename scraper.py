import requests
from bs4 import BeautifulSoup
import time
import re
import sys

main_url = '/auctions/auction/UK010517'
base_url = 'https://www.phillips.com'
start_id = 101
end_id = 302
base_id = 'itemid'
links_file = 'links.txt'
offset = 3

# class AuctionLot:

# 	def __init__(self, text):

def query(url):
	while True:
		try: 
			r = requests.get(url)
			if r.ok:
				return r.text
		except requests.exceptions.ConnectionError:
			print "requests ConnectionError, please make sure you are connected to the internet"
			break

def get_detailed_links(text):
	links = []
	failed = []
	soup = BeautifulSoup(text, 'html.parser')
	for i in range(start_id, end_id):
		item_id = base_id + str(i)
		lot = soup.find(id=item_id)
		tag = lot.find('a')
		if tag != None:
			link = lot.find('a').get('href')
			links.append(link)
		else:
			failed.append(i)
	return links

def write_links(links):
	with open(links_file, 'w') as f:
		for link in links:
			# import pdb; pdb.set_trace()
			f.write(link.encode('utf-8') + '\n')

def read_links():
	links = []
	with open(links_file, 'r') as f:
		for line in f:
			links.append(line.strip())
	return links

def parse_links(links):
	req = requests.get(base_url + links[0])
	soup = BeautifulSoup(req.text, 'html.parser')
	tags = soup.find_all('script')
	data = tags[offset]
	json_data = json.laods(data.string[25:-118]) # the part that is interesting data
	import pdb; pdb.set_trace()
	print data.text[0:100]
	# for link in links:
	# 	attributes = parse_link(link)

def parse_link(link):

	import pdb; pdb.set_trace()


def main():
	if (sys.argv[1] == 0): # read & write links
		html_text = query(base_url + main_url)
		print "Reading links..."
		links = get_detailed_links(html_text)
		print "Writing links..."
		write_links(links)
	else: # parse links
		links = read_links()
		parse_links(links)
		#print links
	

if __name__ == '__main__':
	main()