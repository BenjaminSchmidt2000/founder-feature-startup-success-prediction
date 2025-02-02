import os
import json
import random
import time
import csv
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

# access the variables
linked_email = os.getenv('LINKEDIN_EMAIL')
linked_password = os.getenv('LINKEDIN_PASSWORD')

def get_random_user_agent():
    user_agents = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",

        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",

        # Chrome on Linux
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",

        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",

        # Firefox on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:90.0) Gecko/20100101 Firefox/90.0",

        # Firefox on Linux
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",

        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",

        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.59 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.902.55 Safari/537.36 Edg/92.0.902.55",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.961.38 Safari/537.36 Edg/93.0.961.38",

        ]
    return random.choice(user_agents)

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

    return webdriver.Chrome(options=chrome_options)

# Login to LinkedIn
def linkedin_login(driver, linked_email, linked_password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 7))
    driver.find_element(By.NAME, "session_key").send_keys(linked_email)
    time.sleep(random.uniform(2, 5))
    driver.find_element(By.NAME, "session_password").send_keys(linked_password)
    time.sleep(random.uniform(2, 6))
    driver.find_element(By.CSS_SELECTOR, "button.btn__primary--large").click()
    time.sleep(random.uniform(7, 12))
    print("Logged in successfully.")


def clean_text(text):
    """Helper function to clean text by removing newline characters, extra spaces, and unnecessary whitespace."""
    # Replace newlines with spaces and remove leading/trailing whitespace
    text = text.replace('\n', ' ').strip()
    
    # Replace multiple spaces with a single space
    text = ' '.join(text.split())
    
    return text

def parse_dates(dates_text):
    """Helper function to parse dates and split them into start and end dates."""
    dates_parts = dates_text.split('·')[0].strip()
    if 'Present' in dates_parts:
        start_date, end_date = dates_parts.split(' - Present')
        end_date = 'Present'
    else:
        start_date, end_date = dates_parts.split(' - ')
    return clean_text(start_date), clean_text(end_date)

def nested_experience(section,company_name,company_elements=""):
    nested_experience_data = {}

    try:
        # Extract the job title from the nested experience
        title_xpath = ".//div[contains(@class, 't-bold')]//span[1]"
        title_element = section.find_element(By.XPATH, title_xpath)
        nested_experience_data['title'] = title_element.text.strip()

        nested_experience_data['company_name'] = company_name
        if company_elements:
            nested_experience_data['company_linked_url'] = company_elements.get_attribute("href")
        else:
            nested_experience_data['company_linked_url']="No url for company"
        # Extract the dates and split them into start_date and end_date
        dates_text_element = section.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')]")
        nested_experience_data['start_date'], nested_experience_data['end_date'] = parse_dates(dates_text_element.text)

        # Extract the location (optional) from the nested experience
   
        location_xpath = ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')][2]"
        try:
            location_element = section.find_element(By.XPATH, location_xpath)
            location_text = location_element.text.strip()
            
            # Replace newline characters with spaces
            location_text = location_text.replace('\n', ' ')
            
            # Remove any duplicate entries
            location_parts = location_text.split()
            unique_location_parts = list(dict.fromkeys(location_parts))
            nested_experience_data['location'] = ' '.join(unique_location_parts)
        
        except NoSuchElementException:
            nested_experience_data['location'] = ''

        # print('nested exp:::',nested_experience_data)
        return nested_experience_data

    except NoSuchElementException as e:
        print(f"Required element not found in nested experience. Details: {e}")
    except Exception as e:
        print(f"An error occurred while processing the nested experience: {e}")

    return nested_experience_data

