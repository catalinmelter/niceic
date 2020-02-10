from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import json
import pandas as pd


def get_informations(driver, i, start_of_post_code):
    name = driver.find_element_by_id('gvContractors_ctl0%d_lblName' % i).text
    address_line = driver.find_element_by_id('gvContractors_ctl0%d_lblAddressLine' % i).text
    post_town = driver.find_element_by_id('gvContractors_ctl0%d_lblPostTown' % i).text
    post_code = driver.find_element_by_id('gvContractors_ctl0%d_lblPostCode' % i).text
    telephone = driver.find_element_by_id('gvContractors_ctl0%d_lblTelephone' % i).text
    email = driver.find_element_by_id('gvContractors_ctl0%d_hlEmail' % i).text
    url = driver.find_element_by_id('gvContractors_ctl0%d_hlUrl' % i).text

    try:
        driver.find_element_by_id('gvContractors_ctl0%d_ACt0' % i)
        approved_contractor = 1
    except NoSuchElementException:
        approved_contractor = 0

    try:
        driver.find_element_by_id('gvContractors_ctl0%d_DISt0' % i)
        domestic_installer = 1
    except NoSuchElementException:
        domestic_installer = 0

    try:
        driver.find_element_by_id('gvContractors_ctl0%d_PAT1t0' % i)
        pat = 1
    except NoSuchElementException:
        pat = 0

    data = {
        'name': name,
        'address_line': address_line,
        'post_town': post_town,
        'start_of_post_code': start_of_post_code,
        'post_code': post_code,
        'telephone': telephone,
        'email': email,
        'url': url,
        'approved_contractor': approved_contractor,
        'domestic_installer': domestic_installer,
        'pat': pat
    }

    return json.dumps(data)


def write(file_name, data):
    with open(file_name, 'a') as fp:
        fp.write(data + '\n')


def scrap_data(driver, start_of_post_code, n, file_name):
    driver.get('https://proximity.niceic.com/mainform.aspx?PostCode=%s' % start_of_post_code)
    for _ in range(n):
        for i in range(3, 10):
            try:
                data = get_informations(driver, i, start_of_post_code)
            except StaleElementReferenceException:
                time.sleep(1)
                data = get_informations(driver, i, start_of_post_code)
            write(file_name, data)

        driver.execute_script("__doPostBack('gvContractors','Page$Next')")
        time.sleep(1.5)


if __name__ == '__main__':
    driver = webdriver.Chrome("C:\\Users\\melte\\OneDrive\\Desktop\\chromedriver.exe")
    post_codes = pd.read_csv('D:\\Workspace\\niceic\\Postcodes.csv')['Postcode District'].values
    for post_code in post_codes:
        print(post_code)
        scrap_data(driver, post_code, 5, "D:\\Workspace\\niceic\\dataset\\%s.txt" % post_code)
    driver.close()
