import streamlit as st

st.write("# hello")
st.write("## hello!")
st.write("### hello")
st.write("#### hello!!")
st.write("hello")
st.title('My title')
st.header('header')
my_bar = st.progress(7)
st.error('Error message')
st.warning('Warning message')
st.info('Info message')
if st.button('Say hello', help='help here', disabled=True):
     st.write('Why hello there')


col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
st.success('success message')

st.text_input(
      'Caption goes here',
      
      
      placeholder='Placeholder goes here', 
    )
st.checkbox('this is a test',disabled=True)

# Two equal columns: 
col1, col2 = st.columns(2)
col1.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
col2.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.This is column 2")
with st.echo():
  st.write('jess')
st.code('for i in range(8): foo()')
st.text_input('hello', help='this is a help warning')
st.subheader('caption')
st.number_input('Pick a number',4,10)
st.date_input('your birthday')
st.time_input('meeting time')
st.file_uploader('Upload a CSV')
st.color_picker('Pick a color')
st.checkbox('check box')
st.camera_input('take a picture',help='smile for the camera')
st.text_area('Text to translate')
st.select_slider('Pick a size', ['S', 'M', 'L'])
st.text_input('First name')
st.multiselect('Buy', ['milk', 'apples', 'potatoes'], disabled=True)
st.text('Oh boy — were officially back\n'
        'Today is the day we can hack\n' 
        'I’m pumped, how ‘bout you For hackathon ’22\n' 
        'Now lets get working before we have a snack')
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
     
age = st.slider('How old are you?', 0, 130, 25, disabled=True)
st.write("I'm ", age, 'years old')


st.text_input(
  'Caption goes here, or does it...',
  placeholder='Placeholder goes here',
  help='Help message goes here'
)



