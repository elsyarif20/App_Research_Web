import streamlit as st
import pandas as pd
from core_engine import ResearchEngine

# --- CONFIG ---
st.set_page_config(
    page_title="Ahim Statistics Data Editor",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS: THEMA SPSS CLASSIC ---
st.markdown("""
    <style>
    /* Mengatur background utama menjadi abu-abu terang khas Windows Klasik */
    .stApp {
        background-color: #f0f0f0;
        color: black;
    }

    /* Navbar/Header ala Windows XP/7 */
    .spss-header {
        background: linear-gradient(to bottom, #ebebeb 0%, #d1d1d1 100%);
        border-bottom: 2px solid #999;
        padding: 10px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }

    /* Styling Data Editor agar mirip grid SPSS */
    [data-testid="stDataEditor"] {
        border: 2px solid #718ca1;
        background-color: white;
    }

    /* Sidebar dengan warna abu-abu menu */
    section[data-testid="stSidebar"] {
        background-color: #e1e1e1;
        border-right: 2px solid #999;
    }

    /* Button bergaya standar software lama */
    div.stButton > button:first-child {
        background-color: #f5f5f5;
        color: #333;
        border: 1px solid #707070;
        border-radius: 2px;
        font-size: 13px;
    }
    
    div.stButton > button:hover {
        background-color: #e5f1fb;
        border: 1px solid #0078d7;
    }

    /* Tab Bergaya Data View / Variable View */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #dcdcdc;
        border-top: 1px solid #999;
    }

    .stTabs [data-baseweb="tab"] {
        border: 1px solid #999;
        background-color: #f0f0f0;
        padding: 5px 15px;
        margin-right: 2px;
        font-size: 12px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #fff !important;
        border-bottom: none !important;
        font-weight: bold;
    }
    
    /* Font kecil khas tabel statistik */
    p, span, label {
        font-size: 13px !important;
        color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SPSS STYLE HEADER ---
st.markdown("""
    <div class="spss-header">
        <span style="font-weight:bold; color:#003366;">*Untitled1 [DataSet1] - IBM Ahim Statistics Data Editor</span>
    </div>
    """, unsafe_allow_html=True)

# --- SESSION STATE (DATABASE) ---
if 'df' not in st.session_state:
    data = {
        'id': [1, 2, 3, 4, 5],
        'gender': ['Male', 'Male', 'Female', 'Female', 'Male'],
        'bdate': ['02/03/1952', '05/23/1958', '07/26/1929', '04/15/1947', '02/09/1955'],
        'salary': [57000, 40200, 21450, 21900, 45000],
        'jobcat': ['Manager', 'Clerical', 'Clerical', 'Clerical', 'Clerical']
    }
    st.session_state.df = pd.DataFrame(data)

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown("### Menu")
    uploaded_file = st.file_uploader("📂 Open Data (.sav, .csv, .xlsx)", type=['xlsx', 'csv'])
    if uploaded_file:
        imported = ResearchEngine.load_external_file(uploaded_file)
        if imported is not None:
            st.session_state.df = imported
            st.rerun()
            
    st.divider()
    st.button("➕ Add Variable")
    st.button("🗑️ Delete Case")

# --- MAIN VIEW: DATA VIEW & VARIABLE VIEW TABS ---
# Meniru navigasi bawah SPSS
tab_data, tab_var, tab_analyze = st.tabs(["Data View", "Variable View", "Analyze"])

with tab_data:
    # Menampilkan jumlah variabel aktif seperti di gambar
    st.caption(f"Visible: {len(st.session_state.df.columns)} of {len(st.session_state.df.columns)} Variables")
    
    # Spreadsheet Editor
    edited_df = st.data_editor(
        st.session_state.df, 
        num_rows="dynamic", 
        use_container_width=True,
        height=500,
        hide_index=False # Menampilkan nomor baris seperti SPSS
    )
    st.session_state.df = edited_df

with tab_var:
    st.subheader("Variable Definitions")
    # Menampilkan info kolom
    var_info = pd.DataFrame({
        'Name': st.session_state.df.columns,
        'Type': ['Numeric' if pd.api.types.is_numeric_dtype(st.session_state.df[c]) else 'String' for c in st.session_state.df.columns],
        'Width': [8] * len(st.session_state.df.columns),
        'Label': st.session_state.df.columns
    })
    st.table(var_info)

with tab_analyze:
    st.subheader("Statistical Procedures")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("--- Descriptive Statistics ---")
        items_x = st.multiselect("Select Variables (X):", st.session_state.df.columns)
        y_var = st.selectbox("Select Dependent (Y):", st.session_state.df.columns)
        
    with col2:
        st.write("--- Results ---")
        if st.button("Run Regression Analysis"):
            if items_x and y_var:
                model, narasi = ResearchEngine.run_dynamic_regression(st.session_state.df, items_x, y_var)
                st.info(narasi)

# --- FOOTER STATUS BAR ---
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #f0f0f0; border-top: 1px solid #999; padding: 2px 10px; font-size: 11px;">
        IBM Ahim Statistics Processor is ready | Unicode: ON
    </div>
    """, unsafe_allow_html=True)

