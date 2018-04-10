# Required for sending a GET request for update checks
from multiprocessing import Process, Manager, freeze_support
import requests
import os

# Required for downloading a new version automatically
from tqdmLite import tqdm
import zipfile
# import traceback
import subprocess

from py2exeUtils import scriptDir as SCRIPT_PATH
import py2exeUtils as p2eU


ZIP_DOWNLOAD_PATH = SCRIPT_PATH+'.updateSnL/'
req_error = requests.exceptions

# =============================================================================
# FUNCTIONS THAT USE GITHUB API TO RETRIEVE NEWEST RELEASE
# =============================================================================


def f(d):
    try:
        d['value'] = d['a']('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest',
                            verify=d['b']+'cacert.pem')
    except KeyboardInterrupt:
        pass


def getNewestVersionEx():
    """
    Sends a GET request to GitHub to retrieve the latest release.
    
    Returns a dict containing the the json-encoded content of the response.
    """
    if __name__ == '__main__':
        freeze_support()
    manager = Manager()

    # Create manager dict to send data to our child process
    d = manager.dict()
    d['a'] = requests.get
    d['b'] = SCRIPT_PATH
    
    p = Process(target=f, args=(d, ))
    p.start()
    i = 0
    while p.is_alive() and i < 334:  # 0.03 * 334 ~= 10 seconds
        p.join(0.03)  # Allow user to press ctrl+C
        i += 1
    
    if p.is_alive():
        p.terminate()
        raise req_error.ConnectionError('Connection did not complete within timeout.')

    check = d['value'].json() 
    return check


def getNewestVersion():
    """
    Sends a request to GitHub to retrieve the latest release.
    
    Returns a string containing the tag_name of the latest release.
    
    Eg: v2.2
    
    Uses getNewVersionEx()
    """
    a = getNewestVersionEx()
    return a['tag_name'] if a else ''


# =============================================================================
# FILE IO AND AUTOUPDATE
# =============================================================================
def makeDirSafe(*args, **kargs):
    """
    Make a directory. Does not raise an error if the directory already exists.
    """
    try:
        os.mkdir(*args, **kargs)
    except WindowsError as error:
        if error.winerror == 183:
            pass  # Windows error: cannot create an existing file
        else:
            raise error
    

def extractUpdate(zip_path, destination_folder, delete=False):
    """
    Extracts the contents of a .zip file into a given destination_folder.
    
    Uses makeDirSafe to ensure the folder exists.
    
    If they keyword argument delete is set to true, the zip file is deleted
    after its contents have been fully extracted.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_:
        makeDirSafe(destination_folder)
        zip_.extractall(destination_folder)
    if delete:
        os.remove(zip_path)


def downloadNewestVersion(download_folder, zip_name='Update.zip'):
    """
    Uses getNewestVersionEx() to get a download link to the latest release.
    
    Downloads the latest release while displaying a progress bar.
    
    Returns the path to the created zip file.
    """
    # Get download link
    release_dict  = getNewestVersionEx()
    download_link = release_dict['assets'][0]['browser_download_url']
    
    makeDirSafe(download_folder)
    
    # Make GET request to download link, determine file size and .zip file path
    response  = requests.get(download_link, verify=SCRIPT_PATH+'cacert.pem', stream=True)
    file_size = int(response.headers['Content-Length'])
    zip_path  = download_folder + zip_name
    
    # Download file as a stream, use tqdm to create a progress bar
    with open(zip_path, "wb") as handle:
        for data in tqdm(response.iter_content(chunk_size=1024*500),
                         unit='kb', unit_scale=500, total=file_size/1024./500.):
            handle.write(data)
            
    return zip_path


def autoUpdate():
    DETACHED_PROCESS = 0x00000008
    if not p2eU.frozen:
        print 'Auto Update is only supported when using the compiled executable.'
        return False
    
    zip_path = downloadNewestVersion(ZIP_DOWNLOAD_PATH)
    extractUpdate(zip_path, ZIP_DOWNLOAD_PATH, delete=True)
    
    subprocess.Popen([SCRIPT_PATH+'.updateSnL/SaveNLoad/autoupdate.exe', 'copyFiles', SCRIPT_PATH],
                     stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                     creationflags=DETACHED_PROCESS)
    
    exit()
