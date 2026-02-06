import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

class ResearchEngine:
    @staticmethod
    def run_dynamic_regression(df, x_cols, y_col):
        """Analisis Regresi dengan Interpretasi Otomatis Bahasa Indonesia"""
        try:
            df_clean = df[x_cols + [y_col]].apply(pd.to_numeric, errors='coerce').dropna()
            
            if len(df_clean) < 3:
                return None, "Data tidak cukup. Minimal butuh 3 baris data angka."

            X = sm.add_constant(df_clean[x_cols])
            y = df_clean[y_col]
            model = sm.OLS(y, X).fit()
            
            r2 = round(model.rsquared, 3)
            f_sig = round(model.f_pvalue, 4)
            
            # Narasi Interpretasi Otomatis
            narasi = f"<b>HASIL ANALISIS REGRESI LINIER BERGANDA</b><br><br>"
            narasi += f"Berdasarkan hasil pengujian pada variabel independen ({', '.join(x_cols)}) terhadap variabel dependen ({y_col}), diperoleh data sebagai berikut:<br>"
            narasi += f"1. <b>Koefisien Determinasi (R²):</b> Nilai R-Square sebesar {r2} menunjukkan bahwa variabel X berkontribusi sebesar {r2*100}% terhadap variasi variabel Y.<br>"
            narasi += f"2. <b>Uji Signifikansi (Uji F):</b> Diperoleh nilai signifikansi sebesar {f_sig}.<br><br>"
            
            if f_sig < 0.05:
                narasi += f"<b>KESIMPULAN:</b> Karena nilai signifikansi {f_sig} < 0,05, maka <b>Hipotesis Diterima</b>. "
                narasi += f"Artinya, terdapat pengaruh yang signifikan secara simultan antara variabel {', '.join(x_cols)} terhadap {y_col}."
            else:
                narasi += f"<b>KESIMPULAN:</b> Karena nilai signifikansi {f_sig} > 0,05, maka <b>Hipotesis Ditolak</b>. "
                narasi += f"Artinya, tidak terdapat pengaruh yang signifikan antara variabel tersebut."
            
            return model, narasi
        except Exception as e:
            return None, f"Terjadi kesalahan analisis: {str(e)}"

    @staticmethod
    def run_item_validity(df, item_cols):
        """Uji Validitas Butir Instrumen"""
        df_num = df[item_cols].apply(pd.to_numeric, errors='coerce').dropna()
        if len(df_num) < 3: return None
        
        total_score = df_num.sum(axis=1)
        validity_results = []
        for col in item_cols:
            r_hitung, p_val = stats.pearsonr(df_num[col], total_score)
            status = "✅ VALID" if p_val < 0.05 else "❌ TIDAK VALID"
            validity_results.append({
                "Butir Soal": col,
                "R-Hitung": round(r_hitung, 3),
                "Sig (P-Value)": round(p_val, 4),
                "Keterangan": status
            })
        return pd.DataFrame(validity_results)

    @staticmethod
    def run_t_test(df, col1, col2):
        """Uji T (Perbandingan Dua Kelompok)"""
        d1 = pd.to_numeric(df[col1], errors='coerce').dropna()
        d2 = pd.to_numeric(df[col2], errors='coerce').dropna()
        
        t_stat, p_val = stats.ttest_ind(d1, d2)
        status = "SIGNIFIKAN" if p_val < 0.05 else "TIDAK SIGNIFIKAN"
        
        narasi = f"<b>HASIL UJI BEDA (UJI T):</b><br>"
        narasi += f"Perbandingan antara rata-rata {col1} dan {col2} menghasilkan nilai P-Value: {round(p_val, 4)}.<br>"
        narasi += f"Kesimpulan: Perbedaan antara kedua kelompok dinyatakan <b>{status}</b>."
        
        return round(t_stat, 3), round(p_val, 4), narasi

    @staticmethod
    def generate_chart(df, x_col, y_col):
        plt.style.use('ggplot') # Gaya grafik yang lebih bersih untuk laporan
        fig, ax = plt.subplots(figsize=(8, 5))
        df_plot = df[[x_col, y_col]].apply(pd.to_numeric, errors='coerce').dropna()
        
        ax.scatter(df_plot[x_col], df_plot[y_col], color='blue', alpha=0.5, label='Data Riil')
        m, b = np.polyfit(df_plot[x_col], df_plot[y_col], 1)
        ax.plot(df_plot[x_col], m*df_plot[x_col] + b, color='red', linewidth=2, label='Garis Regresi')
        
        ax.set_title(f"Grafik Pengaruh {x_col} terhadap {y_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()
        return fig
