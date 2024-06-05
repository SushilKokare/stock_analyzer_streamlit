import streamlit as st
import yfinance as yf
import niftystocks as ns
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import candlemarubozu as cm
import matplotlib.pyplot as plt


def get_data(symbol,start=None,end=None,period='max'):
	df = pd.DataFrame()
	if start:
		df = yf.download(symbol,start=str(start) , end=str(end),progress=False)
		st.write(str(len(df))+' Rows')
	else:
	    	df = yf.download(symbol,period=period,progress=False)
	    	st.write(str(len(df))+' Rows')
	return df

# Finding dates on which marubozu is formed
def show_marubozu_dates(df):
	st.markdown('### Marubozu Found of following dates : \n')
	for i in df.index:
	    if(df['Open'][i]<df['Close'][i]):
	    	head = df['High'][i] - df['Close'][i]
	    	tail = df['Open'][i] - df['Low'][i]
	    	body = df['Close'][i] - df['Open'][i]
	    	if( (head < ((body/100)*20) ) and (tail < ((body/100)*20))):
	    		# i = str(i).split('-')
	    		# st.write(int(i[0]),'-',int(i[1]),'-',int(i[2]))
	    		st.write(i)

	

st.title('Stock Analyzer ')

sym = st.text_input('Enter stock name : ')


st.info('Either select range of date Or Just enter the period',icon=":material/info:")
choice = st.selectbox('Choose any one',['Date Range','Period'],help='choose how you want to download the data !')

if choice=="Period":

	# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
	col1,col2 = st.columns(2)
	with col1:
		num = st.number_input('Enter number',min_value=1)
		
	with col2:
		ymw = st.selectbox('Select any one',['Year','Month','Week'])


option_to_key = {
	'Year' : 'y',
	'Month' : 'mo',
	'Week' : 'wk' }	


if choice=="Date Range":
	col1,col2 = st.columns(2)

	with col1:
		start_date = st.date_input('Select start date')
		
	with col2:
		end_date = st.date_input('Select end date')



	
st.selectbox(label='Select Candle ',options=['Bullish Marubozu'])


chkbtn = st.button('Check')

marubozu_list = list()
successs_list = list()

if chkbtn:
	df = pd.DataFrame()
	if choice=='Date Range':
		if start_date>end_date:
			st.error('Start date cannot be greater then End date')	
		else:
			df = get_data(sym+'.ns',start=start_date,end=end_date)	
	elif choice=='Period':
		period = str(num)+option_to_key.get(ymw)
		# st.write(period)
		df = get_data(sym+'.ns',period=period)

	df2 = df.copy()
	df2.index = pd.to_datetime(df.index)
	df2.index = df.index.strftime('%Y-%m-%d')

	st.write(df2)	

	#show_marubozu_dates(df)
	#st.header('xxxxxxxxxxxxxxx')
	marubozu_list, successs_list = cm.marubozu(df,sym)
	#st.header('xxxxxxxxxxxxxxx')


if marubozu_list:
	st.header('Check Report')
	with st.expander('click to see marubozu dates '):
		st.write([x.strftime('%Y-%m-%d') for x in marubozu_list])

	with st.expander('click to see success dates '):
		st.write([x.strftime('%Y-%m-%d') for x in successs_list])




	success_percentage = (len(successs_list) / len(marubozu_list))*100


	rate = pd.DataFrame({ 'Category' : ['success rate','failure rate'],
	'Percentage' : [success_percentage,100-success_percentage]})
    
	# Plot the pie chart using matplotlib
	# fig, ax = plt.subplots()
	# ax.pie(rate['Percentage'], labels=rate['Category'], autopct='%1.1f%%', startangle=90)
	# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	# # Display the pie chart in Streamlit
	# st.write("Pie Chart:")
	# st.pyplot(fig)

	system_bg_color = '#ffffff'

	# Create a smaller pie chart with adjusted background color
	fig, ax = plt.subplots(figsize=(1.5,1.5) ) # Adjust the figsize for smaller chart
	ax.pie(rate['Percentage'], labels=rate['Category'], autopct='%1.1f%%', startangle=90,   textprops=dict(color="black"),  # Default text color
    colors=['green', 'red'] )
	ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	# Set the background color
	fig.patch.set_facecolor(system_bg_color)
	ax.set_facecolor(system_bg_color)

	# Display the pie chart in Streamlit
	st.write("Pie Chart:")
	st.pyplot(fig)

for i in range(5):
	st.write("")
	
	
def myname():
  footer_text = f""" 
  Developed by Sushil Kokare    
  © 2024 
  """
  st.markdown(footer_text, unsafe_allow_html=True)




myname()  




