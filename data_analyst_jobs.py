import csv
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest

BASE_URL = "https://wuzzuf.net"

def fetch_job_data(url):
    """Fetches the job data from the provided URL and returns the parsed content."""
    result = requests.get(url)
    return result.content

def parse_job_data(content):
    """Parses the job data from the page content and extracts job titles, companies, locations, skills, links, and salaries."""
    soup = BeautifulSoup(content, "lxml")
    
    # Initialize lists for storing extracted data
    job_titles, company_names, locations, job_skills, links, salaries, responsabilites = [], [], [], [], [], [], []
    
    # Extract job titles and links
    job_title_elements = soup.find_all("h2", {"class": "css-m604qf"})
    for title in job_title_elements:
        job_titles.append(title.text.strip())
        link_element = title.find("a")
        if link_element and 'href' in link_element.attrs:
            job_link = link_element.attrs['href']
            if not job_link.startswith("http"):
                job_link = BASE_URL + job_link  # Append base URL if relative link
            links.append(job_link)
        else:
            links.append("No link available")  # Fallback in case the link is missing
    
    # Extract company names
    company_name_elements = soup.find_all("a", {"class": "css-17s97q8"})
    for company in company_name_elements:
        company_names.append(company.text.strip().replace("-", ""))
    
    # Extract job locations
    for listing in soup.find_all("div", {"class": "css-d7j1kk"}):
        location_element = listing.find("span", {"class": "css-5wys0k"})
        if location_element:
            locations.append(location_element.text.strip())
        else:
            locations.append("Not specified")
    
    # Extract job skills, filtering out unwanted keywords
    exclude_keywords = {"Full Time", "Remote", "On-site", "Part-time", "Hybrid"}
    job_skill_elements = soup.find_all("div", {"class": "css-y4udm8"})
    for skill_element in job_skill_elements:
        skill_links = skill_element.find_all("a")
        skills = [
            skill.text.strip().replace("·", "").strip() 
            for skill in skill_links 
            if skill.text.strip() not in exclude_keywords
        ]
        if skills:
            job_skills.append(", ".join(skills))
        else:
            job_skills.append("No skills listed")  # Fallback in case no skills are found

    # Extract salary for each job 
    for link in links:
        if link != "No link available":  # Ensure the link is valid before fetching
            result = requests.get(link)
            job_page_soup = BeautifulSoup(result.content, "lxml")
    
        # Find the div with class "css-rcl8e5" for salary
            salary_div = job_page_soup.find("div", {"class": "css-rcl8e5"})
            if salary_div:
            # Find the specific nested span containing the salary info
                salary_span = salary_div.find("span", {"class": "css-4xky9y"})
                if salary_span:
                    salaries.append(salary_span.text.strip())  # Extract "Confidential" or actual salary
                else:
                    salaries.append("Salary not specified")
            else:
                salaries.append("Salary not specified")
        else:
            salaries.append("No salary available")  # Fallback for invalid links

        # Extract responsibilities
        requirememnts = job_page_soup.find("div", {"class":"css-1uobp1k"})  # Fetch from the job page
        if requirememnts:  # Check if the element was found
            req = requirememnts.find("ul")
            if req:  # Ensure the ul element exists
                respon_text = ""
                for li in req.find_all("li"):
                    respon_text += li.text + "| "
                responsabilites.append(respon_text.strip())  # Remove trailing space
            else:
                responsabilites.append("No responsibilities listed")
        else:
            responsabilites.append("No responsibilities listed")

    # Return all extracted data
    return job_titles, company_names, locations, job_skills, salaries, responsabilites, links

def save_to_csv(file_path, data):
    """Saves the job data to a CSV file."""
    with open(file_path, "w", newline="", encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["Job Title", "Company Name", "Location", "Skills", "Salary", "responsabilites", "Link"])
        wr.writerows(zip_longest(*data, fillvalue=""))

def main():
    # URL of the data analyst jobs page
    url = "https://wuzzuf.net/search/jobs/?q=data%20analyst&a=navbg"
    
    # Fetch and parse job data
    page_content = fetch_job_data(url)
    job_titles, company_names, locations, job_skills, salaries, responsabilites, links = parse_job_data(page_content)
    
    # Save the extracted data to a CSV file
    file_path = "E:\\projects\\WebScraping\\data_analyst_jobs\\data_analyst_jobs.csv"
    save_to_csv(file_path, [job_titles, company_names, locations, job_skills, salaries, responsabilites, links])
    
if __name__ == "__main__":
    main()
