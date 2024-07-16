# swissmodel_automation

Due to the API being way too limited, this is a selenium UI solution that replicates the the manual workflow of the site through chrome on linux

How to use this:  
1.  on linux, install chrome webdriver (the dependency libraries called by the script if the package manager didn't get them)  
2.  copy your input .fa file in this directory, open `swissmode_selenium_geturl.py` and give the input path as the value of `inputfile` variable  
3.  run `swissmodel_selenium_geturl.py` to initialize the modelling job for you  
    this appends the project url-s in `project_urls.txt` in `<seq_name>\n<seq_url>\n` format  
4.  wait until the moddeling jobs finish, idk how long this should take, ex. it finished the 300 jobs i gave it in an hour or two  
5.    run `swissmodel_selenium_download.py` to start downloading the models  
    this checks for the best sequence identity matching template and generates it wasn't initially generated, then downloads it's pdb file and moves it to a `pdb_downloads` folder in the project forder, files named from the names in the fasta file  
6.  if this script gets stuck, a thing you could try is going back to previous page  
    if that doesn't work, manually download the project it's currently stuck on, then go to `project_urls.txt`, delete already downloaded projects and restart  
    