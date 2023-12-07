from dotenv import load_dotenv
import openai
from langchain.llms.openai import OpenAI
# from langchain.document_loaders.csv_loader import CSVLoader
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

import os

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
def querry_req(text, filepath):
    if filepath and os.path.exists(filepath):  # Check if filepath is not empty and exists
        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, filepath, verbose=True)
        stri_ng = agent.run(text)
        st.write(stri_ng)
    else:
        if not filepath and os.path.exists(filepath):
            st.write("Invalid file path or file does not exist:", filepath)

# for visuals =====>
def run_request(question_to_ask):
    task = "Generate python code Script. The script should only include code, no comments."
    
    # openai.api_key = "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"
    openai.api_key = openai_api_key

    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"system","content":task},{"role":"user","content":question_to_ask}])
    llm_response = response["choices"][0]["message"]["content"]
    llm_response = format_response(llm_response)
    return llm_response


def format_response(res):
     # Remove the load_csv from the answer if it exists
    csv_line = res.find("read_csv")
    if csv_line > 0:
        return_before_csv_line = res[0:csv_line].rfind("\n")
        if return_before_csv_line == -1:
            # The read_csv line is the first line so there is nothing to need before it
            res_before = ""
        else:
            res_before = res[0:return_before_csv_line]
        res_after = res[csv_line:]
        return_after_csv_line = res_after.find("\n")
        if return_after_csv_line == -1:
            # The read_csv is the last line
            res_after = ""
        else:
            res_after = res_after[return_after_csv_line:]
        res = res_before + res_after
    return res

def format_question(primer_desc,primer_code , question):
    instructions = ""

    primer_desc = primer_desc.format(instructions)

    return '"""\n' + primer_desc + question + '\n"""\n' + primer_code

def get_primer(df_dataset):
    # Primer function to take a dataframe and its name
    # and the name of the columns
    # and any columns with less than 20 unique values it adds the values to the primer
    # and horizontal grid lines and labeling
    primer_desc = "Use a dataframe called df from data_file.csv with columns '" \
        + "','".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i]=="O":
            primer_desc = primer_desc + "\nThe column '" + i + "' has categorical values '" + \
                "','".join(str(x) for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i]=="int64" or df_dataset.dtypes[i]=="float64":
            primer_desc = primer_desc + "\nThe column '" + i + "' is type " + str(df_dataset.dtypes[i]) + " and contains numeric values. "   
    primer_desc = primer_desc + "\nLabel the x and y axes appropriately."
    primer_desc = primer_desc + "\nAdd a title. Set the fig suptitle as empty."
    primer_desc = primer_desc + "{}" # Space for additional instructions if needed
    primer_desc = primer_desc + "\nUsing Python version 3.9.12, create a script using the dataframe df to graph the following: "
    pimer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    pimer_code = pimer_code + "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    pimer_code = pimer_code + "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False) \n"
    # pimer_code = pimer_code + "df=" + df_name + ".copy()\n"
    return primer_desc,pimer_code


def pdf_req(pdf, query):
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
      char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000,
                                                 chunk_overlap=200,length_function=len)
      text_chunks = char_text_splitter.split_text(text)
      
      # create embeddings
      embeddings = OpenAIEmbeddings()
      docsearch = FAISS.from_texts(text_chunks, embeddings) 
      llm = OpenAI() 
      chain = load_qa_chain(llm, chain_type="stuff")
      #--------------------------------------------------------------------------------------
      # show user input
      query = st.text_input("Type your question:")
      if query:
        docs = docsearch.similarity_search(query)
        response = chain.run(input_documents=docs, question=query)
           
        st.write(response)        
