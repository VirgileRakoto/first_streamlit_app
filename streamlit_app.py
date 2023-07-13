import streamlit 
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(This_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return  fruityvice_normalized

 

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

#Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruit_selected]


streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get infos")
 else:
  streamlit.write('The user entered ', fruit_choice)
  back_from_function=get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
except URLError as e:
 streamlit.error()
  
 

def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("USE ROLE ACCOUNTADMIN ;")
  my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST ;")
  return my_cur.fetchall()

if streamlit.button('Get fruit load list'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows=  get_fruit_load_list()
 streamlit.text("The fruit load list contains:")
 streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("USE ROLE ACCOUNTADMIN ;")
  my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES('{fruit_choice}')")

add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('add a fruit'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 get_fruit_load_list(add_my_fruit)
 streamlit.write('Thanks for adding ', fruit_choice)

 





 
