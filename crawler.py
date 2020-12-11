from bs4 import BeautifulSoup
import requests
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


## Prepare for Firebase 
# 引用私密金鑰
cred = credentials.Certificate('/Users/mikey/Documents/Programming/Python/Projects/Lottery Reader/lottery-reader-bb401-firebase-adminsdk-rsxkw-162643f584.json')
# 初始化firebase
firebase_admin.initialize_app(cred)
# 初始化firestore
db = firestore.client()

def fetch_src():
    ## Retrieve prize number from website
    src_url = "https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx"
    res = requests.get(src_url, timeout=30)
    # print(res.text)

    # Patterns of the html that contains prize number info
    # primary_tags = ["Lotto649Control_history_dlQuery_No1_", "Lotto649Control_history_dlQuery_No2_","Lotto649Control_history_dlQuery_No3_" ,"Lotto649Control_history_dlQuery_No4_", "Lotto649Control_history_dlQuery_No5_", "Lotto649Control_history_dlQuery_No6_", "Lotto649Control_history_dlQuery_SNo_"]

    soup = BeautifulSoup(res.text, "lxml")
    headers = soup.find_all(id = [re.compile(r"Lotto649Control_history_dlQuery_No\d"), re.compile("Lotto649Control_history_dlQuery_L649_DDate_")])

    # Clean up and extract the actual prize number with .text
    # Stored with dictionary {"date": [ , , , , , , ]}
    # A set will contain a date & 7 numbers, the first number is the special prize
    prize_dict = {}
    current_key = ""
    for item in headers:
        if("/" in item.text):
            current_key = item.text
            prize_dict[current_key] = []
        else:
            prize_dict[current_key].append(item.text)
    return prize_dict


def db_write(prize_dict):
    prize_doc = {"Prize_0": "","Prize_1": "", "Prize_2": "", "Prize_3": "", "Prize_4": "", "Prize_5":"", "Prize_6":"" }
    for key in prize_dict:
        format_key = str(key)
        formate_key_1 = format_key.replace("/", "-")
        print(formate_key_1)
        prize_dict_ref = db.collection("prize_numbers").document(formate_key_1)
        for index, value in enumerate(prize_dict[key]):
            prize_doc["Prize_"+str(index)] = value
        prize_dict_ref.set(prize_doc)

## Take in usr input and perform check by retrieving data from firestore
def check_prize(usr_input):
    

if __name__ == "__main__":
    db_write(fetch_src())