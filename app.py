import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Academic Curriculum Manager", layout="wide")

# IMPROVED CSS: Works for both Light and Dark mode
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("academic_curriculum.csv")
        df.columns = df.columns.str.strip()
        df["YearOfStudy"] = df["YearOfStudy"].astype(str)
        return df
    except Exception:
        return None

df = load_data()

if df is not None:
    st.title("🎓 Academic Curriculum Dashboard")
    st.info("💡 **Tip:** If you leave a filter empty, it will show **all** results for that category.")

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Controls")
    
    all_programs = sorted(df["ProgramName"].unique())
    program_select = st.sidebar.multiselect("Programs", options=all_programs)

    all_years = sorted(df["YearOfStudy"].unique())
    year_select = st.sidebar.multiselect("Years of Study", options=all_years)

    all_semesters = sorted(df["SemesterName"].unique())
    semester_select = st.sidebar.multiselect("Semesters", options=all_semesters)

    all_types = sorted(df["ModuleType"].unique())
    mod_type_select = st.sidebar.multiselect("Module Types", options=all_types)

    # "Show All" Logic
    f_programs = program_select if program_select else all_programs
    f_years = year_select if year_select else all_years
    f_semesters = semester_select if semester_select else all_semesters
    f_types = mod_type_select if mod_type_select else all_types

    filtered_df = df[
        (df["ProgramName"].isin(f_programs)) & 
        (df["YearOfStudy"].isin(f_years)) & 
        (df["SemesterName"].isin(f_semesters)) &
        (df["ModuleType"].isin(f_types))
    ]

    # --- Metrics (The part that looked broken in your image) ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Modules", len(filtered_df))
    m2.metric("Years Active", len(f_years))
    m3.metric("Semesters Active", len(f_semesters))

    st.divider()
    
    # --- Search and Table ---
    search = st.text_input("🔍 Search by Module Name or Code", "")
    if search:
        filtered_df = filtered_df[filtered_df['Modules'].str.contains(search, case=False, na=False)]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # --- Download ---
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.sidebar.markdown("---")
    st.sidebar.download_button("📥 Export CSV", data=csv, file_name="curriculum.csv", mime="text/csv")

else:
    st.error("🚨 'academic_curriculum.csv' not found!")