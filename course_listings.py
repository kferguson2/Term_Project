import csv
import urllib.request
from bs4 import BeautifulSoup

def generate_url(program, term, year):
    """ 
    Generates a url based on parameters
    program (string): Undergraduate or Graduate
    term (string): Fall, Spring, Winter, or Summer
    year (int): Year that the term is in

    # add in section to make first letters upper
    # add in some raise exception error messages when inputting wrong
    """
    url = f'https://fusionmx.babson.edu/CourseListing/index.cfm?fuseaction=CourseListing.DisplayCourseListing&blnShowHeader=true&program={program}&semester={term}+{year}&sort_by=course_number&btnSubmit=Display+Courses'
    return url

# url = generate_url('Undergraduate','Fall', 2021)

def download_page(url):
    return urllib.request.urlopen(url)


# print(download_page(url).read())


def parse_html(html):
    """
    Currently returning a tuple of course no. and title
    Getting repeats of classes becasue its every section of that class like: 
    (ACC1000-01,INTRODUCTION TO FINANCIAL ACCOUNTING
    ACC1000-02,INTRODUCTION TO FINANCIAL ACCOUNTING)
    Do we want to include day/times and instructors or figure out way to elimate the duplicates?

    Also for some of the courses when it converted to a csv it added "" around the title not sure why 
    because it doesn't have the quotations when you print(course_title)
    """
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    course_table = soup.find_all('table')[1]
    # print(course_table)
    course_list = []
    for course_row in course_table.find_all('tr')[4:]: # for some reason first 4 lines were none or <td> Course No.
        course_num = course_row.find('td', attrs={'width': 85}).string
        # print(course_num)
        # course_code = course_num[0].strip()
        # # print(course_code)
        # section_num = course_num[1].strip()
        # print(section_num)
        course_title = course_row.find('td', attrs={'width': 250}).string.strip()
        course_day_time = course_row.find('td', attrs={'width': 140}).get_text().split(' ', 1)
        # print(course_day_time)
        prof = course_row.find('td', attrs={'width': 140})
        # print(prof)
        course_nodes = course_row.findChildren('td')
        # print(course_nodes)
        professor = course_nodes[4].string
        if professor != None:
            professor = professor.strip()
        # print(professor)
        if len(course_day_time) == 2:
            course_day = course_day_time[0].strip()
            course_time = course_day_time[1].strip()
        else:
            course_day = course_day_time[0].strip()
        if [course_num, course_title, course_day, course_time] not in course_list:
            course_list.append([course_num, course_title, course_day, course_time, professor])
    return course_list



# parse_html(download_page(url).read())


def main():
    url = generate_url('Undergraduate','Fall', 2021)

    with open('data/course_listings.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        fields = ('Course No.', 'Title', 'Day(s)', 'Time', 'Professor')
        writer.writerow(fields)

        html = download_page(url)
        courses = parse_html(html)
        writer.writerows(courses)


if __name__ == '__main__':
    main()