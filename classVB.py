from bs4 import BeautifulSoup as bs
import requests as req

class VB:

	def __init__(self, url):
		self.url = url;
		self.soup = 'blank';

	def retrieve(self):
		try:
			pyforum = req.get(self.url);
		except:
			return 'pyforum did not make request'
		soup = bs(pyforum.text, 'html.parser')

		self.soup = soup;

		return soup.title;

	def totals(self, obj, name):
		stats = self.soup.find('ul', {'class': 'forum-stats-bits'})
		children = stats.findChildren();
		count = 0
		for child in children:
			if (count > 0):
				# print(child.contents[0])
				pass
			if (count == 2):
				num = list(child.contents[0])
				truenum = []
				for x in num:
					if x != ',':
						truenum.append(x)
				strnumber = ''.join(truenum)
				number = int(strnumber);
				obname = name + "discussions"
				obj[obname] = number
			if (count == 4):
				num = list(child.contents[0])
				truenum = []
				for x in num:
					if x != ',':
						truenum.append(x)
				strnumber = ''.join(truenum)
				number = int(strnumber);
				obname = name + "messages"
				obj[obname] = number
			if (count == 6):
				num = list(child.contents[0])
				truenum = []
				for x in num:
					if x != ',':
						truenum.append(x)
				strnumber = ''.join(truenum)
				number = int(strnumber);
				obname = name + "members"
				obj[obname] = number
			count += 1

		return obj;
