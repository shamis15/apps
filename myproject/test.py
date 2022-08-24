import streamlit as st

st.write("# hello")
st.write("## hello")
st.write("### hello")
st.write("#### hello")
st.write("hello")
st.title('My title')
st.header('header')
my_bar = st.progress(7)
st.error('Error message')
st.warning('Warning message')
st.info('Info message')
if st.button('Say hello', help='help here', 'disabled=true'):
     st.write('Why hello there')


col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
st.success('success message')


# Two equal columns: 
col1, col2 = st.columns(2)
col1.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
col2.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.This is column 2")
with st.echo():
  st.write('jess')
st.code('for i in range(8): foo()')
st.subheader('caption')
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

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
     st.image("https://static.streamlit.io/examples/dice.jpg")




