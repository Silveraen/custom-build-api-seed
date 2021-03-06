
import csv
import json

csv_file = open('BirdsBeingDicks.csv', 'r') # Open read only
json_file = open('BBD.json', 'w')           # Write only JSON
col_names = ("created_utc", "score", "domain", "_id", "title", "author", "ups", "downs", "num_comments", "permalink", "selftext", "link_flair_text", "over_18", "thumbnail", "subreddit_id", "edited", "link_flair_css_class", "author_flair_css_class", "is_self", "name", "url", "distinguished")
read_csv = csv.DictReader(csv_file, col_names);

i=0
for row in read_csv:
	row_necessary = {}
	row_necessary['time'] = row['created_utc']
	row_necessary['score'] = row['score']
	row_necessary['domain'] = row['domain']
	row_necessary['_id'] = row['_id']
	row_necessary['title'] = row['title']
	row_necessary['author'] = row['author']
	row_necessary['ups'] = row['ups']
	row_necessary['downs'] = row['downs']
	row_necessary['num_comments'] = row['num_comments']
	row_necessary['permalink'] = row['permalink']
	row_necessary['name'] = row['name']
	row_necessary['url'] = row['url']
	if i != 0:
		json.dump(row_necessary, json_file, sort_keys=False)
		json_file.write("\n")
	i+=1

json_file.close()
jsonnew = open('BBDNEW.json','w');
with open('BBD.json') as f:
	content = f.readlines()
	for line in content:
		if "\(\)\[\]"  in line:
			line = line.replace("\(","\\(")
			line = line.replace("\)","\\)")
			line = line.replace("\[","\\[")
			line = line.replace("\]","\\]")
		jsonnew.write(line)
f.close()
