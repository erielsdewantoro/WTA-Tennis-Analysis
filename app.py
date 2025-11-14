import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="WTA Tennis Match Dashboard",
    page_icon="🎾", # Ikon tab browser
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PERUBAHAN V3.0: SUNTIKAN CSS KUSTOM ---
# Kita tambahkan CSS untuk memperbesar judul utama dan memberinya sedikit penekanan
st.markdown("""
    <style>
    /* Mengubah font dan ukuran judul utama (H1) */
    .stApp [data-testid="stHeader"] {
        font-size: 3rem; /* 3rem sedikit lebih besar dari default */
        font-weight: 700; /* Lebih tebal */
        padding-top: 1rem; /* Beri sedikit jarak di atas */
    }
    /* Mengubah font dan ukuran sub-header (H2) */
    .stApp h2 {
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
# --- AKHIR PERUBAHAN V3.0 ---

# 2. CACHING DATA
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

try:
    data = load_data('wta_processed.csv') 
except FileNotFoundError:
    st.error("File 'wta_processed.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()

# 3. JUDUL UTAMA
# Kita tambahkan ikon di judul utama
st.title("🏆 WTA Tennis Match Analysis")
st.markdown("Dashboard interaktif untuk menganalisis **42,000+** pertandingan tenis WTA (2006-2025).")

# 4. SIDEBAR (FILTER)
st.sidebar.header("Filter Data 📊")
unique_years = sorted(data['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + unique_years)
unique_surfaces = sorted(data['Surface'].unique())
selected_surface = st.sidebar.multiselect("Pilih Jenis Lapangan", unique_surfaces, default=unique_surfaces)

# 5. TERAPKAN FILTER KE DATA
if selected_year != "Semua Tahun":
    data_filtered = data[data['year'] == selected_year]
else:
    data_filtered = data.copy()
if selected_surface:
    data_filtered = data_filtered[data_filtered['Surface'].isin(selected_surface)]
else:
    data_filtered = data_filtered.copy() 
if data_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter Anda. Coba ubah pilihan filter.")
    st.stop()

# 6. KONTEN UTAMA DENGAN TABS
# --- PERUBAHAN V3.0: IKON TABS BARU ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard Utama 📈", 
    "Analisis Lapangan 🏟️", 
    "Upset & Odds 🎾", 
    "Jelajahi Data 📊"
])
# --- AKHIR PERUBAHAN V3.0 ---

# === KONTEN TAB 1: DASHBOARD UTAMA ===
with tab1:
    st.header("Gambaran Umum Performa")
    st.markdown("Metrik performa kunci berdasarkan filter yang Anda pilih.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pertandingan", f"{data_filtered.shape[0]:,}")
    with col2:
        st.metric("Pemain Unik", data_filtered['Winner'].nunique())
    with col3:
        st.metric("Rata-rata Set", f"{data_filtered['sets_played'].mean():.2f}")
    with col4:
        st.metric("Upset Rate", f"{data_filtered['upset'].mean() * 100:.1f}%")

    st.markdown("---")
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.subheader("Top 10 Pemain dengan Kemenangan Terbanyak")
        top_10_winners = data_filtered['Winner'].value_counts().head(10).reset_index()
        top_10_winners.columns = ['Player', 'Total Wins']
        fig_bar = px.bar(
            top_10_winners, 
            x='Total Wins', 
            y='Player', 
            orientation='h',
            title="Top 10 Pemain Pemenang",
            labels={'Player': 'Pemain', 'Total Wins': 'Jumlah Kemenangan'},
            text='Total Wins'
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan pemain paling dominan. Gunakan filter tahun untuk melihat siapa yang mendominasi di tahun tertentu.")

    with col_kanan:
        st.subheader("Distribusi Pertandingan per Babak")
        round_distribution = data_filtered['Round'].value_counts().reset_index()
        round_distribution.columns = ['Round', 'Count']
        fig_pie = px.pie(
            round_distribution, 
            names='Round', 
            values='Count', 
            title="Persentase Pertandingan per Babak",
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info("💡 **Insight:** Seperti yang terlihat, sebagian besar pertandingan terjadi di babak-babak awal turnamen.")

# === KONTEN TAB 2: ANALISIS LAPANGAN ===
with tab2:
    st.header("Analisis Performa Berdasarkan Jenis Lapangan")
    st.markdown("Bagaimana jenis lapangan (Surface) memengaruhi hasil pertandingan?")
    surface_wins = data_filtered['Surface'].value_counts().reset_index()
    surface_wins.columns = ['Surface', 'Total Matches']
    fig_surface = px.bar(
        surface_wins,
        x='Surface',
        y='Total Matches',
        title="Jumlah Pertandingan per Jenis Lapangan",
        labels={'Surface': 'Jenis Lapangan', 'Total Matches': 'Jumlah Pertandingan'},
        color='Surface'
    )
    st.plotly_chart(fig_surface, use_container_width=True)
    st.info("💡 **Insight:** Lapangan 'Hard' jelas mendominasi jumlah turnamen yang dimainkan sepanjang tahun.")

# === KONTEN TAB 3: ANALISIS UPSET & ODDS ===
with tab3:
    st.header("Analisis Upset dan Odds (Peluang)")
    st.markdown("Menganalisis frekuensi kemenangan tak terduga (upset) dan hubungannya dengan odds.")
    
    col_upset_1, col_upset_2 = st.columns(2)
    with col_upset_1:
        st.metric("Total Upset Terjadi", f"{data_filtered['upset'].sum():,}")
    with col_upset_2:
        st.metric("Rata-rata Odds Gap", f"{data_filtered['odds_gap'].mean():.2f}")

    st.markdown("---")
    st.subheader("Tren Upset Rate dari Tahun ke Tahun")
    
    if selected_year == "Semua Tahun":
        upset_trend = data[data['Surface'].isin(selected_surface)].groupby('year')['upset'].mean().reset_index()
        upset_trend.columns = ['Year', 'Upset Rate']
        fig_line = px.line(
            upset_trend,
            x='Year',
            y='Upset Rate',
            title="Fluktuasi Upset Rate Tahunan",
            labels={'Year': 'Tahun', 'Upset Rate': 'Rata-rata Upset Rate'},
            markers=True
        )
        fig_line.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_line, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan apakah tenis menjadi lebih atau kurang dapat diprediksi dari waktu ke waktu. Gunakan filter 'Jenis Lapangan' untuk melihat tren di lapangan tertentu.")
    else:
        st.warning(f"Grafik tren tahunan hanya dapat ditampilkan jika Anda memilih 'Semua Tahun' di filter sidebar. (Anda sedang memilih {selected_year})")

# === KONTEN TAB 4: EXPLORE DATA ===
with tab4:
    st.header("Jelajahi Data Mentah")
    st.markdown("Lihat data yang telah difilter dalam format tabel.")
    with st.expander("Tampilkan Data (sesuai filter)", expanded=False):
        st.dataframe(data_filtered)
    st.markdown(f"Menampilkan **{data_filtered.shape[0]:,} baris** dari **{data.shape[0]:,} total baris**.")
