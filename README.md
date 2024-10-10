# Data Analyst Jobs Web Scraper

This project is a web scraping tool designed to extract data about data analyst jobs from Wuzzuf.net. The scraper uses Python and BeautifulSoup to collect job information such as:

- **Job Titles**
- **Company Names**
- **Locations**
- **Required Skills**
- **Job Responsibilities**
- **Salaries**
- **Links**

The collected data is saved to a CSV file for further analysis.

## Project Structure

- **data_analyst_jobs.py**: The main script that handles scraping the job data and saving it into a CSV file.
- **requirements.txt**: List of required Python libraries to run the project.

## Features

- **Web scraping**: Extracts job data directly from Wuzzuf.net.
- **Data collection**: Gathers detailed information such as job titles, companies, locations, and links to the job listings.
- **CSV Export**: Outputs the collected data into a CSV file for easy use and analysis.

##Current Issues
There is an ongoing issue with extracting data for the following fields:

- **Salary: The salary column sometimes returns "Salary not specified" even when the salary is available on the job listing.
- **Job Requirements: The job responsibilities column occasionally fails to extract complete requirement details.
  
I plan to fix these issues in future updates. If you have any suggestions or a potential solution, feel free to reach out to me.
