from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyautogui
import json
import os
import shutil
import re
import os




def rename_file(new_name_without_extension):
    
    # Folder where the file is located
    folder_path = "C:\\Users\\artur.sahakyan\\Desktop\\all_doc"
    
    
    # Step 1: Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # Step 2: Check if there is exactly one file in the folder
    if len(files) == 1:
        old_file_name = files[0]  # Get the first (and only) file name
        old_file_path = os.path.join(folder_path, old_file_name)
        
        # Step 3: Extract the file name and extension from the original file path
        file_name, file_extension = os.path.splitext(old_file_name)
        
        # Step 4: Create the new file path by combining the folder path, new name, and original extension
        new_file_path = os.path.join(folder_path, new_name_without_extension + file_extension)
        
        # Step 5: Rename the file
        try:
            os.rename(old_file_path, new_file_path)
            print(f"File renamed successfully to: {new_name_without_extension}{file_extension}")
        except FileNotFoundError:
            print(f"The file at {old_file_path} was not found.")
        except PermissionError:
            print(f"Permission denied. Unable to rename the file.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:

      

        print("There is not exactly one file in the folder.")
        print(files)




'''
def rename_file(file_name):
    

    # Specify the folder path and the current file name
    folder_path = download_dir  # Replace with your folder path
    
    files = os.listdir(folder_path)

    # Check if there is exactly one file in the folder
    if len(files) == 1:
        old_file_name = files[0]  # Get the first (and only) file name
        new_file_name = file_name  # Replace with the new desired file name
    
        # Create full paths for old and new file names
        old_file_path = os.path.join(folder_path, old_file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
    
        # Rename the file
        os.rename(old_file_path, new_file_path)
    
        print(f"File renamed from '{old_file_name}' to '{new_file_name}'")
    else:
        print("There is not exactly one file in the folder.")
'''


def sanitize_windows_filename(name):
    # Replace Windows-invalid characters with underscore
    return re.sub(r'[\\/*?:"<>|]', '_', name)


def move_files_to_new_folder(source_folder, new_folder_name):
    # Step 1: Create the new folder (if it doesn't already exist)
    new_folder = os.path.join(source_folder, new_folder_name)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print(f"Created new folder: {new_folder}")
    else:
        print(f"Folder already exists: {new_folder}")
    
    # Step 2: Move all files from the source folder to the new folder
    files = os.listdir(source_folder)  # List all files in the source folder
    
    for file in files:
        # Get the full path of the file
        file_path = os.path.join(source_folder, file)
        
        # Only move files, not directories
        if os.path.isfile(file_path):
            try:
                # Move the file to the new folder
                shutil.move(file_path, os.path.join(new_folder, file))
                print(f"Moved {file} to {new_folder}")
            except Exception as e:
                print(f"Error moving file {file}: {e}")



with open('grouped_data.json', 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# Use the data_list
#print(data_list)

installing_files = []
count = 50
download_dir = "C:\\Users\\artur.sahakyan\\Desktop\\all_doc"
new_folder_name_path = " "


def install_files(driver, file_name):
    global count, installing_files, new_folder_name_path
    
    try:
        button_scanMenu1 = driver.find_element(By.ID, "scanMenu1")
        print("Button with ID 'scanMenu1' found, returning early.")
        return  # If button exists, return early without doing anything else
    except:
        pass


    button = driver.find_element(By.ID, "scanMenu0")
    button.click()
    #time.sleep(1)
    #download_links = driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu li a")

    wait = WebDriverWait(driver, 10)
    download_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.dropdown-menu li a")))



    #and (link_text not in installing_files)

    for link in download_links:
        
        file_id = link.get_attribute("href").split('id=')[-1]
        
        link_text = link.text
        print("text is ")
        if (link_text.endswith('.pdf') or link_text.endswith('.PDF')) and (file_id not in installing_files): 
            print(f"Clicking on file: {link_text}") 
            link.click()
            time.sleep(2)
            installing_files.append(file_id)
            
            file_name = sanitize_windows_filename(file_name)
            if count > 0:
                file_name = file_name + f"_{count}"
                
            count = count + 1
            rename_file(file_name)
            move_files_to_new_folder(download_dir, new_folder_name_path)

            install_files(driver, file_name)

# Set up Chrome options to connect to the remote debugging port
chrome_options = Options()


chrome_prefs = {
    "download.default_directory": download_dir,  # Set the custom download directory
    "download.prompt_for_download": False,  # Prevent the download prompt
    "download.directory_upgrade": True,  # Allow Chrome to change the directory
    "safebrowsing.enabled": True  # Enable safe browsing (optional)
}
chrome_options.add_experimental_option("prefs", chrome_prefs)


chrome_options.add_argument("--remote-debugging-port=9222")  # Connect to Chrome on port 9222

# Optionally, you can disable the automation warning
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Connect to the running Chrome instance on port 9222
driver = webdriver.Chrome(options=chrome_options)

# Go to a website (if not already opened)
driver.get("https://armeps.am/ppcm/public/contracts")


button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "hide-filters"))
)
button.click()

search_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[ng-model='filter.number']"))
)



def get_contract(cont_id):
    global installing_files
    print(f"searching id is {cont_id}")
    search_box.send_keys(cont_id)

    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)


    install_files(driver, cont_id)
    installing_files.clear()
    time.sleep(1)
    search_box.clear()

# Iterate over each key-value pair in the JSON data

T = False

specific_code = "ՀՀ Ո ՄԱԾՁԲ-2023-ԱՎՎ/ԾԱՍ/Ա-16"

#while True
#    get_contract(specific_code)




with open("contact_id_with_downloaded_files.txt", "W", encoding='utf-8') as file:
    for organization, contract_codes in data_list.items():
        
        file.write(f"{organization}\n")
        print(f"Organization: {organization}")
        print("Contract Codes:")
    
        updated_folder_name = sanitize_windows_filename(organization)
        new_folder_name_path = f"C:\\Users\\artur.sahakyan\\Desktop\\specific_contract_doc\\{updated_folder_name}"



        # Iterate over the list of contract codes for the current organization
        for code in contract_codes:
            '''
            if code == "Ա4015929530":
                file.write(f"------------------------------------------------------------------------------------------\n")
                T = True
                continue

            if T == False:
                continue
            '''
            
            count = 0
            get_contract(code)
            file.write(f"   {code}  -----   {count}\n")

        print("-" * 30)  # Print a separator line between organizations

driver.refresh()

time.sleep(2)

# Close the browser
driver.quit()

# need to clean the search box then do other search