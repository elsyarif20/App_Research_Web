import streamlit as st
import pandas as pd
from core_engine import ResearchEngine

# --- KONFIGURASI ---
st.set_page_config(page_title="Ahim Statistics - SMA Islam Al Ghozali", layout="wide")

# --- CSS SPSS CLASSIC ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; color: black; }
    [data-testid="stDataEditor"] { border: 2px solid #718ca1; background-color: white; }
    .spss-bar { background: #d1d1d1; padding: 5px; border-bottom: 2px solid #999; font-weight: bold; color: #003366; }
    div.stButton > button { background-color: #e1e1e1; border: 1px solid #707070; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="spss-bar">*Data_Penelitian_Liyas.sav [DataSet1] - Ahim Statistics</div>', unsafe_allow_html=True)

# --- DATABASE ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Responden', 'Pre_Test', 'Post_Test'])
    st.session_state.df.loc[0] = ["Siswa 1", 60, 85]

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Menu Data")
    if st.button("➕ Tambah Baris"):
        st.session_state.df.loc[len(st.session_state.df)] = [""] * len(st.session_state.df.columns)
        st.rerun()
    
    col_name = st.text_input("Nama Kolom/Variabel Baru:")
    if st.button("📁 Tambah Kolom"):
        if col_name:
            st.session_state.df[col_name] = 0.0
            st.rerun()

# --- EDITOR UTAMA ---
st.subheader("Data Editor (Tampilan Spreadsheet)")
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=False)
st.session_state.df = edited_df

st.divider()

# --- ANALISIS ---
st.subheader("🔬 Laboratorium Analisis Statistik")
tab1, tab2, tab3 = st.tabs(["🎯 Validitas Instrumen", "📈 Analisis Regresi", "⚖️ Uji Beda (T-Test)"])

cols = st.session_state.df.columns.tolist()

with tab1:
    st.write("Gunakan menu ini untuk menguji apakah butir kuesioner Anda valid untuk digunakan dalam penelitian.")
    items = st.multiselect("Pilih Butir Soal untuk Diuji:", cols)
    if st.button("Mulai Cek Validitas"):
        if items:
            res = ResearchEngine.run_item_validity(st.session_state.df, items)
            st.table(res)

with tab2:
    st.write("Gunakan menu ini untuk melihat seberapa besar pengaruh variabel X terhadap variabel Y.")
    cx1, cx2 = st.columns(2)
    with cx1: x_vars = st.multiselect("Variabel Bebas (X):", cols)
    with cx2: y_var = st.selectbox("Variabel Terikat (Y):", cols)
    
    if st.button("Jalankan Uji Regresi"):
        if x_vars and y_var:
            model, narasi = ResearchEngine.run_dynamic_regression(st.session_state.df, x_vars, y_var)
            if model:
                st.markdown(f"<div style='background: white; padding: 20px; border: 1px solid #999; color: black;'>{narasi}</div>", unsafe_allow_html=True)
                st.pyplot(ResearchEngine.generate_chart(st.session_state.df, x_vars[0], y_var))

with tab3:
    st.write("Gunakan menu ini untuk membandingkan rata-rata dari dua kelompok data (misalnya Pre-test vs Post-test).")
    t1, t2 = st.columns(2)
    with t1: var_a = st.selectbox("Data Kelompok A:", cols)
    with t2: var_b = st.selectbox("Data Kelompok B:", cols)
    
    if st.button("Mulai Uji T"):
        t_stat, p_val, narasi_t = ResearchEngine.run_t_test(st.session_state.df, var_a, var_b)
        st.markdown(f"<div style='background: #e5f1fb; padding: 15px; border-left: 5px solid #0078d7; color: black;'>{narasi_t}</div>", unsafe_allow_html=True)
