import streamlit as st

st.write("# hello")
st.write("## hello")
st.write("### hello")
st.write("#### hello")
st.write("hello")
st.number_input('Pick a number',4,10)
st.date_input('your birthday')
st.time_input('meeting time')
st.file_uploader('Upload a CSV')
st.color_picker('Pick a color')
st.checkbox('check box')
st.camera_input('take a picture')
st.text_area('Text to translate')
st.select_slider('Pick a size', ['S', 'M', 'L'])
st.text_input('First name')
st.multiselect('Buy', ['milk', 'apples', 'potatoes'])
st.text('hello')
st.markdown('Markdown- this is some `code`') # see *
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write(['st', 'is <', 3]) # see *


