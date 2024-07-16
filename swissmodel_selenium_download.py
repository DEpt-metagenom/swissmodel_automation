import time
from Bio import SeqIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import shutil
import os

inputfile="projects_urls.txt"   #<<<<<<<<<<<<<<<<<<<<-- input path here!!!!!!!!

options = Options()
profile_path = '/home/al9000/.config/google-chrome/Default'
options.add_argument(r"user-data-dir=" + profile_path)  
options.add_argument(r"profile-directory=Default")  # For the "Default" profile

driver = webdriver.Chrome(options=options)

#iterate tabs and download stuff
with open('projects_urls.txt', 'r') as file:
    while True:
        sequence_name = file.readline()
        sequence_url = file.readline()

        if( not sequence_name or 
           sequence_name == '\n' or 
           not sequence_url or 
           sequence_url == '\n'
           ):
            break

        if( os.path.exists(os.path.expanduser("~/Downloads/model_01.pdb")) or
           os.path.exists(os.path.expanduser("~/Downloads/model_02.pdb")) or
           os.path.exists(os.path.expanduser("~/Downloads/model_03.pdb"))
           ):
            print("Please delete previously downloaded project pdb files from your Downloads folder!")
            break

        os.makedirs("pdb_downloads", exist_ok=True)


        driver.get(sequence_url)

        while True:
            try:
                driver.find_element("xpath", "//a[contains(text(),'Templates')]").click()
                #print("try id sort...")
                idheader=driver.find_element("xpath", "//thead/tr[1]/th[@id='seq_idHeader']")
                driver.execute_script("arguments[0].class = 'headerSortDown';", idheader)
                #print("try select best...")
                driver.find_element("xpath", "/html/body/div[2]/div[3]/div/div/div/div[1]/div/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input").click()
                #print("try build best...")
                driver.find_element("xpath", "//button[@id='submitButton']").click()
                #print("generating best seqId model, we're getting there...")
            except:
                time.sleep(5)
                print("almost...")
                continue
            else:
                break

        while True:
            try:
                driver.find_element("xpath", "//a[contains(text(),'Models')]").click()
                Select(driver.find_element("xpath", "//select[@id='sortby']")).select_by_visible_text('Seq Identity')
                driver.find_element("xpath", "//button[contains(text(),'Download files')]").click()
                driver.find_element("xpath", "//ul[@class='dropdown-menu']/li[@title='Download coordinates in PDB format']/a").click()
                #print("That's a Bingo!")
                time.sleep(2)

            except:
                time.sleep(5)
                print("almost...")
                continue
            else:
                break

        if os.path.exists(os.path.expanduser("~/Downloads/model_01.pdb")):
            shutil.move(os.path.expanduser("~/Downloads/model_01.pdb"), f"./pdb_downloads/{sequence_name}.pdb")
        elif os.path.exists(os.path.expanduser("~/Downloads/model_02.pdb")):
            shutil.move(os.path.expanduser("~/Downloads/model_02.pdb"), f"./pdb_downloads/{sequence_name}.pdb")
        elif os.path.exists(os.path.expanduser("~/Downloads/model_03.pdb")):
            shutil.move(os.path.expanduser("~/Downloads/model_03.pdb"), f"./pdb_downloads/{sequence_name}.pdb")

print("Think we're done here...")
time.sleep(600)