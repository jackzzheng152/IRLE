import pandas as pd
import streamlit as st
import base64
from io import BytesIO
import xlsxwriter
st.set_page_config(page_title="UCLA IRLE Scheduler", page_icon = ":calendar:", layout="wide")
def download_excel(df_list):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    for i, df in enumerate(df_list):
        sheet_name = ["Facilitator", "NoteTaker", "CleanUp"][i]
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="schedule.xlsx">Download Excel File</a>'
    return href
st.header("UCLA IRLE Meeting Scheduler")



with st.container():
    left_body, right_body = st.columns([2.3, 1])
    with right_body:
        st.subheader("Date")
        date_input = st.text_input("Enter dates (separated by commas):", placeholder="MM/DD/YYYY,MM/DD/YYYY,etc")
        date = [date.strip() for date in date_input.split(",")]
        number_of_meeting = len(date)
        st.write("---")
        st.subheader("Parameters")
        num_fac = int(st.text_input("Enter # of Facilitators per Meeting", value=2))
        num_nt = int(st.text_input("Enter # of Note Takers per Meeting", value=1))
        num_cu = int(st.text_input("Enter # of Clean Up per Meeting", value=3))
        st.write("---")
        st.subheader("Absence")
        curr_people = []
        absence_input = st.text_input()
        st.write("---")
        st.subheader("Upload File")
        uploaded_file = st.file_uploader("")
        if uploaded_file is not None:
            df1 = pd.read_excel(uploaded_file, 'Facilitator')
            df2 = pd.read_excel(uploaded_file, 'NoteTaker')
            df3 = pd.read_excel(uploaded_file, 'CleanUp')        
        st.write("---")
        
    with left_body:
        
        if uploaded_file is not None:
            for i in range(number_of_meeting):
                total_people = len(df1['Staff Name'])
                for k in range(num_fac):
                    for j in range(total_people):
                        if df1['Last Facilitated'].notna().all():
                            for l in range(total_people - 6):
                                df1.at[l, 'Last Facilitated'] = pd.NaT
                            df1 = df1.sort_values(by="Last Facilitated")
                        if df1['Last Facilitated'][j] is pd.NaT:
                            df1.at[j, "Last Facilitated"] = date[i]
                            curr_people.append(df1['Staff Name'][j])
                            break
                df1 = df1.sort_values(by="Last Facilitated")
                for k in range(num_nt):
                    for j in range(total_people):
                        if df2['Last Notetaker'].notna().all():
                            for l in range(total_people - 3):
                                df2.at[l, 'Last Notetaker'] = pd.NaT
                            df2 = df2.sort_values(by="Last Notetaker")
                        if df2['Last Notetaker'][j] is pd.NaT and df2['Staff Name'][j] not in curr_people:
                            df2.at[j, "Last Notetaker"] = date[i]
                            curr_people.append(df2['Staff Name'][j])
                            break
                df2 = df2.sort_values(by="Last Notetaker")
                for k in range(num_cu):
                    for j in range(total_people):
                        if df3['Set Up/Clean up'].notna().all():
                            for l in range(total_people - 9):
                                df3.at[l, 'Set Up/Clean up'] = pd.NaT
                            df3 = df3.sort_values(by="Set Up/Clean up")
                        if df3['Set Up/Clean up'][j] is pd.NaT and df3['Staff Name'][j] not in curr_people:
                            df3.at[j, "Set Up/Clean up"] = date[i]
                            curr_people.append(df3['Staff Name'][j])
                            break
                df3 = df3.sort_values(by="Set Up/Clean up")
                st.write(
                    f'Meeting {date[i]}: \n Facilitator - ({curr_people[:num_fac]}) \n Notetaker - {curr_people[num_fac:num_fac+num_nt]} \n CleanUp - {curr_people[num_fac+num_nt:num_fac+num_nt+num_cu]}')
                st.write("---")
                curr_people = []
            st.subheader("Download File")
            st.markdown(download_excel([df1, df2, df3]), unsafe_allow_html=True)






