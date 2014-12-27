from BeautifulSoup import BeautifulSoup as make_soup
from BeautifulSoup import Tag
from urllib2 import urlopen as get
from json import dumps as to_json

import sys

dept, url = sys.argv[1:3]
soup = make_soup(get(url).read())
courses = soup.findAll('div', attrs={'class': 'course'})
report = {}

for course in courses:
  courseid = course.previousSibling.previousSibling['name'].strip()
  number = course.find('p', attrs={'class': 'courseNumber'}).contents[0].strip()
  try:
    title = course.find('p', attrs={'class': 'courseTitle'}).contents[0].strip()
  except:
    title = 'No title available.'
  try:
    desc = course.find('div', attrs={'class': 'courseDesc'}).find('p').contents[0].strip()
  except:
    desc = 'No description available.'
  attrs = course.findAll('p', attrs={'class': 'courseAttrs'})
  report[courseid] = {
    'courseNumber': number,
    'courseTitle': title,
    'courseDescription': desc,
    'prerequisites': [],
    'corequisites': [],
    'concurrent': []
  }
  for asoup in attrs:
    line = ' '.join(s.text if isinstance(s, Tag) else s.strip() for s in asoup)
    colon_index = line.index(':')
    k, v = line[:colon_index].strip(), line[colon_index + 1:].strip()
    if k in ('PR', 'CR', 'CO'):
      links = asoup.findAll('a', attrs={'class': 'clink'})
      ids = []
      for link in links:
        val = link['onclick'].split()[0]
        ids.append(val[val.index('\'') + 1 : -2])
      if k == 'PR':
        report[courseid]['prerequisites'] = ids
      elif k == 'CR':
        report[courseid]['concurrent'] = ids
      elif k == 'CO':
        report[courseid]['corequisites'] = ids
    report[courseid][k] = v

print to_json({dept: report}, indent=4)
