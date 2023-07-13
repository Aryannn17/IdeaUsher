import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Step 1: Monitor Competitors' Activity

# Configure Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode without opening a browser
driver = webdriver.Chrome(options=chrome_options)

# Login to LinkedIn
def login(username, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    email_input = driver.find_element_by_id('username')
    email_input.send_keys(username)
    time.sleep(1)

    password_input = driver.find_element_by_id('password')
    password_input.send_keys(password)
    time.sleep(1)

    login_button = driver.find_element_by_css_selector('.login__form_action_container button')
    login_button.click()
    time.sleep(2)

# Scrape new connections of competitor decision-makers
def scrape_new_connections():
    driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    connections = soup.select('.mn-connection-card__name')
    new_connections = [conn.text.strip() for conn in connections]

    return new_connections

# Step 2: Analyze Connections' Profiles

# Scrape profile information of a connection
def scrape_profile(connection_name):
    search_input = driver.find_element_by_css_selector('.search-global-typeahead__input')
    search_input.clear()
    search_input.send_keys(connection_name)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    profile_info = soup.select('.pv-about-section .pv-about__summary-text')
    job_description = soup.select('.experience-section .pv-position-entity p')

    return {
        'profile_info': profile_info[0].text.strip() if profile_info else '',
        'job_description': job_description[0].text.strip() if job_description else ''
    }

# Step 3: Message Generation

# Generate a personalized connection request message
def generate_message(profile_info, job_description):
    # Add your personalized message generation logic here
    message = f"Hi, I noticed that you recently joined our industry. I found your profile information and job description quite interesting. Let's connect and explore potential synergies. Regards, Your Name"
    return message

# Step 4: Connection Request

# Send a connection request with a personalized message
def send_connection_request(connection_name, message):
    search_input = driver.find_element_by_css_selector('.search-global-typeahead__input')
    search_input.clear()
    search_input.send_keys(connection_name)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)

    connect_button = driver.find_element_by_css_selector('.artdeco-button--secondary')
    connect_button.click()
    time.sleep(1)

    add_note_button = driver.find_element_by_css_selector('.button-primary-large')
    add_note_button.click()
    time.sleep(1)

    message_input = driver.find_element_by_css_selector('.send-invite__custom-message')
    message_input.send_keys(message)
    time.sleep(1)

    send_button = driver.find_element_by_css_selector('.ml1')
    send_button.click()
    time.sleep(random.randint(3, 6))

# Main script execution
def main():
    # Set your LinkedIn credentials
    username = 'your_username'
    password = 'your_password'

    # Step 1: Monitor Competitors' Activity
    login(username, password)
    new_connections = scrape_new_connections()

    # Step 2: Analyze Connections' Profiles
    for connection_name in new_connections:
        profile_data = scrape_profile(connection_name)

        # Step 3: Message Generation
        message = generate_message(profile_data['profile_info'], profile_data['job_description'])

        # Step 4: Connection Request
        send_connection_request(connection_name, message)

    driver.quit()

if __name__ == '__main__':
    main()
