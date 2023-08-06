import logging

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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import getenv
from json import loads as jsonls

from helpers.configuration import ConfigurationHelper


class LinkedIn(object):

    @staticmethod
    def get_configuration():
        with open(f"configuration/{getenv('ENV')}/selenium.json", "r", encoding="utf8") as f:
            config = jsonls(f.read())
        envs = {
            "SELENIUM_URL": config["url"]
        }
        return config, envs

    @staticmethod
    def extract_job_data(url):
        try:
            logging.info(f"Using Selenium browser driver to access: {url}")
            selenium_url = f"{getenv('SELENIUM_URL')}/wd/hub"
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor=selenium_url,
                options=chrome_options
            )
            logging.debug("Selenium driver connected.")
            # Open the URL in the WebDriver
            driver.get(url)
            logging.debug("Url accessed")
            # Wait for the "view more" button to appear and click it
            view_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.show-more-less-button"))
            )
            view_more_button.click()

            # Parse the HTML content
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract relevant data from the job post
            job_title = soup.find("h1", {
                "class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
            company_name = soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
            job_description = soup.find("div",
                                        {"class": "show-more-less-html__markup relative overflow-hidden"}).text.strip()

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
            logging.error("Error occurred while locating the element.")
            return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    _, envs = LinkedIn.get_configuration()
    ConfigurationHelper.load_config(envs)
    job_url = "https://www.linkedin.com/jobs/view/3679344643/"
    li = LinkedIn()
    job_post = li.extract_job_data(job_url)
    print(job_post)
