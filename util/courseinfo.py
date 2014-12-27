'''This utility exports the get_course_info function to make it easy to fetch
information about a single course given its course ID.
A course ID is something like "SCI-0921" and can be found in course listing pages
in <a> tags directly above the <div class="course"> tag describing the course it
identifies.
The course.php page is the same page the course listing pages send requests to in
order to get information about courses to fill the tooltip one sees when one clicks
the course links on course list pages.
'''

from BeautifulSoup import BeautifulSoup as make_soup
from BeautifulSoup import Tag
from urllib2 import urlopen as get
from json import dumps as to_json
import sys

base_url = 'http://www.mun.ca/regoff/calendar/course.php?courseId='

def get_course_info(course_id):
  url = base_url + course_id
  try:
    source = get(url).read()
  except:
    print 'Could not get ' + url
    sys.exit()
  soup = make_soup(source)
  courseNumber = soup.find('p', attrs={'class': 'courseNumber'}).contents[0].strip()
  try:
    courseTitle = soup.find('p', attrs={'class': 'courseTitle'}).contents[0].strip()
  except:
    courseTitle = 'No title available.'
  try:
    courseDesc = soup.find('div', attrs={'class': 'courseDesc'}).find('p').contents[0].strip()
  except:
    courseDesc = 'No description available.'
  attrs = soup.findAll('p', attrs={'class': 'courseAttrs'})
  report = {
    'identifier': course_id,
    'courseNumber': courseNumber,
    'courseTitle': courseTitle,
    'courseDesc': courseDesc
  }
  for asoup in attrs:
    line = ' '.join(s.text if isinstance(s, Tag) else s.strip() for s in asoup)
    colon_index = line.index(':')
    k, v = line[:colon_index].strip(), line[colon_index + 1:].strip()
    report[k] = v
  return report

def main():
  if len(sys.argv) != 2:
    print 'Run as `python {0} <course-id>`'.format(sys.argv[0])
    sys.exit(1)
  course_id = sys.argv[1]
  print to_json(get_course_info(course_id), indent=4)


if __name__ == '__main__':
  main()
