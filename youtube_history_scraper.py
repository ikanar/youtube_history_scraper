import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import tkinter as tk





#REQUIRES YOU TO USE YOUR PHONE TO AUTHENTICATE THE USER
#GOOGLE WILL SEND YOU AN ALERT AND YOU HAVE 10 SECONDS TO CLICK YES OR THE PROGRAM WILL FAIL
#PROGRAM ALSO WILL THROW ERROR AT THE END THIS IS A KNOWN BUG WITH UNDETECTED CHROME DRIVER AND IT IS WORKING AS INTENDED FOR NOW.


def scrape_history(username,password,scan_length,file_name):
    driver = uc.Chrome()
    driver.get('https://accounts.google.com/')
    scan_length_int = int(scan_length)

    

    #handles login to google account
    #sleeps inbetween each stage to allow time to load
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    sleep(7)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    sleep(10)
    driver.get('https://www.youtube.com/feed/history')

    #scans and collects the html elements
    
    while scan_length_int > 0:
        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        sleep(5)
        scan_length_int = scan_length_int - 1
    
    elements = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')

    links = []

    #loads links from html elements into a list 
    #filters out the "None" elements
    for element in elements:
        e = element.get_attribute("href")
        if e != None:
            links.append(e)
        

    #prints out links to a file
    file = open(file_name + ".txt","w")
    for link in links[:-1]:
        file.write(link+"\n")
    file.write(links[-1])
    file.close()    
    

    driver.close()

    return links


def Search():
    #gathers the data from the UI and then uses it to call scrape_history
    email = email_entry.get()
    password = password_entry.get()
    scan_length = scan_length_entry.get()
    file_name = file_name_entry.get()
    scrape_history(email,password,scan_length,file_name)



if __name__ == '__main__':
    #UI initialization 

    root = tk.Tk()

    root.geometry("400x150")

    root.title("Youtube History Scraper")

    email_label = tk.Label(root,text= "Enter Email")
    email_entry= tk.Entry(root,font=('calibre',10,'normal'))

    password_label = tk.Label(root,text= "Enter Password")
    password_entry = tk.Entry(root,font=('calibre',10,"normal"),show='*')

    scan_length_label = tk.Label(root,text="Enter Integer scan length")
    scan_length_entry = tk.Entry(root,font=('calibre',10,"normal"))
    
    file_name_label = tk.Label(root,text="Enter name of save File")
    file_name_entry = tk.Entry(root,font=('calibre',10,"normal"))

    quit_button = tk.Button(root, text='Quit', command=root.destroy)
    search_button = tk.Button(root,text = "Search", command = Search )
    


    email_label.grid(row=0,column=0)
    email_entry.grid(row=0,column=1)

    password_label.grid(row=1,column=0)
    password_entry.grid(row=1,column=1)

    scan_length_label.grid(row=2,column=0)
    scan_length_entry.grid(row=2,column=1)
    
    file_name_label.grid(row=3,column=0)
    file_name_entry.grid(row=3,column=1)
    
    quit_button.grid(row=4,column =0)
    search_button.grid(row=4,column=1)
    
    
    root.mainloop()
