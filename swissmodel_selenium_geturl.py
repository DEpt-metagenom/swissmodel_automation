import time
from Bio import SeqIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

project_queue=[]

options = Options()
profile_path = '/home/al9000/.config/google-chrome/Default'
options.add_argument(r"user-data-dir=" + profile_path)  
options.add_argument(r"profile-directory=Default")  # For the "Default" profile

driver = webdriver.Chrome(options=options)

inputfile="sequences_for_modelling.fa"

tabnum=0
with open('projects_urls.txt', 'a+') as file:
    for seq_record in SeqIO.parse(inputfile, "fasta"):
        # Start a new job
        driver.get("https://swissmodel.expasy.org/interactive")
        input_element = driver.find_element("xpath", "//textarea[@name='target']")
        input_element.send_keys([str(seq_record.seq)])
        time.sleep(0.5)
        driver.find_element("xpath", "//button[@id='validateInputButton']").click()
        time.sleep(0.3) 
        driver.find_element("xpath", "//button[@id='buildButton']").click()
        time.sleep(1)

        print(seq_record.id + "\n" + driver.current_url + "\n")
        file.write(seq_record.id + "\n" + driver.current_url + "\n")

time.sleep(600)
driver.quit()