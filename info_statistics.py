from post import Post
import re

INFO_DETAILS = 'http://119.254.102.70:8080/crawler-source/infodetails.do'
LIST = 'http://119.254.102.70:8080/crawler-source/info/list.do'
USERID = 28
ROWS = 1700

def get_avg_download_times(info_id, p):
	r = p.session.get(INFO_DETAILS, params={'id': info_id})
	html = r.content.decode('utf-8')
	value_list_line = [x for x in html.split('\n') if 'var valueList =' in x][0]
	lst = re.sub(r'var valueList =|[\r\t;]', r'', value_list_line)
	valueList = eval(lst) # valueList = [.., ..]
	# get average download times
	avg = sum(valueList) / len(valueList)
	return avg

if __name__ == "__main__":
	p = Post()
	p.logon()

	items = p.session.post(LIST,{'userid':USERID,'rows':ROWS})

	res = items.content.decode('utf-8')

	infos = eval(res)['infos']

	count = 0
	total = len(infos)
	
	f = open('statistics','a')
	
	for info in infos:
		print(count, '/', total)
		id = info['id']
		regionName = info['regionName']
		website = info['website']
		websiteplate = info['websiteplate']
		avg_download_times = get_avg_download_times(id, p)
		url = info['url']

		whole_string = " ".join([str(id), regionName, website, websiteplate, str(avg_download_times), url]) + '\n'
		print(whole_string)
		# write columns to file

		f.write(whole_string)
		count += 1 

	f.close()
