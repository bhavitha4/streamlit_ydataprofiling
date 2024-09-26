import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import os
import sys
st.set_page_config(page_title="Data profiler",layout="wide")

def get_filesize(file):
    size_bytes=sys.getsizeof(file)
    size_mb = size_bytes/(1024**2)
    return size_mb

def validate_file(file):
    filename= file.name
    name , ext = os.path.splitext(filename)
    if ext in(".csv",".xlsx"):
        return ext
    else:
        return False
# Sidebar for file upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a .csv or .xlsx file (max. 10 MB)", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        st.write("Modes of operations")
        minimal=st.checkbox("do you want minimal report ?")
        display_mode=st.radio("display mode:",options=("primary","dark","orange")
                              )
        if display_mode =="primary":
            dark_mode=True
            orange_mode=False
        elif display_mode == "orange":
            dark_mode=False
            orange_mode=True
        else:
            dark_mode=False
            orange_mode=False


if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize=get_filesize(uploaded_file)
        if filesize <=10:
            if ext == ".csv":
                df =pd.read_csv(uploaded_file)
            else:
                xl_file=pd.ExcelFile(uploaded_file)
                sheet_tuple=tuple(xl_file.sheet_names)
                sheet_name=st.sidebar.selectbox("select the sheet",sheet_tuple)
                df=xl_file.parse(sheet_name)
        
            with st.spinner("Generating the report..."): 
                # Generate profile report
                pr = ProfileReport(df,minimal=minimal,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode)
                
                # Display the profile report
            st_profile_report(pr)

        else:
            st.error(f"maximum allowed filesize is 10 MB, but received {filesize} MB")
    else:
        st.error("kindly upload only .csv or .xlsx file")
else:
    st.title("Data profile")
    st.info("upload your data in the left sidebar to generate profiling")
    