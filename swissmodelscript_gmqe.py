import shutil
import requests
import time
from Bio import SeqIO

#NOTE: this version of the sript uses the default swissmodel API options, downloading the 2 highet gmqe scored models pdb files

#NOTE: download only first model, file name as sequence name (from fasta)

#input file
inputfile="sequences_for_modelling_TEST.fa"
#Albert Bokor's swissmodel.expasy.org API token
user_token = "bae511865356f745e4c825d6d23c02afb7b1c924"
#for tracking the projects

project_queue = []
projects_failed = []
#seconds of delay between requests
delay = 3


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

