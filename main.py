import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title_list = []
company_names_list = []
lacations_list = []
job_skilles_list = []
links = []
salary = []
requirments_list = []
date_posted_list = []

page_number = 0
while True :
    try :
        path = f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}'
        base_url =" https://wuzzuf.net"
        try :
            results = requests.get(path)
        except Exception as e :
            print(e)
        src = results.content
        soup = BeautifulSoup(src , "lxml")
        # print(soup)

        page_counter = int(soup.find("strong").text)
        if page_number > (page_counter // 15 ) :
            print("pages ended ")
            break

        job_tittles = soup.find_all("h2", {"class":"css-m604qf"})
        company_names = soup.find_all("a", {"class":"css-17s97q8"})
        lacations = soup.find_all("span", {"class":"css-5wys0k"})
        job_skilles = soup.find_all("div", {"class":"css-y4udm8"})
        posted_new = soup.find_all("div" , {"class":"css-4c4ojb"})
        posted_old = soup.find_all("div" , {"class":"css-do6t5g"})
        posted = [*posted_new , *posted_old]


        for i in range(len(job_tittles)):
            job_title_list.append(job_tittles[i].text)
            full_link = base_url+job_tittles[i].find("a").attrs["href"]
            links.append(full_link)
            company_names_list.append(company_names[i].text)
            lacations_list.append(lacations[i].text)
            job_skilles_list.append(job_skilles[i].text)
            date_posted_list.append(posted[i].text)

        page_number+=1
        print("Page switched")
    except Exception as p :
        print(p)
        print(" ERROR OCCURATE")
        break

for link in links :
    try :
        salary_results = requests.get(link)
        salary_src = salary_results.content
        salary_soup = BeautifulSoup(salary_src , "lxml")
        salaries = salary_soup.find("div" , {"class":"css-rcl8e5"})
        print(salaries)
        salary.append(salaries.text)
        requirments = salary_soup.find("div" , {"class":"css-1t5f0fr"}).find("ul")
        requirments_list.append(salaries.text)
    except Exception as l :
        print(l)

file_lists = [job_title_list , company_names_list , lacations_list ,date_posted_list ,job_skilles_list  , requirments_list,links , salary]
exported = zip_longest(*file_lists)

with open("jobs.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(["job tittles" , "company names" , "lacations" , "Date Posted","job skilles" , "requirments" ,"Links" , "Salary"])
    wr.writerows(exported)