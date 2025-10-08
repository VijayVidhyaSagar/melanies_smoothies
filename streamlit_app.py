# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
# st.title("My Parents New Healthy Dinner")
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# st.dataframe(data=my_dataframe, use_container_width=True)
nameos = st.text_input(
    'Name on Smoothie:'
)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5)

# if ingredients_list:
#     st.write(ingredients_list)
#     st.text(ingredients_list)
if ingredients_list:
    ingredients_string = ''
    for f_c in ingredients_list:
        ingredients_string += f_c + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

# st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + nameos + """')"""

# st.write(my_insert_stmt)
# st.stop()
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {nameos}!', icon="✅")


# New section to display smoothiefroot info
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
