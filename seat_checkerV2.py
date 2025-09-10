import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import smtplib 
from email.mime.text import MIMEText 
import re

#config
TARGET_SECTION = "BIO-181-071" 
EXPECTED_SEAT_COUNT = "0 / 24 / 0" 
DROPDOWN_TEXT = "View Available Sections for BIO-181"

#email setup - replace with your actual credentials
EMAIL_SENDER = "your_email@gmail.com" 
EMAIL_RECEIVER = "your_email@gmail.com" 
EMAIL_APP_PASSWORD = "your_16_char_app_password"

def send_email_notification(): 
    subject = f"Seat Open Alert for {TARGET_SECTION}!" 
    body = f"A seat has opened for {TARGET_SECTION}! Go register now!" 
     
    msg = MIMEText(body) 
    msg['Subject'] = subject 
    msg['From'] = EMAIL_SENDER 
    msg['To'] = EMAIL_RECEIVER 
 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: 
        server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD) 
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string()) 

#browser setup
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

#navigate to page
driver.get("https://self-serv.morainevalley.edu/Student/Courses/Search?keyword=anatomy%20and%20physiology%20") 
time.sleep(10)

def click_bio181_dropdown():
    try:        
        exact_selectors = [
            f"//button[contains(text(), '{DROPDOWN_TEXT}')]",
            f"//div[contains(text(), '{DROPDOWN_TEXT}')]/parent::button",
            f"//span[contains(text(), '{DROPDOWN_TEXT}')]/parent::button",
            f"//*[contains(text(), '{DROPDOWN_TEXT}')]"
        ]
        
        for selector in exact_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                for elem in elements:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                    time.sleep(1)
                    try:
                        driver.execute_script("arguments[0].click();", elem)
                        time.sleep(2)
                        return True
                    except:
                        try:
                            elem.click()
                            time.sleep(2)
                            return True
                        except:
                            try:
                                ActionChains(driver).move_to_element(elem).click().perform()
                                time.sleep(2)
                                return True
                            except:
                                pass
        return False
    except:
        return False

def check_section_seats():
    try:
        sections = driver.find_elements(By.XPATH, f"//*[contains(text(), '{TARGET_SECTION}')]")
        
        for section in sections:
            try:
                container = section.find_element(By.XPATH, "./ancestor::div[contains(@class, 'section') or contains(@class, 'row') or contains(@class, 'item')][1]")
                container_text = container.text
                
                # look for seat pattern (available/total/waitlisted)
                seat_match = re.search(r'(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{1,2})', container_text)
                if seat_match and not re.search(r'20\d{2}', seat_match.group(0)):
                    seat_count = seat_match.group(0).strip()
                    if seat_count != EXPECTED_SEAT_COUNT:
                        print("SEAT IS OPEN!")
                        send_email_notification()
                        return True
            except:
                continue
        
        return False
    except:
        return False

#main loop
try: 
    while True:
        driver.refresh() 
        time.sleep(15)
        
        if click_bio181_dropdown():
            time.sleep(5)
            if check_section_seats(): 
                break
        
        time.sleep(60) 

finally: 
    driver.quit()
