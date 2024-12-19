import yfinance as yf
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets Authentication
SERVICE_ACCOUNT_FILE = 'E:/User/API Key for Stock Tracker/stock-tracker-445201-13dc73f76830.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Your Google Sheets ID and range
SPREADSHEET_ID = 'https://docs.google.com/spreadsheets/d/1H2sDWt3awqdyAQ72uztq9WV37juyx0zNAYcLGzey4VY'  # Replace with your actual Spreadsheet ID
SHEET_RANGE = 'Sheet1!A1'  # Update based on where you want to start writing data

# Fetch stock price using yfinance
stock_symbol = 'AAPL'  # Replace with the stock symbol you want to track
stock_data = yf.Ticker(stock_symbol)
current_price = stock_data.history(period='1d')['Close'][0]

# Get the current price from the previous sheet (if available) and calculate change
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE).execute()
previous_price = result.get('values', [])[0][0] if result.get('values') else 0
price_change = current_price - float(previous_price) if previous_price else 0

# Prepare the data to be written to the sheet
data = [
    ['Stock Symbol', 'Current Price', 'Price Change'],
    [stock_symbol, current_price, price_change]
]

# Write the data to Google Sheets
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE,
    valueInputOption="RAW", body={"values": data}
).execute()

print(f"Stock data for {stock_symbol} written to Google Sheets.")