from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_data_from_lazio():
    options = Options()
    options.add_argument("--headless")
    config = configparser.ConfigParser()
    config.read('config.ini')
    data = []


    for section in config.sections():
        if section != "email":
            url = "https://login.laziodisco.it/access/borse"
            driver = webdriver.Chrome(options=options,
                                      executable_path="C:/Users/Asus/Downloads/chromedriver_win32/chromedriver")
            driver.get(url)
            driver.find_element_by_id("username").send_keys(config[section]["username"])
            driver.find_element_by_id("password").send_keys(config[section]["password"])
            driver.find_element_by_css_selector(".btn:not(:disabled):not(.disabled)").click()
            driver.find_element_by_css_selector(".it-header-wrapper .it-nav-wrapper .it-header-navbar-wrapper nav .custom-navbar-toggler").click()
            storico_button = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href=\"/Home/StoricoEsitiPagamenti\"]"))
             )
            storico_button.click()

            table = driver.find_element_by_css_selector(".table-responsive")
            rows = table.find_elements_by_css_selector("tr")
            for row in rows:
                cells = row.find_elements_by_css_selector("td")
                data.append([cell.text for cell in cells])


            send_email(data[1][2], data[1][3], data[1][5], config[section]["reciver_email"], config["email"]["email"], config["email"]["password"])
            data.clear()
            driver.quit()




def send_email(status, amount, block, reciver_email, sender_email, password):

    message = MIMEMultipart()
    message["from"] = "Lazio Disco Checker"
    message["to"] = reciver_email
    message["subject"] = "Lazio scholarship status"
    if status == "Vincitore":
        english_status = "winner"
    else:
        english_status = "excluded"
    x = f"Dear Student\nYour scholarship status is {english_status}, you have {block} payment block and your total scholarship amount is {amount} euros.\nBest regards.\nLazio Disco Checker"
    x1 = f"\n\nCaro Studente\nLa tua borsa di studio è {status}, hai {block} blocco dei pagamenti e l'importo totale della tua borsa di studio e` {amount} euros.\nCordiali saluti.\nLazio Disco Checker"

    message.attach(MIMEText(x+x1))


    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, password)
        smtp.send_message(message)


def credintials(section_name, username, password, reciver_email):
    config = configparser.ConfigParser()
    config.read("config.ini")

    if not config.has_section(section_name):
        config.add_section(section_name)

    config[section_name]["username"] = username
    config[section_name]["password"] = password
    config[section_name]["reciver_email"] = reciver_email

    with open("config.ini", "w") as configfile:
        config.write(configfile)


