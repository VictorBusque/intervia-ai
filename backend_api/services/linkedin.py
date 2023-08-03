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


class LinkedIn(object):
    @staticmethod
    def extract_job_data(url):
        try:
            service = Service(executable_path="tmp/chromedriver_linux64/chromedriver")
            options = Options()
            options.add_argument("--headless=new")
            # Initialize the WebDriver (make sure you have the appropriate web driver installed)
            driver = webdriver.Chrome(service=service, options=options)  # Replace "Chrome" with "Firefox", or other compatible web driver

            # Open the URL in the WebDriver
            driver.get(url)
            # Wait for the "view more" button to appear and click it
            view_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.show-more-less-button"))
            )
            view_more_button.click()

            # Parse the HTML content
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract relevant data from the job post
            job_title = soup.find("h1", {"class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
            company_name = soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
            job_description = soup.find("div", {"class": "show-more-less-html__markup relative overflow-hidden"}).text.strip()

            # Create a dictionary to store the extracted data
            job_data = {
                "title": job_title,
                "company": company_name,
                "description": job_description,
                "url": url
            }
            # Close the WebDriver after extracting the data
            driver.quit()
            return job_data

        except NoSuchElementException as e:
            print("Error occurred while locating the element.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None



if __name__ == "__main__":
    job_url = "https://www.linkedin.com/jobs/view/3679344643/"
    li = LinkedIn()
    job_post = li.extract_job_data(job_url)
    print(job_post)