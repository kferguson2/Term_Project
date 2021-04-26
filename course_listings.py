from concentration import concentrations_dict
import urllib.request
from bs4 import BeautifulSoup
import pprint


def generate_url(program, term, year):
    """ 
    Generates a url based on parameters
    program (str): Undergraduate or Graduate
    term (str): Fall, Spring, Winter, or Summer
    year (int): Year that the term is in
    """
    url = f'https://fusionmx.babson.edu/CourseListing/index.cfm?fuseaction=CourseListing.DisplayCourseListing&blnShowHeader=true&program={program}&semester={term}+{year}&sort_by=course_number&btnSubmit=Display+Courses'
    return url



def download_page(url):
    """ Dowloads page url """
    return urllib.request.urlopen(url)



def parse_html(html):
    """
    Parses an html for Babson course listings and returns a list of courses offered that semester

    Information for each course includes: the course number, course title, days/time course is offered, and the professor teaching the course.
    """
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    course_table = soup.find_all('table')[1]
    # print(course_table)
    course_list = []
    for course_row in course_table.find_all('tr')[4:]: # First 4 lines of table were None or row titles (such as Course No.)
        course_code = course_row.find('td', attrs={'width': 85}).string
        course_title = course_row.find('td', attrs={'width': 250}).string.strip()
        course_day_time = course_row.find('td', attrs={'width': 140}).get_text().split(' ', 1)
        prof = course_row.find('td', attrs={'width': 140})
        course_nodes = course_row.findChildren('td')
        children = course_nodes[4].get_text().strip()
        contains_digit = any(map(str.isdigit, children))
        if contains_digit == False:
            professor = children
        if len(course_day_time) == 2:
            course_day = course_day_time[0].strip()
            course_time = course_day_time[1].strip()
        else:
            course_day = course_day_time[0].strip()
        if [course_code, course_title, course_day, course_time] not in course_list:
            course_list.append([course_code, course_title, course_day, course_time, professor])
    temporary_course_list = []
    copy_course_list = course_list.copy()
    for course in copy_course_list:
        course_number = course[0]
        temporary_course_list.append(course_number)
        if temporary_course_list.count(course_number) > 1:
            index_number = temporary_course_list.index(course_number)
            temporary_course_list.pop(index_number)
            course_list.pop(index_number)

    return course_list



def concentration_course_list(concentration, course_list):
    """
    Take a list of all courses being offered and the desired concentration
    Returns a list of courses being offered the fulfill the concentration requirements

    concentration (str): student's concentration (eg. Accounting)
    course_list: list of all available courses
    """
    concentration_courses = [] 
    for course_available in course_list:
        try:
            course_code = course_available[0]
            course_number, section_number = course_code.split('-')
            if course_number in concentrations_dict[concentration]:
                concentration_courses.append(course_available)
        except:
            pass

    return concentration_courses



def course_type_list(course_type, course_list):
    """ 
    Take a list of all courses being offered and the desired course type
    Returns a list of courses all available courses that are the designated course type

    course_type (str): Eg. LVA, CVA, HSS
    course_list: list of all available courses
    """
    available_courses = []

    for course_available in course_list:
        course_code = course_available[0]
        course_type_code = course_code[:3]
        if course_type_code == course_type:
            available_courses.append(course_available)

    return available_courses



def sort_by_course_level_num(course):
    """
    Function that returns the course level number

    Example: course = ACC3500-01, returns 5
    """
    course_code = course[0]
    course_level_num = course_code[4]
    return course_level_num



def course_level_list(course_level, course_list):
    """
    Take a list of all courses being offered and the desired course level
    Returns a list of courses that are available for the given course level

    course_level (str): Advanced Liberal Arts Electives, Advanced Electives, or Free Electives
    """
    advanced_liberal_arts = []
    advanced_electives = []
    free_electives = []
    for course_available in course_list:
        course_code = course_available[0]
        course_level_num = course_code[4]
        if course_level_num == '6':
            advanced_liberal_arts.append(course_available)
            advanced_electives.append(course_available)
            free_electives.append(course_available)
        elif course_level_num == '5':
            advanced_electives.append(course_available)
            free_electives.append(course_available)
        elif course_level_num == '1' or course_level_num == '2':
            free_electives.append(course_available)
        else:
            pass
    if course_level == 'Advanced Liberal Arts Electives':
        return advanced_liberal_arts
    elif course_level == 'Advanced Electives':
        advanced_electives_sorted = sorted(advanced_electives, key=sort_by_course_level_num)
        return advanced_electives_sorted
    else:
        free_electives_sorted = sorted(free_electives, key=sort_by_course_level_num)
        return free_electives_sorted
    



# def main():

#     url = generate_url('Undergraduate','Fall', 2021)

#     html = download_page(url).read()
#     # print(html)

#     course_list = parse_html(html)
#     # print(course_list)

#     concentration_courses = concentration_course_list("Accounting", course_list)
#     # pprint.pprint(concentration_courses)

#     available_courses = course_type_list("HSS", course_list)
#     # pprint.pprint(available_courses)

#     electives_available = course_level_list("Free Electives", course_list)
#     # pprint.pprint(electives_available)

# if __name__ == '__main__':
#     main()