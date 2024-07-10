import time
from Bio import SeqIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

initialized_tabs=[]
maxtab=5                #<<<<<<<<<<<<<<<<<<<<<<<<<<<for current testfile

options = Options()
profile_path = '/home/al9000/.config/google-chrome/Default'
options.add_argument(r"user-data-dir=" + profile_path)  
options.add_argument(r"profile-directory=Default")  # For the "Default" profile

driver = webdriver.Chrome(options=options)
"""
inputfile="sequences_for_modelling_TEST.fa"
user_token = "bae511865356f745e4c825d6d23c02afb7b1c924" #Albert Bokor's swissmodel.expasy.org API token

tabnum=0
for seq_record in SeqIO.parse(inputfile, "fasta"):

    # Start a new job
    driver.get("https://swissmodel.expasy.org/interactive")
    input_element = driver.find_element("xpath", "//textarea[@name='target']")
    input_element.send_keys([str(seq_record.seq)])
    time.sleep(0.5)
    driver.find_element("xpath", "//button[@id='validateInputButton']").click()
    time.sleep(0.3) 
    driver.find_element("xpath", "//button[@id='buildButton']").click()

    initialized_tabs.append(driver.current_url)
    tabnum+=1
    if tabnum>=maxtab:           
        break

    driver.execute_script("window.open('https://swissmodel.expasy.org/interactive');")
    driver.switch_to.window(driver.window_handles[tabnum])


#wait a bit til models generate
time.sleep(120)
"""

driver.get("https://swissmodel.expasy.org/interactive/hs9nQz/templates/")
i=0
#iterate tabs and download stuff
while i<maxtab:
    #generate best seqid model
    driver.switch_to.window(driver.window_handles[i])


    driver.find_element("xpath", "//a[contains(text(),'Templates')]").click()
    time.sleep(0.3)
    print("try id sort...")
    idheader=driver.find_element("xpath", "//thead/tr[1]/th[@id='seq_idHeader']")
    driver.execute_script("arguments[0].class = 'headerSortDown';", idheader)
    print("try select best...")
    driver.find_element("xpath", "//tbody/tr[1]/td[1]/input']").click()
    print("try build best...")
    driver.find_element("xpath", "//button[@id='submitButton']").click()
    print("generating best seqId model, we're getting there...")

    """
    while True:
        try:
            driver.find_element("xpath", "//a[contains(text(),'Templates')]").click()
            time.sleep(0.3)
            print("try id sort...")
            idheader=driver.find_element("xpath", "//thead/tr[1]/th[@id='seq_idHeader']")
            driver.execute_script("arguments[0].class = 'headerSortDown';", idheader)
            print("try select best...")
            driver.find_element("xpath", "//tbody/tr[1]/td/input']").click()
            print("try build best...")
            driver.find_element("xpath", "//button[@id='submitButton']").click()
            print("generating best seqId model, we're getting there...")
        except:
            time.sleep(5)
            print("almost...")
            continue
        else:
            break
"""
    #wait til new model generates
    while True:
        try:
            Select(driver.find_element("xpath", "//select[@id='sortby']")).select_by_visible_text('Seq Identity')
            driver.find_element("xpath", "//button[contains(text(),'Download files')]").click()
            driver.find_element("xpath", "//ul[@class='dropdown-menu']/li[@title='Download coordinates in PDB format']/a").click()
            print("That's a Bingo!")
            time.sleep(1)
        except:
            time.sleep(5)
            print("almost...")
            continue
        else:
            break
    i+=1

print(initialized_tabs)

time.sleep(600)

"""

    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={ "Authorization": f"Token {user_token}" },
        json={ "target_sequences":[str(seq_record.seq)],
            "project_title":f"automation_test{seq_record.id}",
        })
    
    project_id = response.json()["project_id"]
    print(f"Start Automodel project {project_id}: ",response)

# Function to download the next project in the queue
def try_download_next_project():
    time.sleep(delay)

    project_id=project_queue[0][0]
    sequence_id=project_queue[0][1]

    response = requests.get(
        f"https://swissmodel.expasy.org/project/{ project_id }/models/summary/", 
        headers={ "Authorization": f"Token {user_token}" })    

    status = response.json()["status"]

    response_object = response.json()
    if status =="COMPLETED":
        project_queue.pop(0)
        i=1
        model =(response_object['models'])[0]           #TODO: download firt model, name after sequence name
        print(model['coordinates_url'])                                                     
        with requests.get(model['coordinates_url'], stream=True) as r:                      
            with open("./"+sequence_id+"_"+project_id+".pdb.gz", mode="wb") as file:
                shutil.copyfileobj(r.raw, file)
        i+=1
        
        project_id = response.json()["project_id"]
        print(f"Downloaded project {project_id}'s pdb files")

    if status =="FAILED":
        projects_failed.append(project_queue.pop(0))


# Read the sequences from a fasta file and initiate a modelling job for each sequence

for seq_record in SeqIO.parse(inputfile, "fasta"):
    # Start a new job
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={ "Authorization": f"Token {user_token}" },
        json={ "target_sequences":[str(seq_record.seq)],
            "project_title":f"automation_test{seq_record.id}",
        })
    
    project_id = response.json()["project_id"]
    print(f"Start Automodel project {project_id}: ",response)
    project_queue.append((project_id,seq_record.id))                                #TODO: switch to seqname+project_id tuple 

    try_download_next_project()

while len(project_queue) > 0:
    try_download_next_project()

print("\n\nFailed projects:", projects_failed)

"""
