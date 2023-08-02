import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from models.linkedin import JobPost


class LinkedIn(object):
    def __init__(self):
        pass

    def extract_linkedin_job_data(self, url):
        try:
            service = Service(executable_path="tmp/chromedriver_linux64/chromedriver")
            options = Options()
            options.add_argument('--headless=new')
            # Initialize the WebDriver (make sure you have the appropriate web driver installed)
            driver = webdriver.Chrome(service=service, options=options)  # Replace 'Chrome' with 'Firefox', or other compatible web driver

            # Open the URL in the WebDriver
            driver.get(url)
            driver.page_source
            # Wait for the "view more" button to appear and click it
            view_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-box__expand-button"))
            )
            view_more_button.click()

            # Wait for the expanded job details to load
            time.sleep(2)

            # Parse the HTML content
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract relevant data from the job post
            job_title = soup.select_one('h1.jobs-details-top-card__job-title').text.strip()
            company_name = soup.select_one('a.jobs-details-top-card__company-url').text.strip()
            location = soup.select_one('span.jobs-details-top-card__bullet').text.strip()
            job_description = soup.select_one('div.jobs-description-content__text').text.strip()

            # Additional data you may want to extract
            # job_type = soup.select_one('span.jobs-box__body--sub-title').text.strip()
            # job_posted_date = soup.select_one('time.jobs-details-top-card__job-posted-date').text.strip()

            # Create a dictionary to store the extracted data
            job_data = {
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'job_description': job_description,
            }

            return job_data

        except NoSuchElementException as e:
            print("Error occurred while locating the element.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            # Close the WebDriver after extracting the data
            driver.quit()


if __name__ == "__main__":
    job_url = "https://www.linkedin.com/jobs/view/3679344643/"
    li = LinkedIn()
    job_post = li.extract_linkedin_job_data(job_url)
    print(job_post)