import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import tkinter as tk



#REQUIRES YOU TO USE YOUR PHONE TO AUTHENTICATE THE USER
#GOOGLE WILL SEND YOU AN ALERT AND YOU HAVE 30 SECONDS TO CLICK YES OR THE PROGRAM WILL FAIL
#PROGRAM ALSO WILL THROW ERROR AT THE END THIS IS A KNOWN BUG WITH UNDETECTED CHROME DRIVER AND IT IS WORKING AS INTENDED FOR NOW.


def scrape_history(username,password,scan_length):
    driver = uc.Chrome()
    driver.get('https://accounts.google.com/')

    #handles login to google account
    #sleeps inbetween each stage to allow time to load
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    sleep(7)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    sleep(7)
    driver.get('https://www.youtube.com/feed/history')

    #scans and collects html elements
    while scan_length > 0:
        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        sleep(5)
        scan_length = scan_length - 1
    
    elements = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')

    links = []

    #loads links from html elements into a list 
    #filters out the "None" elements
    for element in elements:
        e = element.get_attribute("href")
        if e != None:
            links.append(e)
        

    #prints out links
    file = open("youtube_history.txt","w")
    for link in links:
        print(link)
        file.write(link+"\n")
    file.close()    
    

    driver.close()

    return links


def Search():
    email = email_entry.get()
    password = password_entry.get()
    scrape_history(email,password,2)



if __name__ == '__main__':
    #gets username and password from user
    #username = input("Enter google Username:")
    #password = input("Enter password:")


    UI = tk.Tk()

    UI.geometry("600x400")

    email_label = tk.Label(UI,text= "Enter Email")

    email_entry= tk.Entry(UI,font=('calibre',10,'normal'))

    password_label = tk.Label(UI,text= "Enter Password")

    password_entry = tk.Entry(UI,font=('calibre',10,"normal"),show='*')

    
    button = tk.Button(UI,text = "Search", command = Search )

    
    email_label.grid(row=0,column=0)
    email_entry.grid(row=0,column=1)
    password_label.grid(row=1,column=0)
    password_entry.grid(row=1,column=1)
    button.grid(row=2,column=1)
    
    
    
    
    UI.mainloop()





    



    history = scrape_history(username,password,2)