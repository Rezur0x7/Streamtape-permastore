import requests,time,argparse
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#https://api.streamtape.to/file/listfolder?login=<apiid>&key=<apipass>

failure = False

def list_folders():
    time.sleep(0.1)
    params = {
        "login" : username,
        "key" : password
    }
    response = requests.get("https://api.streamtape.to/file/listfolder", params=params, verify=False)
    resp_json = response.json()
    length = len(resp_json['result']['folders'])-1
    blacklist = ['Remote','Subtitles','Thumbnails']
    folder_id = []
    name = []
    for i in range(length):
        if resp_json['result']['folders'][i]['name'] not in blacklist:
            folder_id.append(resp_json['result']['folders'][i]['id'])
    return(folder_id)

def list_files_in_folder(folderid):
    time.sleep(0.1)
    params = {  
        "login" : username,
        "key" : password,
        "folder" : folderid
    }
    response = requests.get("https://api.streamtape.to/file/listfolder", params=params, verify=False)
    resp_json = response.json()
    length = len(resp_json['result']['files'])
    links = []
    file_id = []
    for i in range(length):
        links.append(resp_json['result']['files'][i]['link'])
        file_id.append(resp_json['result']['files'][i]['linkid'])
    return(links,file_id)

def delete_file(fileid):
    time.sleep(0.1)
    global failure
    params = {  
        "login" : username,
        "key" : password,
        "file" : fileid
    }
    response = requests.get("https://api.streamtape.to/file/delete", params=params, verify=False)
    if str(response.status_code) != "200":
        failure = True
    
def remote_upload(remoteurl,folderid):
    time.sleep(0.1)
    global failure
    params = {  
        "login" : username,
        "key" : password,
        "url" : remoteurl,
        "folder" : folderid
    }
    response = requests.get("https://api.streamtape.to/remotedl/add", params=params, verify=False)
    if str(response.status_code) != "200":
        failure = True

def main():
    for folder in list_folders():
    #for folder in list_folders()[11:]:     #specify index of folder from which upload continues in case of failure
        file_url_list, file_id_list = list_files_in_folder(folder)
        for file_url in file_url_list:
            print("Uploading: ",file_url)
            remote_upload(file_url,folder)
            if failure:
                print(file_url)
                break
        for file_id in file_id_list:
            print("Deleting: ",file_id)
            delete_file(file_id)
            if failure:
                print(file_id)
                break

            
def argsetup():
    about  = 'Allows storage of videos permanently instead of the default 60 days inactivity period by using "remote-upload" functionality to re-upload videos iteratively in the same directory'
    parser = argparse.ArgumentParser(description=about)
    parser.add_argument('-u', '--username', help='Streamtape API Username', required=True)
    parser.add_argument('-p', '--password', help='Streamtape API Password', required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args   = argsetup()
    username = args.username
    password = args.password
    main()