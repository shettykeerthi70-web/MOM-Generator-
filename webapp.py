
import google.generativeai as genai
import os
import streamlit as st


from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image

# configure the model 
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')

st.sidebar.title(':orange[upload your MoM NOTES HERE:]')
st.sidebar.subheader('only Image,pdfs,docx files are allowed to upload')
user_file = st.sidebar.file_uploader("Upload your file", type=['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ['image/png','image/jpg','image/jpeg']:
        user_text = extract_text_image(user_file)
    else:
        st.sidebar.write("Please upload a correct file type")

if user_file:
    st.write(user_text)

st.title(':blue[Minutes of Meeting]:[AI assisted MoM genertor in a standardised format for meeting notes]')
tips='''Tips to use this app:
* upload your meeting in side bar (Image , PDF or DOCX)
* click on generate MOM and get the standardised MoM's'''

st.write(tips)

if st.button('Generate MoM'):
    if user_text is None:
        st.error('Text is not generated')
    else: 
        with st.spinner('Processing your data...'):
            prompt='''Assume yoy are expert in creating minutes of meeting. user has provided notes of meeting , using this data yo need to create a standardised minutes of meeting for the user .the data provided by user is as follows
              {user_text}
              keep the format strictly as mentioned below
              title :Title of meeting 
              Heading : meeting Agenda 
              subheading: name of attendees (if attendees name is not there just keep it NA)
              subheading:date of meeting and place of meeting (place means name of conference / meeting room if not provided keep it online)
              Body: The body must following sequence of points
              * key point discussed
              * highlight any decission that has been fianlised
              * mention actionable items
              * any additional notes 
              * any deadline that has been discussed
              * any next meeting date that has been discussed
              * 2-3 line of summary
              * use bullet points and highlight or bold important keywords such that context is 
               
            The data provided by user is as follows {user_text}'''

            response=model.generate_content([prompt])
            output_text=response.text
            
            
            st.download_button(label = 'Click to download',
                               data = response.text,
                               file_name = 'MoM.txt',
                               mime='text/plain')

