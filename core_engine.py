import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

class ResearchEngine:
    @staticmethod
    def load_external_file(file_path):
        """Membaca file eksternal (Excel/CSV)"""
        ext = os.path.splitext(str(file_path))[-1].lower()
        try:
            if ext == '.csv':
                return pd.read_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
        except: return None
        return None

    @staticmethod
    def run_item_validity(df, item_cols):
        """Uji Validitas Butir menggunakan Korelasi Pearson"""
        df_num = df[item_cols].apply(pd.to_numeric, errors='coerce').dropna()
        if len(df_num) < 3: return None
        
        total_score = df_num.sum(axis=1)
        validity_results = []
        for col in item_cols:
            r_calc, p_val = stats.pearsonr(df_num[col], total_score)
            status = "✅ Valid" if p_val < 0.05 else "❌ Tidak Valid"
            validity_results.append({
                "Butir/Item": col,
                "R-Hitung": round(r_calc, 3),
                "P-Value": round(p_val, 4),
                "Status": status
            })
        return pd.DataFrame(validity_results)

    @staticmethod
    def run_dynamic_regression(df, x_cols, y_col):
        """Analisis Regresi Berganda Dinamis"""
        df_clean = df[x_cols + [y_col]].apply(pd.to_numeric, errors='coerce').dropna()
        if len(df_clean) < 3: return None, "Data tidak cukup (Min. 3 baris numerik)."

        X = sm.add_constant(df_clean[x_cols])
        y = df_clean[y_col]
        model = sm.OLS(y, X).fit()
        
        r2, f_sig = round(model.rsquared, 3), round(model.f_pvalue, 4)
        narasi = f"""
        <b>HASIL ANALISIS REGRESI:</b><br>
        - Variabel: {', '.join(x_cols)} terhadap {y_col}<br>
        - Koefisien Determinasi (R²): {r2} ({r2*100}% pengaruh)<br>
        - Signifikansi (P-Value): {f_sig}<br>
        - Kesimpulan: Hipotesis <b>{'DITERIMA' if f_sig < 0.05 else 'DITOLAK'}</b>.
        """
        return model, narasi

    @staticmethod
    def run_t_test(df, col1, col2):
        """Uji T Independen untuk membandingkan dua kelompok"""
        d1 = pd.to_numeric(df[col1], errors='coerce').dropna()
        d2 = pd.to_numeric(df[col2], errors='coerce').dropna()
        if len(d1) < 2 or len(d2) < 2: return None, None, "Data kurang untuk Uji T."
        
        t_stat, p_val = stats.ttest_ind(d1, d2)
        status = "Signifikan" if p_val < 0.05 else "Tidak Signifikan"
        narasi = f"Hasil Uji T: P-Value {round(p_val, 4)}. Perbedaan dinyatakan <b>{status}</b>."
        return round(t_stat, 3), round(p_val, 4), narasi

    @staticmethod
    def generate_chart(df, x_col, y_col):
        """Membuat Grafik untuk Streamlit"""
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 5))
        df_plot = df[[x_col, y_col]].apply(pd.to_numeric, errors='coerce').dropna()
        ax.scatter(df_plot[x_col], df_plot[y_col], color='#8aadf4', alpha=0.7)
        m, b = np.polyfit(df_plot[x_col], df_plot[y_col], 1)
        ax.plot(df_plot[x_col], m*df_plot[x_col] + b, color='#ed8796', linewidth=2)
        ax.set_title(f"Tren {x_col} vs {y_col}")
        return fig