# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:06:04 2019

@author: mseno
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 08:26:10 2019

@author: mseno
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 11:55:28 2019

@author: mseno
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Setup your driver path
chrome_path = r"C:\Users\mseno\Desktop\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

# Start at Marketsite Alert page
driver.get("https://wolverineaccess.umich.edu/marketsite_alert.html")
driver.find_element_by_xpath("""//*[@id="content_static"]/p[2]/a/img""").click()

#username = driver.find_element_by_id("login")
#password = driver.find_element_by_id("password")

def clear_uniqname():
    blank_pass = driver.find_element_by_id("password")
    blank_pass.clear()
    blank_uniqname = driver.find_element_by_id("login")
    blank_uniqname.clear()

def user_login():
    user_name_input = input("Enter uniqname: ")
    user_password_input = getpass.getpass("Password: ")
    username = driver.find_element_by_id("login")
    password = driver.find_element_by_id("password")
    username.send_keys(user_name_input)
    password.send_keys(user_password_input)
    driver.find_element_by_xpath("""//*[@id="loginSubmit"]""").submit()
 
# The end user will have to enter their uniqname, password and submit on their own
# Check to see if a valid username and pass are entered
logged_in = False
while logged_in is False:
    try:
        user_login()
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, "duo_form")))
        break
    except TimeoutException:
        print('The username and/or password entered is incorrect.  Please try again.')
        clear_uniqname()

# Get/Check Current URL just to see if we're on the right page
current_url = driver.current_url
#print ( " URL : %s" % current_url)

WebDriverWait(driver, 25).until(EC.title_contains("Shop"))


# This clicks on the HP marketsite link
sleep(3)
# NOTE: HP changed the sticker number once already.  Might need to choose better element.
driver.find_element_by_id("sticker-1459161").click()

# Allow the JS to fully load - this allows us to be able to click on the "order status" link
WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"""/html/frameset/frame[2]""")))
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, """/html/body/table[5]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[5]/td[2]/h3/a""")))

#driver.implicitly_wait(10)

driver.find_element_by_link_text("Order status").click()

# Clicking on order status link generates a new window so we must switch to it
driver.switch_to.window(driver.window_handles[1])

# Close the cookie disclosure popup
sleep(5)
driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div/button""").click()

# Clear the Search bar if there is an existing value
def clear_search():
    # Click the "Close" button on HP Order Status page to get back to search bar
    driver.find_element_by_xpath("""//*[@id="ossOrderModal"]/div/div/div[3]/div/div[2]/button""").click()
    blank = driver.find_element_by_id("compSearchId")
    blank.clear()
    
user_po_entry = False
def validate_po():
    if len(user_po_entry) == 10:
        return user_po_entry
    else:
        print("This does not appear to be a valid HP PO#.  Please try again.")

def po_search(user_po_entry):
    user_po_entry = input("Enter HP PO#: ")
    print(type(user_po_entry))
    validate_po()
    poNum = driver.find_element_by_id("compSearchId")
    
    poNum.send_keys(user_po_entry)
    driver.find_element_by_id("orderSearchButton").click()
    
    # Switch to the "Shipped Items" tab
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "itemsTab")))
    driver.find_element_by_xpath("""//*[@id="itemsTab"]/li[2]/a/span""").click()
    
    # Grab our order status data
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retreive order status time line
    order_timeline = []
    timestamps = soup.findAll("div", {"class": "timelineMiddle"})
    for timestamp in timestamps:
        order_timeline.append(timestamp)
    
    # Extract only the HTML date stamp from what soup returned
    date_stamp = []
    for time in order_timeline:
        new_time = str(time)
        split_time = new_time.replace('>', ',').replace('<', ',').split(',')
        date_stamp.append(split_time[2])
    
    # Extract item rows from Order Status page
    item_rows = soup.findAll("tr", {"class": "rowHover"})
    item_rows_lst2 = []
    for row in item_rows:
        item_rows_lst2.append(row)
    
    # This creates a list containing each row in a list 
    item_descriptions = []
    for item in item_rows_lst2:
        str_item = str(item)
        split_row = str_item.replace('>', ',').replace('<', ',').split(',')
        item_descriptions.append(split_row)
        
    # Print all desired values
    purchased = date_stamp[0]
    print("Order Purchased On: " + purchased)
    clean_order = date_stamp[1]
    print("Order Confirmed By HP On: " + clean_order)
    shipped = date_stamp[2]
    print("Order Shipped On: " + shipped)
    delivered = date_stamp[3]
    print("Order Delivered to Novastar On: " + delivered)
    print("\n")
    
    for item in range(0, len(item_descriptions)):
        item_status1 = item_descriptions[item][16]
        print("Item Status: " + item_status1)
        item_description1 = item_descriptions[item][20]
        print("Item Description: " + item_description1)
        order_quantity1 = item_descriptions[item][28]
        print("Order Quantity: " + order_quantity1)
#        if type(item_descriptions[item][28]) == int:
#            order_quantity1 = item_descriptions[item][28]
#            print("Order Quantity: " + order_quantity1)
#        elif type(item_descriptions[item][28]) == str:
#            cancelled_item = str(item_descriptions[item][28])
#            print("Order Quantity: " + cancelled_item)
        if item_status1 == 'Production':
            open_items1 = item_descriptions[item][32]
            print("Open Quantity: " + open_items1)
        else:
            shipped_quantity1 = item_descriptions[item][32]
            print("Shipped Quantity: " + shipped_quantity1)
        price1 = item_descriptions[item][36]
        print("Price: $" + price1)
        planned_delivery_date1 = item_descriptions[item][44]
        print("Planned Delivery Date to Novastar: " + planned_delivery_date1)
        print("\n")
    
    print("""**************************************************
          ****************************************************""")
    clear_search()
    po_search(user_po_entry)

po_search(user_po_entry)