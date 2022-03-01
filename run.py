
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures from the user
    """
    print("please enter data from the last market")
    print("Data shoudl be six numbers, seperated by comas")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("enter your data here: ")

    sales_data = data_str.split(",")
    validate_data(sales_data)
    

def validate_data(values):
    """
    Inside the try, converts all strings into integers
    Raises ValueError if strings cannot be converted into a int 
    or if there in not enought values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"The expected result is 6 values, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid input data {e}, please try again.")
        
    
    
get_sales_data()