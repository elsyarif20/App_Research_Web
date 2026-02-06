import streamlit as st
import pandas as pd
from core_engine import ResearchEngine

# --- CONFIG ---
st.set_page_config(page_title="Ahim Research Pro | Liyas Syarifudin", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #1e1e2e; color: #cad3f5; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (DATABASE) ---
if 'df' not in st.session_state:
    # Template awal penelitian sekolah
    data = {
        'Responden': [f'Siswa {i}' for i in range(1, 6)],
        'Item_1': [5, 4, 3, 5, 4],
        'Item_2': [4, 4, 2, 5, 3],
        'Pre_Test': [60, 65, 50, 70, 62],
        'Post_Test': [85, 80, 75, 90, 82]
    }
    st.session_state.df = pd.DataFrame(data)

# --- SIDEBAR: KONTROL DATA ---
with st.sidebar:
    st.title("🛠️ Control Panel")
    st.info(f"Developer: Liyas Syarifudin\nLokasi: SMA Islam Al Ghozali")
    
    st.subheader("Manajemen Kolom")
    new_col = st.text_input("Nama Variabel Baru:")
    if st.button("➕ Tambah Kolom"):
        if new_col:
            st.session_state.df[new_col] = 0
            st.rerun()

    st.subheader("Eksternal Data")
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=['xlsx', 'csv'])
    if uploaded_file:
        imported = ResearchEngine.load_external_file(uploaded_file)
        if imported is not None:
            st.session_state.df = imported
            st.success("Data Berhasil Dimuat!")

# --- MAIN DASHBOARD ---
st.title("🚀 Ahim Research Pro - Dashboard Riset")
st.divider()

# Layout: Spreadsheet di atas, Analisis di bawah
st.subheader("📊 Spreadsheet Editor (Excel-Like)")
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
st.session_state.df = edited_df

st.divider()

# --- BAGIAN ANALISIS ---
st.subheader("🧪 Laboratory Analisis")
tab1, tab2, tab3 = st.tabs(["🎯 Validitas Butir", "📈 Regresi & Pengaruh", "⚖️ Uji T (Beda Rata-rata)"])

cols = st.session_state.df.columns.tolist()

with tab1:
    st.markdown("### Uji Validitas Instrumen")
    items = st.multiselect("Pilih Butir Kuesioner (Item Soal):", cols)
    if st.button("Jalankan Uji Validitas"):
        if items:
            res_val = ResearchEngine.run_item_validity(st.session_state.df, items)
            st.table(res_val)
        else: st.warning("Pilih butir dulu!")

with tab2:
    st.markdown("### Uji Regresi Linear Berganda")
    c1, c2 = st.columns(2)
    with c1: x_vars = st.multiselect("Variabel Bebas (X):", cols)
    with c2: y_var = st.selectbox("Variabel Terikat (Y):", cols)
    
    if st.button("Hitung Pengaruh"):
        if x_vars and y_var:
            model, narasi = ResearchEngine.run_dynamic_regression(st.session_state.df, x_vars, y_var)
            if model:
                st.write(narasi, unsafe_allow_html=True)
                st.pyplot(ResearchEngine.generate_chart(st.session_state.df, x_vars[0], y_var))
        else: st.warning("Lengkapi variabel X dan Y!")

with tab3:
    st.markdown("### Uji Beda (Independent T-Test)")
    t1, t2 = st.columns(2)
    with t1: var1 = st.selectbox("Kelompok A (Misal: Pre-test):", cols)
    with t2: var2 = st.selectbox("Kelompok B (Misal: Post-test):", cols)
    
    if st.button("Bandingkan Data"):
        t_stat, p_val, narasi_t = ResearchEngine.run_t_test(st.session_state.df, var1, var2)
        if t_stat:
            st.metric("P-Value", p_val)
            st.write(narasi_t, unsafe_allow_html=True)

# --- DOWNLOAD AREA ---
st.divider()
csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Data CSV", data=csv_data, file_name="data_ahim_pro.csv")