import gspread
from google.oauth2.service_account import Credentials
import pprint

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
    while True:
        print("please enter data from the last market")
        print("Data shoudl be six numbers, seperated by comas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("enter your data here:\n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all strings into integers
    Raises ValueError if strings cannot be converted into a int or if there \n
    in not enought values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"The expected result is 6 values, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid input data {e}, please try again.")
        return False

    return True


# def update_spreadsheet_data(data):
#     """
#     Updates data in workable sales sheet
#     """
#     print("Updating sales spreadsheet...")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Data has been updated")


# def update_surplus_data(data):
#     """
#     Updates data in workable surplus sheet
#     """
#     print("Updating surplus spreadsheet...")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus data has been updated")


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into worksheet.
    Update the relavant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully")


def calculate_surplus_data(sales_row):
    """
    Calculate the amount of food that has been sold. 
    
    Negative figure is extra food was made
    Possitive figure is too much food was made
    """
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entrties_sales():
    """
    Collect collumns of data sales worksheet, collecting the last 5 entries 
    for each sandwich and return the data as a list if lists
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculatin stock data...\n")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Runs all functions in the program
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, "surplus")
    sales_columns = get_last_5_entrties_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("welcome to Love Sandwiches Automation")
main()

