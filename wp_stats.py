import re
import datetime
import requests
import json

site_number_regex = '(?<=https://public-api.wordpress.com/rest/v1.1/sites/)\d+?(?=/stats/visits)';
cookie_regex = '(?<=-H \'cookie: ).*?(?=\')'
auth_regex = '(?<=-H \'authorization: ).*?(?=\')'

def extract(regex, s, name):
	r = re.search(regex, s)
	if(r == None):
		print "Unable to extract " + name
		exit()
	return r.group(0)

def write_member(f, row):
	for field in row:
		f.write(str(field) + ",")
	f.write("\n")

print "Paste XHR:"
xhr = raw_input();

siteNumber = extract(site_number_regex, xhr, "site number")
cookie = extract(cookie_regex, xhr, "cookie")
auth = extract(auth_regex, xhr, "authorization")

print "Extracted Site Number, Cookie and Auth."
print "Enter date to start stats (DD-MM-YYYY):"
startDate = datetime.datetime.strptime(raw_input(), '%d-%m-%Y')
print "Enter date to end stats (DD-MM-YYYY):"
endDate = datetime.datetime.strptime(raw_input(), '%d-%m-%Y')
quantity = (endDate - startDate).days + 1

params = {	'unit': 'day', 
			'stat_fields': 'views,visitors,likes,comments,post_titles',
			'quantity': str(quantity),
			'date': '{0}-{1}-{2}'.format(endDate.year, endDate.month, endDate.day)}

headers = {'cookie': cookie, 'authorization': auth}

url = 'https://public-api.wordpress.com/rest/v1.1/sites/{0}/stats/visits'.format(siteNumber)

r = requests.get(url, headers=headers, params=params)
jdata = json.loads(r.text)

with open('stats.csv', 'w') as f:
	write_member(f, jdata['fields'])
	for row in jdata['data']:
		write_member(f,row)

print "Complete! Saved to stats.csv"