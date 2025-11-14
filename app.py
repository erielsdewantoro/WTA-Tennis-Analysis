import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="WTA Tennis Match Analysis",
    page_icon="🎾",
    layout="wide" 
)

# 2. CACHING DATA
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

# Load data Anda
try:
    data = load_data('wta_processed.csv') 
except FileNotFoundError:
    st.error("File 'wta_processed.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()

# 3. JUDUL DAN DESKRIPSI
st.title("🎾 WTA Tennis Match Analysis Dashboard")
st.write("""
Analisis interaktif ini melihat data pertandingan WTA dari 2006-2025. 
Gunakan filter di sidebar untuk menjelajahi data.
""")

# 4. SIDEBAR (FILTER)
st.sidebar.header("Filter Data")

# --- PERBAIKAN 1 ---
# Mengganti 'Year' menjadi 'year' (huruf kecil)
unique_years = sorted(data['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + unique_years)

if selected_year != "Semua":
    data_filtered = data[data['year'] == selected_year]
else:
    data_filtered = data.copy()

# 'Surface' sudah benar
unique_surfaces = sorted(data['Surface'].unique())
selected_surface = st.sidebar.multiselect("Pilih Jenis Lapangan", unique_surfaces, default=unique_surfaces)

if selected_surface:
    data_filtered = data_filtered[data_filtered['Surface'].isin(selected_surface)]
else:
    st.warning("Pilih setidaknya satu jenis lapangan.")
    st.stop()

# 5. HALAMAN UTAMA (MAIN PAGE)
st.header("Gambaran Umum Data (Berdasarkan Filter)")

# 'Winner' sudah benar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pertandingan", f"{data_filtered.shape[0]:,}")
with col2:
    st.metric("Pemain Unik", data_filtered['Winner'].nunique())
with col3:
    # --- PERBAIKAN 2 ---
    # Mengganti 'Avg_Sets' menjadi 'sets_played'
    st.metric("Rata-rata Set", f"{data_filtered['sets_played'].mean():.2f}")
with col4:
    # --- PERBAIKAN 3 ---
    # Mengganti 'Upset_Rate' menjadi 'upset'
    st.metric("Upset Rate (%)", f"{data_filtered['upset'].mean() * 100:.1f}%")

# 6. TAMPILKAN GRAFIK
st.header("Visualisasi Data")
st.subheader("Top 10 Pemain dengan Kemenangan Terbanyak")
# 'Winner' sudah benar
top_10_winners = data_filtered['Winner'].value_counts().head(10).reset_index()
top_10_winners.columns = ['Player', 'Total Wins']
st.bar_chart(top_10_winners.set_index('Player'))

st.subheader("Pratinjau Data (Sesuai Filter)")
st.dataframe(data_filtered.head())