import streamlit as st
import pandas as pd
import base64
import os
import warnings
from dotenv import load_dotenv
from back_func import querry_req, run_request, format_question, format_response, get_primer, pdf_req

warnings.filterwarnings("ignore")

load_dotenv()

st.markdown("<h1 style='text-align: center; padding-top: 0rem; font-weight: bold; font-family:helvetica'> Data Assist Tool</h1>",
            unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Creating Visualisations using Natural Language with ChatGPT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Choose any type of document from your device and perfom data inspection or visualization!</p>", unsafe_allow_html=True)

st.primaryColor="purple"
temp_filepath = ""
file_extension = ""
filepath_ = ""
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-size:large; color:white; padding-top: 0rem;padding-bottom: 2rem;'> Welcome to Data Assist tool! </h4>",
                unsafe_allow_html=True)
    file = st.file_uploader("Upload the file here")

    filepath_ = ""
    df = None
    querry_type = ""
    file_type = ""
    flag = None
    if file is not None:
        _ , file_extension = os.path.splitext(file.name)
        file_extension = file_extension.lower()
        # Use the file extension to determine the file type
        temp_filepath = r"C:\Users\Night\OneDrive\Documents\langchain_try\temp" + file_extension
        filepath_ = temp_filepath
        flag = 0
        if file_extension == ".csv":
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())

            df = pd.read_csv(filepath_)
            flag = 1
            querry_type = st.radio(
                "What would you like to do with your csv file?",
                ["General querry", "Graph visualisation"]
            )
if file_extension == ".pdf":
    g_querry = st.text_input("General querry prompt:")
    with open(temp_filepath, "rb") as f:
        bytes_data = file.getvalue()

    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str("100%")} height={str(int(100*17/3))} type="application/pdf"></iframe>'  
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
    pdf_req(file, g_querry)

if querry_type == "General querry":
    # if df is not None:
   g_querry = st.text_input("General querry prompt:")
   if flag == 1:
       st.write(df)
       querry_req(g_querry, filepath=filepath_)
elif querry_type == "Graph visualisation":
    #     # if df is not None:
    vis_querry = st.text_area("Ghraphical Visualization prompt:", height=10)
    if flag == 1:
        st.write(df)
    # Format the question 
        primer1,primer2 = get_primer(df) 
        question_to_ask = format_question(primer1, primer2, vis_querry, )   
    # Run the question
        answer=""
        answer = run_request(question_to_ask)
    # the answer is the completed Python script so add to the beginning of the script to it.
        answer = primer2 + answer
        # print("Model: ")
        print(answer)
        plot_area = st.empty()
        plot_area.pyplot(exec(answer))

