!pip install yfinance
!pip install bs4
!pip install nbformat
!pip install --upgrade plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))

# Create a ticker object for Tesla (TSLA)
tsla_ticker = yf.Ticker("TSLA")

# Extract stock information and save it in a dataframe
tesla_data = tsla_ticker.history(period="max")

# Reset the index of the dataframe
tesla_data.reset_index(inplace=True)

# Display the first five rows
tesla_data.head()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')

!pip install lxml

# Find all tables in the HTML data
tables = pd.read_html(str(soup))

# Extract the table at index 1, which contains Tesla's quarterly revenue data
tesla_revenue = tables[1]

# Rename columns to "Date" and "Revenue"
tesla_revenue.columns = ["Date", "Revenue"]

# Display the first few rows of the dataframe
tesla_revenue.head()

tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r',|\$', "", regex=True)
tesla_revenue.head()

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.head()
tesla_revenue.tail()

gme_ticker = yf.Ticker("GME")
gme_data = gme_ticker.history(period="max")

# Reset the index of the dataframe
gme_data.reset_index(inplace=True)

# Display the first five rows
gme_data.head()

url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

response = requests.get(url2)
html2_data = response.text
soup2 = BeautifulSoup(html2_data, 'html.parser')

# Find all tables in the HTML data
tables2 = pd.read_html(str(soup2))

# Extract the table at index 1, which contains Tesla's quarterly revenue data
gme_revenue = tables2[1]

# Rename columns to "Date" and "Revenue"
gme_revenue.columns = ["Date", "Revenue"]

gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(r',|\$', "", regex=True)
gme_revenue.head()

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail()
gme_revenue.head()

make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GME')