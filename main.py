#C:\Program Files (x86)\chromedriver.exe
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys #gives access to keyboard keys like enter, escape, etc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from handlers import chrome_sel as cs
from handlers import files as fs
from handlers.chrome_sel import click_element
import config as cf

user = os.getenv('PSE_USER'),
password = os.getenv('PSE_PASS'),

mappings_2023 = {
    "primaHigh": {
        "new_student_reference": "32110", # THIS IS IN A CLOSED STATE
        "account_id":"select-customer-radio-Primavera Online Middle/High School",
        "zendesk_Group":"Primavera MS/HS",
        "distro":"Primavera MS/HS Distribution"
    },
    "glla" : {
        "new_student_reference": "32264",
        "account_id":"select-customer-radio-Great Lakes Learning Academy",
        "zendesk_Group":"GLLA","distro":"GLLA Distribution"
    },
    "isucceed" : {
        "new_student_reference": "32103",
        "account_id":"select-customer-radio-iSucceed Virtual High School",
        "zendesk_Group":"iSucceed",
        "distro":"iSucceed Distribution"
    },

    "bridge" : {
        "new_student_reference": "32442",
        "account_id":"select-customer-radio-The Bridge School American Virtual Academy",
        "zendesk_Group":"Bridge School",
        "distro":"Bridge School Distribution"
    },
    "valorOH": {
        "new_student_reference": "32111",
        "account_id":"select-customer-radio-Valor Academy, Inc.",
        "zendesk_Group":"Valor OH",
        "distro":"Valor OH Distribution"
    },
    "valorAZ": {
        "new_student_reference": "32084",
        "account_id":"select-customer-radio-Valor Preparatory Academy of Arizona",
        "zendesk_Group":"Valor AZ",
        "distro":"Valor AZ Distribution"
    }
}

#note pse selenium not yet called since it's not finished, starting with files already downloaded

def pse_login():
    #this'll install everytime it's run???
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://registration.powerschool.com/admin/login/login.rails")

    #use ID first if avail, then name, then class in that priority order.  it'll return first element with that id/name/class so id is likely most unique

    email = driver.find_element("id","email")
    ps = driver.find_element("id","password")
    signin = driver.find_element(By.CLASS_NAME, "btn--act")

    email.send_keys(user)
    ps.send_keys(password)
    signin.send_keys(Keys.RETURN)

    el = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID,"switch-customer-button"))

    #start process of exporting files from PSE
    export_pse_files(driver)

def main_school_loop(driver,current_school_mapping,current_school):
    #switch account using account picker
    cs.set_account(driver, current_school_mapping["account_id"])

    #need to process selenium steps here to navigate menus

def export_pse_files(driver):
    for current_school in mappings_2023.keys():
        current_school_mapping = mappings_2023[current_school]

        #function to handle menu navigation for each school
        main_school_loop(driver, current_school_mapping, current_school)


#after all files exported, begin processing

#grab all submitted files
submitted_files = fs.import_files("C:\\Users\mkunz6071\\Documents\\Marketing_Dashboard\\RawPSE\\submitted_*.csv")

submitted_headers = ["ExternalStudentID","FirstName","LastName","DateOfBirth","Contact1_ PhoneNumber","Contact 1 - Email","Contact 1 - First Name","Contact 1 - Last Name","Grade","Submitted","EnrollmentWorkflow","PostponeReason_Attempt","Started","Imported","Status","DeliveryDate","DeliveryTime","FamilyMemberID","FamilyID","SubmissionTime","Entry_Date","stu_FirstName","stu_PreferredName","stu_MiddleName","stu_LastName","stu_Suffix","stu_Gender","stu_PreferredGender","stu_DoB","stu_Email","stu_Phone","p_SigDate","filename"]
submitted_df = pd.DataFrame()

#create new df with only columns in header list above
for clmn in submitted_headers:
    submitted_df[clmn] = submitted_files[clmn].copy()

#fix column names
submitted_df.rename({'Contact1_ PhoneNumber':'contact1_phone','Contact 1 - Email':'contact1_email',
                     'Contact 1 - First Name':'contact1_firstname',
                     'Contact 1 - Last Name':'contact1_lastname'}, axis=1, inplace=True)

#change any datatypes necessary
submitted_df['Grade'] = submitted_df['Grade'].astype(str)

#set column names to upper to match snowflake
submitted_df.columns=submitted_df.columns.str.upper()

cf.write_to_snowflake_with_trunc(submitted_df,'strongmind','development','researchdb','marketing','PSE_SUBMITTED_EXPORT')



#grab all presubmitted files
presubmitted_files = fs.import_files("C:\\Users\mkunz6071\\Documents\\Marketing_Dashboard\\RawPSE\\presub_*.csv")

#fix column names
presubmitted_files.rename({'First Name':'firstname',
                  'Last Name':'lastname',
                  'Date of Birth':'dob',
                  'Date Started':'date_started',
                  'Date Last Accessed':'date_last_accessed',
                  'Current Page':'current_page'}, axis=1, inplace=True)

#change any datatypes necessary
#presubmitted_files['dob'] = pd.to_datetime(presubmitted_files['dob'])
#presubmitted_files['date_started'] = pd.to_datetime(presubmitted_files['date_started'])
#presubmitted_files['date_last_accessed'] = pd.to_datetime(presubmitted_files['date_last_accessed'])

#set column names to upper to match snowflake
presubmitted_files.columns=presubmitted_files.columns.str.upper()

cf.write_to_snowflake_with_trunc(presubmitted_files,'strongmind','development','researchdb','marketing','PSE_PRESUBMITTED_EXPORT')

