import csv
import urllib.request
from bs4 import BeautifulSoup
global DOWNLOAD_URL 
DOWNLOAD_URL = 'https://www.babson.edu/academics/undergraduate-school/concentrations/'


def download_page(url):
    return urllib.request.urlopen(url)


# print(download_page(DOWNLOAD_URL).read())'
def parse_html_concentration_list(html):
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    concentration_table = soup.find('ul', attrs={'class':'multilevel-linkul-1'})
    # print(concentration_table)
    concentrations_list = []
    # print(concentration_table)
    for concentration_row in concentration_table.find_all('li'):
        # print(concentration_row)
        try:
            concentration_detail = concentration_row
            concentrations_list.append(concentration_detail.string)
        except:
            pass
    return concentrations_list

# print(type("a"))
def parse_html(concentrations_list, html):
    global DOWNLOAD_URL
    concentrations_dict = dict()
    for i in concentrations_list:
        # print(i)
        str_i = str(i)
        # print(str_i)
        clean_i = str_i.replace(",", "")
        clean_i = clean_i.replace(" ", "-")
        clean_i = clean_i.lower()
        # print(clean_i)
        usuable_url = f"{DOWNLOAD_URL}{clean_i}"
        # print(usuable_url)
        soup = BeautifulSoup(download_page(usuable_url), features="html.parser")
        # print(soup.prettify())
        concentration_table = soup.find('div', attrs={"class": "u-margin-bottom--30"})
        req_course_list = []
        # print(concentration_table)
        for concentration_row in concentration_table.find_all('li'):
            try:
                details = concentration_row.string.split(' ')
                course_number = details[0] + details[1]
                if len(course_number)==7:
                    if course_number not in req_course_list:
                        req_course_list.append(course_number)
            
            except:
                pass
            concentrations_dict[i] = req_course_list
    return concentrations_dict



def main():
    import pprint
    url = DOWNLOAD_URL
    # print(url)
    # print(parse_html(download_page(url)))
    concentrations_list = parse_html_concentration_list(download_page(DOWNLOAD_URL))
    # pprint.pprint(concentrations_list)
    # print(concentrations_list[2])
    pprint.pprint(parse_html(concentrations_list,download_page(url)))


if __name__ == '__main__':
    main()