def scrape_experience_details(driver,show_more_button):
   
    experiences=[]
    
    try:
        
        ul_element = driver.find_element(By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
        print("Parent ul found")
        
        # # Find all education entries within the <ul>
        experience_sections = ul_element.find_elements(By.XPATH, "./li")
        experience=scrape_experience(driver,experience_sections,show_more_button)
        return experience

    except TimeoutException:
        print("The 'ul' element was not found or the page took too long to load.")
    except NoSuchElementException:
        print("The 'ul' element was not found on the page.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return experiences

def scrape_experience(driver, li_list, show_more_button):
    time.sleep(random.uniform(7, 10))
    experiences = []

    try:
        for section in li_list:
            try:
                experience = {}

                # Extract company name from the main section
                title_element = section.find_element(By.XPATH, ".//div[contains(@class, 't-bold')]//span[1]")
                company_para = clean_text(title_element.text)

                # Check if there is a "Show More" button
                if show_more_button  and section.find_elements(By.XPATH, ".//div/div/div/div/ul/li/div/div/div/ul/li"):
                    # Find nested <li> elements if "Show More" is clicked or available
                    
                    next_nested_li = section.find_elements(By.XPATH, ".//div/div/div/div/ul/li/div/div/div/ul/li")
                    if next_nested_li and show_more_button:
                        print("Nested DEEP <li> found.")
                        # print(f"Number of nested <li> elements found: {len(next_nested_li)}")
                        for li in next_nested_li:
                            next_nested_company_elem = section.find_element(By.CSS_SELECTOR, "a.optional-action-target-wrapper.display-flex")            
                            if next_nested_company_elem:
                                next_nested_experience_data = nested_experience(li, company_para,next_nested_company_elem)
                            else:
                                next_nested_experience_data = nested_experience(li, company_para)
                            experiences.append(next_nested_experience_data)
                
                    continue  # Skip further processing and move to the next section

                # If no "Show More" button, check for nested <li> directly
                nested_li = section.find_elements(By.XPATH, ".//div/div/div/ul/li[span]")
                
                if nested_li: 
                    print("Nested <li> found.")
                    # print(f"Number of nested <li> elements found: {len(nested_li)}")
    
                    for li in nested_li:
                        try:

                            
                            nested_company_elem = section.find_element(By.CSS_SELECTOR, 'a[data-field="experience_company_logo"]')
            
                        except Exception as e:
                            print(f"An error occurred while retrieving the nested company URL: {e}")
                        if nested_company_elem:
                            nested_experience_data = nested_experience(li, company_para,nested_company_elem)
                        else :
                            nested_experience_data = nested_experience(li, company_para)
                        experiences.append(nested_experience_data) 
                      # Add nested experiences to main experiences list
                
                    continue  # Skip this <li> if it has a nested <ul>
                
                # If no nested <li> or "Show More", proceed with normal extraction
                # experience['title'] = clean_text(title_element.text)
                experience['title'] = company_para  # Assuming company_para is the job title
                
                # Extract and clean company name
                company_name_element = section.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and not(contains(@class, 't-black--light'))][1]")
                company_name_text = clean_text(company_name_element.text)
                company_name_text = ' '.join(company_name_text.split())  # Remove extra spaces
                company_name_parts = company_name_text.split(' ')
                company_name_text = ' '.join(sorted(set(company_name_parts), key=company_name_parts.index))

                # company_link = section.find_element(By.CSS_SELECTOR, 'a[data-field="experience_company_logo"]')
                # experience['company_linked_url']=company_link
                # Remove unwanted characters or repeated words
                for word in ['Full-time', 'Internship', 'Part-time']:
                    company_name_text = company_name_text.split(word)[0].strip()

                experience['company_name'] = company_name_text

                try:
                    # Locate all matching elements with the selector
                    
                    # Check if at least one matching element exists and select the first one
                    if show_more_button:
                        next_nested_company_elem = section.find_element(By.CSS_SELECTOR, "a.optional-action-target-wrapper.display-flex")
                        experience['company_linked_url'] = next_nested_company_elem.get_attribute("href") 
                         
                    elif ( not show_more_button) and section.find_element(By.CSS_SELECTOR, 'a[data-field="experience_company_logo"]'):
                        company_elements= section.find_element(By.CSS_SELECTOR, 'a[data-field="experience_company_logo"]')
                        company_url = company_elements.get_attribute("href")  # Get the URL from the first element
                        experience['company_linked_url'] = company_url
                    else:
                        print("No LinkedIn URL found for the company.")
                except Exception as e:
                    print(f"An error occurred while retrieving the company URL: {e}")


                # Extract company location
                try:
                    location_element = section.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')][2]")
                    location_text = clean_text(location_element.text).replace('\u00b7', '').strip()
                    location_text = location_text.split('.')[0].strip()
                    experience['location'] = ' '.join(dict.fromkeys(location_text.split())).strip()

                    for keyword in ['Hybrid', 'Remote', 'On-site']:
                        experience['location'] = experience['location'].split(keyword)[0].strip()

                    if experience['location'] in ['Hybrid', 'Remote', 'On-site']:
                        experience['location'] = ''

                except NoSuchElementException:
                    experience['location'] = ''  # Set to an empty string if location is not found

                # Extract dates and split them into start_date and end_date
                dates_text_element = section.find_element(By.XPATH, ".//span[contains(@class, 't-black--light') and contains(@class, 't-14') and contains(@class, 't-normal')][1]")
                experience['start_date'], experience['end_date'] = parse_dates(dates_text_element.text)

                # Append the extracted information to the experiences list
                # print('SIMPLE exp:::', experience)
                experiences.append(experience)
                
            except NoSuchElementException as e:
                print(f"Required element not found in this section. Skipping this section. Details: {e}")
            except Exception as e:
                print(f"An error occurred while processing this section: {e}")

    except TimeoutException:
        print("The 'ul' element was not found or the page took too long to load.")
    except NoSuchElementException:
        print("The 'ul' element was not found on the page.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return experiences

def extract_experience(driver):
    time.sleep(random.uniform(7, 10))
    experiences = []

    try:
        experience_section = driver.find_element(By.XPATH, "//h2[contains(@class,'pvs-header__title')]//span[contains(@aria-hidden,'true')][normalize-space()='Experience']/ancestor::section")

        # Locate the parent ul element
        ul_element = experience_section.find_element(By.XPATH, ".//ul")
        print("Parent ul found")
        
        show_more_button = experience_section.find_elements(By.XPATH, ".//div[contains(@class,'pvs-list__footer-wrapper')]//a[contains(@class, 'optional-action-target-wrapper')]")
        # print('Button Found')
        li_list = ul_element.find_elements(By.XPATH, "./li")
        # print(f"Number of PARENT <li> elements found: {len(li_list)}")
        if show_more_button:
            print("Button present")
            # Click on the button to load the full education details page
            show_more_button[0].click()
            print("Button clicked, navigating to full experience page...")

            # Wait for the new page to load
            time.sleep(random.uniform(5, 8))  # Adjust time if necessary
            
            # Print confirmation that the new page has loaded
            print("Page loaded")
            experience=scrape_experience_details(driver,show_more_button)
        
            back_button= driver.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
            print('BACK button found')
            back_button.click()
            print('button clicked')
            time.sleep(random.uniform(7, 12)) 
            # print(experience)
            return experience
            # experiences = scrape_experience(driver)
                
        else:
            # If no "Show All" button is present, scrape the current page
            experience = scrape_experience(driver,li_list,show_more_button)
            return experience

    except TimeoutException:
        print("The 'ul' element was not found or the page took too long to load.")
    except NoSuchElementException:
        print("The 'ul' element was not found on the pageeeeeeeeee.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return experiences
# Call the function with your driver instance

def scrape_education(driver,ul_element):
    # Wait for the page to load
    

    try:  
        # Initialize an empty list to store education details
        education_details = []

        # Find all education entries within the <ul>
        education_sections = ul_element.find_elements(By.XPATH, "./li")
        
        for entry in education_sections:
            try:
                # Extract the institution
                institution = entry.find_element(By.CSS_SELECTOR, "a.optional-action-target-wrapper > div > div > div > div").text.strip()
                institution = institution.split('\n')[0]  # Remove any repeated values
            except Exception:
                institution = "N/A"
            
            try:
                    # Locate all matching elements with the selector
                    uni_elements = entry.find_elements(By.CSS_SELECTOR, 'a.optional-action-target-wrapper')

                    # Check if at least one matching element exists and select the first one
                    if uni_elements:
                        uni_url = uni_elements[0].get_attribute("href")  # Get the URL from the first element
                        # print("Uni url::",uni_url)
                    else:
                        print("No LinkedIn URL found for the uni.")
            except Exception as e:
                    uni_url=""

            try:
                # Extract the degree
                 # Extract the degree by checking the structure
                degree_span = entry.find_elements(By.XPATH, ".//span[contains(@class, 't-14') and not(contains(@class, 't-black--light'))]")
                degree = degree_span[0].text.strip() if degree_span else ""  # Use first matched element if available
                degree = degree.split('\n')[0]  # Remove any repeated values
            except Exception:
                degree = ""
                
            try:
                # Extract the time period
                time_period = entry.find_element(By.CSS_SELECTOR, "span.t-14.t-black--light").text.strip()
                time_period = time_period.split('\n')[0]  # Remove any repeated values

                # Split the time period into start_date and end_date
                if "-" in time_period:
                    start_date, end_date = map(str.strip, time_period.split("-"))
                else:
                    start_date, end_date = time_period, "Present"
            except Exception:
                start_date, end_date = "N/A", "N/A"
            
            # Append the details to the list
            education_details.append({
                'degree': degree,
                'institution': institution,
                'uni_url':uni_url,
                'start_date': start_date,
                'end_date': end_date
            })
    
    except Exception as e:
        print(f"An error occurred while scraping education details: {e}")
    
    return education_details

def scrape_education_details(driver):
    # Wait for the page to load
    time.sleep(random.uniform(5, 9))
    
    # Initialize an empty list to store education details
    education_details = []

    try:
        # Locate the education section using XPath
        ul_element = driver.find_element(By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
        print("Parent ul found")
        
        # # Find all education entries within the <ul>
        education_sections = ul_element.find_elements(By.XPATH, "./li")
        
        for entry in education_sections:
            try:
                # Extract the institution
                institution = entry.find_element(By.XPATH, ".//a[contains(@class, 'optional-action-target-wrapper')]/div/div/div[1]/div").text.strip()
                institution = institution.split('\n')[0]  # Remove any repeated values
            except Exception:
                institution = "N/A"
            
            try:
                # Locate all matching elements with the selector
                uni_elements = entry.find_elements(By.CSS_SELECTOR, 'a.optional-action-target-wrapper')

                # Check if at least one matching element exists and select the first one
                if uni_elements:
                    uni_url = uni_elements[0].get_attribute("href")  # Get the URL from the first element
                    # experience['uni_linked_url'] = uni_url
                    # print("Uni url::",uni_url)
                else:
                    print("No LinkedIn URL found for the uni.")
            except Exception as e:
                    uni_url= " "

            try:
                # Extract the degree
                 # Extract the degree by checking the structure
                degree_span = entry.find_elements(By.XPATH, ".//span[contains(@class, 't-14') and not(contains(@class, 't-black--light'))]")
                degree = degree_span[0].text.strip() if degree_span else ""  # Use first matched element if available
                degree = degree.split('\n')[0]  # Remove any repeated values
            except Exception:
                degree = ""
                
            try:
                # Extract the time period
                time_period = entry.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-black--light')]").text.strip()
                time_period = time_period.split('\n')[0]  # Remove any repeated values

                # Split the time period into start_date and end_date
                if "-" in time_period:
                    start_date, end_date = map(str.strip, time_period.split("-"))
                else:
                    start_date, end_date = time_period, "Present"
            except Exception:
                start_date, end_date = "N/A", "N/A"
            
            # Append the details to the list
            education_details.append({
                'degree': degree,
                'institution': institution,
                'uni_url':uni_url,
                'start_date': start_date,
                'end_date': end_date
            })
    
    except Exception as e:
        print(f"An error occurred while scraping education details: {e}")
    
    return education_details

def extract_education(driver):
    # Wait for the page to load
    time.sleep(random.uniform(4, 8))

    try:
        # Locate the education section by finding the h2 header with 'Education'
        education_section = driver.find_element(By.XPATH, "//h2[contains(@class,'pvs-header__title')]//span[contains(@aria-hidden,'true')][normalize-space()='Education']/ancestor::section")
        print("Education section found")

        # Now, find the ul element within the located section
        ul_element = education_section.find_element(By.CSS_SELECTOR, "div > ul")
        print("Education ul found")
        
        # Check for the "Show All" button below the ul element
        show_more_button = education_section.find_elements(By.XPATH, ".//div[contains(@class,'pvs-list__footer-wrapper')]//a[contains(@class, 'optional-action-target-wrapper')]")
        
        if show_more_button:
            print("Button present")
            # Click on the button to load the full education details page
            show_more_button[0].click()
            print("Button clicked, navigating to full education page...")

            # Wait for the new page to load
            time.sleep(random.uniform(5, 8))  # Adjust time if necessary
            
            # Print confirmation that the new page has loaded
            print("Page loaded")
            
            education_details = scrape_education_details(driver)

            back_button= driver.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
            print('BACK button found')
            back_button.click()
            print('button clicked')
           

        else:
            # If no "Show All" button is present, scrape the current page
            education_details = scrape_education(driver,ul_element)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    # Return the scraped education details
    return education_details

def human_like_scroll(driver, max_scroll_attempts=30, scroll_delay=0.5):
    """
    Continuously scrolls down the page in small increments, simulating human-like scrolling.
    Attempts to load new content up to a maximum number of scroll attempts. Stops if no new content is loaded.
    """
    scroll_attempts = 0
    last_scroll_position = driver.execute_script("return window.scrollY;")  # Get the current scroll position
    
    while scroll_attempts < max_scroll_attempts:
        # Scroll down by a small amount
        driver.execute_script("window.scrollBy(0, 200);")  # Adjust the value for scroll increment as needed
        time.sleep(scroll_delay)  # Wait a bit between each scroll to simulate human scrolling

        # Get the new scroll position
        current_scroll_position = driver.execute_script("return window.scrollY;")

        # If the scroll position hasn't changed, we've reached the bottom
        if current_scroll_position == last_scroll_position:
            print("Reached the bottom of the page. No more content to load.")
            break  # Exit the loop if no more content is loaded

        # Update the last scroll position
        last_scroll_position = current_scroll_position

        # Increment the scroll attempts counter
        scroll_attempts += 1

        # Periodically print status to monitor scrolling
        if scroll_attempts % 5 == 0:
            # print(f"Scrolled down {scroll_attempts} times.")

            print("Finished human-like scrolling (or reached max attempts).")


def scroll_to_bottom(driver):
    """Scrolls to the bottom of the page twice, waits, and then scrolls back to the top."""
     # Slowly scroll to the bottom
    human_like_scroll(driver)
    
    # Wait for a few seconds after scrolling down
    time.sleep(random.uniform(5, 8))
    print("Waiting at the bottom before scrolling up.")

    # Scroll back to the top
    driver.execute_script("window.scrollTo(0, 0);")
    print("Scrolled back to the top.")


def scrape_profile(driver,url):
    driver.get(url)
    time.sleep(random.uniform(4, 8))

    profile_name_element = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/main/section/div/div/div/div/span/a/h1")
    profile_name = profile_name_element.text


    profile_url = driver.current_url
    username = profile_url.split('/')[-2]
    # username_encoded = urllib.parse.quote(username, safe='')

    location_element = driver.find_element(By.CSS_SELECTOR, ".text-body-small.inline.t-black--light.break-words")
    location = location_element.text.strip()
    # location_encoded = urllib.parse.quote(location, safe='')
    about_text=" "
    try:
    # Locate the "About" section if it exists
        about_section = driver.find_element(By.XPATH, "//h2[contains(@class,'pvs-header__title')]//span[contains(@aria-hidden,'true')][normalize-space()='About']/ancestor::section")
        
    # Locate the <div> element within the "About" section if it exists
        about_div = about_section.find_element(By.CSS_SELECTOR, "div.inline-show-more-text--is-collapsed.inline-show-more-text--is-collapsed-with-line-clamp.full-width")
        print('about section found')
    # Then, find the <span> element within it and get the visible text
        about_text = about_div.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
        # print(about_text)  # Print or store the text as needed
    except Exception as e:
    # If the "About" section or any nested element is missing, print a message or log it, and continue
        print("About section not found, continuing with other elements.")


    activity_section= driver.find_element(By.XPATH, "//h2[contains(@class,'pvs-header__title')]//span[contains(@aria-hidden,'true')][normalize-space()='Activity']/ancestor::section")
    # Locate the <p> element first

    followers_element = activity_section.find_element(By.CSS_SELECTOR, "p.pvs-header__optional-link.text-body-small")
    # Then, find the <span> element within it and get its text
    followers_text = followers_element.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
    # print(followers_text)
    show_activity_button = activity_section.find_element(By.XPATH, "//footer")

    show_activity_button.click()
    print('All activity page loaded')
    time.sleep(random.uniform(2, 7))
    
    posts_list = []
    comments_list=[]
    reactions_list = []

    try:
  
        posts_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Posts')]]")
        posts_button.click()
        print("Posts button clicked.")
        time.sleep(random.uniform(4, 7))
        scroll_to_bottom(driver)
        
        # ul_xpath = "//*[@id='profile-content']//section//div[2]//ul[contains(@class, 'display-flex') and contains(@class, 'flex-wrap') and contains(@class, 'list-style-none') and contains(@class, 'justify-center')]"
        ul_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
        ul_element = ul_container.find_element(By.XPATH, "./ul")

        # Locate the li elements within the ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        # li_elements = ul_container.find_elements(By.CSS_SELECTOR, "li.profile-creator-shared-feed-update__container")
        
        # print(f"Total posts: {len(li_elements)}")
        time.sleep(2)
        for  li in li_elements:
            post_text = li.text.strip() 
            if post_text:
                posts_list.append(post_text)
            # print(li.text)
       
    except NoSuchElementException:
        print("Posts button not found.")

    try:
    # Locate and click the "Posts" button if it exists
        
        comments_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Comments')]]")
        comments_button.click()
        print("Comments button clicked.")
        time.sleep(random.uniform(4, 7))
        scroll_to_bottom(driver)
        # time.sleep(random.uniform(3, 7))
        # ul_xpath = "//*[@id='profile-content']//section//div[2]//ul[contains(@class, 'display-flex') and contains(@class, 'flex-wrap') and contains(@class, 'list-style-none') and contains(@class, 'justify-center')]"
        # li_elements = driver.find_elements(By.CSS_SELECTOR, "li.profile-creator-shared-feed-update__container")
        
        ul_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
        ul_element = ul_container.find_element(By.XPATH, "./ul")

        # Locate the li elements within the ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        
        # print(f"Total posts: {len(li_elements)}")
        time.sleep(2)
        for  li in li_elements:
            comment_text = li.text.strip()  
            if comment_text:  # Check if the text is not empty
                comments_list.append(comment_text)
            # print(li.text)
       
    except NoSuchElementException:
        print("Comments button not found.")

    try:
    # Locate and click the "Reactions" button if it exists

        reactions_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Reactions')]]")
        reactions_button.click()
        time.sleep(random.uniform(4, 7))
        print("Reactions button clicked.")
        scroll_to_bottom(driver)
       
        # li_elements = driver.find_elements(By.CSS_SELECTOR, "li.profile-creator-shared-feed-update__container")
        # print(f"Total reactions: {len(li_elements)}")
        ul_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
        ul_element = ul_container.find_element(By.XPATH, "./ul")

        # Locate the li elements within the ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        
        
        time.sleep(2)
        
        for  li in li_elements:
            reaction_text = li.text.strip()  
            if reaction_text:  # Check if the text is not empty
                reactions_list.append(reaction_text)
            # print(li.text)
        # print('reactions ul list found')

    except NoSuchElementException:
        print("Reactions button not found.")
    
    driver.get(url)
    print(f"Navigated back to homepage")

    time.sleep(5)
    experience_details = extract_experience(driver)
    education_details = extract_education(driver)

    final_json = {
        "username": username,
        "about":about_text,
        "followers": followers_text,
        "posts":posts_list,
        "comments":comments_list,
        "reactions":reactions_list,
        "Location_Name": location,
        "profile_name": profile_name,
        "experience": experience_details,
        "education": education_details
    }
    # print(final_json)
    return final_json

def main():
    # Read URLs from CSV using pandas
    founder_df = pd.read_csv(r"C:\Users\priiy\Downloads\thesis yuno - rohan\founder_linkedin_url.csv")  # Assuming the column with URLs is named "LinkedIn_url"
    
    # Initialize WebDriver
    driver = init_browser()
    
    # Create a list to store batch profile data
    batch_profile_data = []
    
    try:
        # Login to LinkedIn (provide your credentials)
        linkedin_login(driver, linked_email, linked_password)
        
        # Iterate over URLs from the DataFrame
        for index, row in founder_df.iloc[9000:9200].iterrows():  # Adjust slicing as needed
            linkedin_url = row['Linkedin_url']  # Assuming the column containing the URLs is named 'LinkedIn_url'
            print(f"Scraping profile: {linkedin_url}")
            
            try:
                # Scrape the profile data
                profile_data = scrape_profile(driver, linkedin_url)
                
                # Append profile data to the current batch list
                batch_profile_data.append(profile_data)
                
                # Save individual profile data to a JSON file
                profile_filename = f"profile_{index + 1}.json"
                with open(profile_filename, "w", encoding="utf-8") as f:
                    json.dump(profile_data, f, ensure_ascii=False, indent=4)
                print(f"Saved individual profile to {profile_filename}")
                
            except Exception as e:
                # If an error occurs during scraping, log the error and continue
                print(f"Error scraping {linkedin_url}: {e}")
            
            # Sleep for a random time to avoid rate limiting
            time.sleep(random.uniform(2, 5))
            
            # Check if 50 profiles have been scraped or if it's the last profile
            if (index + 1) % 50 == 0 or (index + 1) == len(founder_df.iloc[1:500]):
                # Save the batch data to a JSON file
                start_index = (index // 50) * 50 + 1
                end_index = index + 1
                batch_filename = f"profile_data_{start_index}_{end_index}.json"
                with open(batch_filename, "w", encoding="utf-8") as f:
                    json.dump(batch_profile_data, f, ensure_ascii=False, indent=4)
                print(f"Saved batch to {batch_filename}")
                
                # Clear the batch list for the next 50 profiles
                batch_profile_data = []
                
                # Go to LinkedIn homepage and wait if it's a 50-profile checkpoint
                if (index + 1) % 50 == 0:
                    print("Taking a break, returning to homepage.")
                    driver.get("https://www.linkedin.com")
                    # Wait for a random time between 5 to 10 minutes
                    time.sleep(random.uniform(300, 600))
        
        print("All profiles scraped and saved.")
    
    finally:
        driver.quit()

# Run the main function
main()

