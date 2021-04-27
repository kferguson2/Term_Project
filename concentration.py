import csv
import urllib.request
import pprint
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



# def main():
#     import pprint
#     url = DOWNLOAD_URL
#     # print(url)
#     # print(parse_html(download_page(url)))
#     concentrations_list = parse_html_concentration_list(download_page(DOWNLOAD_URL))
#     # pprint.pprint(concentrations_list)
#     # print(concentrations_list[2])

url = DOWNLOAD_URL
concentrations_list = parse_html_concentration_list(download_page(DOWNLOAD_URL))
concentrations_dict = (parse_html(concentrations_list,download_page(url)))
extra_ba = ['QTM2000', 'MKT4530', 'OIM3525', 'OIM3535', 'MOB3536', 'OIM3580', 'OIM3640']
concentrations_dict['Business Analytics'].extend(extra_ba)
extra_cmf = ['QTM3625']
concentrations_dict['Computational and Mathematical Finance'].extend(extra_cmf)
concentrations_dict['Computational and Mathematical Finance'].remove('ECN3620')
concentrations_dict['Computational and Mathematical Finance'].remove('QTM3612')
econ = concentrations_dict['Economics'][:15]
# print(econ)
concentrations_dict['Economics'] = econ

extra_entre = ['EPS3502', 'EPS3503', 'EPS3508', 'EPS420', 'EPS3509', 'EPS3531', 'EPS4530', 'EPS4534']
concentrations_dict['Entrepreneurship'].extend(extra_entre)

index_env = concentrations_dict['Environmental Sustainability'].index('SUS4600')
concentrations_dict['Environmental Sustainability'][:index_env]
extra_env = ['NST2080', 'HSS2080', 'NST2090', 'HSS2090', 'NST2011', 'ECN2611', 'CVA2013', 'SUS2600', 'SCN3630']
concentrations_dict['Environmental Sustainability'].extend(extra_env)

extra_fin = ['FIN4520', 'FIN4521']
concentrations_dict['Finance'].extend(extra_fin)

extra_id = ['HUM4600', 'LIT4682']
concentrations_dict['Identity and Diversity'].extend(extra_id)

concentrations_dict['Information Technology Management'] = ['OIM3640', 'OIM3690', 'OIM3505', 'OIM3525', 'OIM3555', 'OIM3560', 'OIM3605', 'OIM3610', 'OIM3615', 'OIM3565', 'OIM3580', 'OIM2645', 'OIM3525', 'OIM3545', 'MKT3515', 'MKT4530', 'QTM2601', 'OIM3620', 'OIM3635', 'OIM3645', 'OIM3655', 'QTM3674']

concentrations_dict['International Business Environment'].pop(-1)

concentrations_dict['Justice, Citizenship, and Social Responsibility'].append('CVA2010')

extra_lead = ['MOB3514', 'MOB3515']
concentrations_dict['Leadership'].extend(extra_lead)

concentrations_dict['Legal Studies'].append('LAW3605')

extra_lit = ['VSA4610', 'LVA2067']
concentrations_dict['Literary and Visual Arts'].extend(extra_lit)

index_man = concentrations_dict['Managerial Financial Planning and Analysis'].index('ACC4530')
concentrations_dict['Managerial Financial Planning and Analysis'] = concentrations_dict['Managerial Financial Planning and Analysis'][:index_man]

concentrations_dict['Marketing'] = ['MKT4505', 'MKT3510', 'MKT4506', 'MKT4530','MKT3500', 'MKT3501', 'MKT3515', 'MKT3540', 'MKT3550', 'MKT3574', 'MKT3575', 'EPS3580', 'MKT4510', 'MKT4515', 'MKT4520', 'MKT4560']

extra_op = ['OIM3573', 'OIM3509', 'OIM3517', 'OIM3519', 'MOB3536', 'MIS3535', 'DES3600']
concentrations_dict['Operations Management'].extend(extra_op)

extra_qtm = ['QTM2600', 'QTM3620']
concentrations_dict['Quantitative Methods'].extend(extra_qtm)

concentrations_dict['Real Estate'] = ['FIN3511', 'FIN3512', 'FIN3555', 'FIN3565', 'FIN4571']

index_rscm= concentrations_dict['Retail Supply Chain Management'].index('EPS3525')
concentrations_dict['Retail Supply Chain Management'] = concentrations_dict['Retail Supply Chain Management'][:index_rscm]
concentrations_dict['Retail Supply Chain Management'].append('OIM3573')

index_stat = concentrations_dict['Statistical Modeling'].index('QTM2600')
concentrations_dict['Statistical Modeling'] = concentrations_dict['Statistical Modeling'][:index_stat]

extra_strat = ['M0B3540', 'MOB3545', 'MOB3546', 'MOB3555', 'MOB3514']
concentrations_dict['Strategic Management'].extend(extra_strat)

extra_ted = ['EPS3501', 'EPS3503', 'EPS3504', 'EPS3513', 'EPS3531', 'EPS3537', 'EPS3541', 'EPS4515', 'EPS4523', 'OIM3635']
concentrations_dict['Technology, Entrepreneurship, and Design'].extend(extra_ted)

# pprint.pprint(concentrations_dict['Technology, Entrepreneurship, and Design'])
#identity and diversity



# if __name__ == '__main__':
#     main()