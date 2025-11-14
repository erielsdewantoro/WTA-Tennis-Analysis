import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN (LEBIH LENGKAP)
st.set_page_config(
    page_title="WTA Tennis Match Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded" # Sidebar langsung terbuka
)

# 2. CACHING DATA (TETAP SAMA)
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Konversi kolom tanggal jika perlu
    # data['Date'] = pd.to_datetime(data['Date'])
    return data

# Load data Anda
try:
    data = load_data('wta_processed.csv') 
except FileNotFoundError:
    st.error("File 'wta_processed.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()

# 3. JUDUL UTAMA (DESAIN BARU)
st.title("🎾 WTA Tennis Match Analysis")
st.markdown("Dashboard interaktif untuk menganalisis **42,000+** pertandingan tenis WTA (2006-2025).")

# 4. SIDEBAR (FILTER)
st.sidebar.header("Filter Data 📊")

# Filter Tahun
unique_years = sorted(data['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + unique_years)

# Filter Jenis Lapangan
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
    # Jika pengguna menghapus semua pilihan, tampilkan semua data
    data_filtered = data_filtered.copy() 

# Jika filter menghasilkan data kosong
if data_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter Anda. Coba ubah pilihan filter.")
    st.stop()

# 6. KONTEN UTAMA DENGAN TABS (INI BAGIAN BESARNYA!)
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Gambaran Umum", 
    "🏟️ Analisis Lapangan", 
    "⚡ Analisis Upset & Odds", 
    "Explore Data"
])

# === KONTEN TAB 1: GAMBARAN UMUM ===
with tab1:
    st.header("Gambaran Umum Performa")
    st.markdown("Metrik performa kunci berdasarkan filter yang Anda pilih.")
    
    # KPI (Key Performance Indicators)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pertandingan", f"{data_filtered.shape[0]:,}")
    with col2:
        st.metric("Pemain Unik", data_filtered['Winner'].nunique())
    with col3:
        st.metric("Rata-rata Set", f"{data_filtered['sets_played'].mean():.2f}")
    with col4:
        st.metric("Upset Rate", f"{data_filtered['upset'].mean() * 100:.1f}%")

    st.markdown("---") # Garis pemisah

    # Visualisasi di Tab 1
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.subheader("Top 10 Pemain dengan Kemenangan Terbanyak")
        
        # Hitung Top 10
        top_10_winners = data_filtered['Winner'].value_counts().head(10).reset_index()
        top_10_winners.columns = ['Player', 'Total Wins']
        
        # Grafik Interaktif dengan Plotly
        fig_bar = px.bar(
            top_10_winners, 
            x='Total Wins', 
            y='Player', 
            orientation='h', # Horizontal bar chart
            title="Top 10 Pemain Pemenang",
            labels={'Player': 'Pemain', 'Total Wins': 'Jumlah Kemenangan'},
            text='Total Wins' # Tampilkan angka di dalam bar
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}) # Urutkan dari kecil ke besar
        st.plotly_chart(fig_bar, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan pemain paling dominan. Gunakan filter tahun untuk melihat siapa yang mendominasi di tahun tertentu.")

    with col_kanan:
        st.subheader("Distribusi Pertandingan per Babak")
        
        # Hitung distribusi
        round_distribution = data_filtered['Round'].value_counts().reset_index()
        round_distribution.columns = ['Round', 'Count']
        
        # Grafik Donat dengan Plotly
        fig_pie = px.pie(
            round_distribution, 
            names='Round', 
            values='Count', 
            title="Persentase Pertandingan per Babak",
            hole=0.4 # Ini yang membuatnya jadi Donut Chart
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info("💡 **Insight:** Seperti yang terlihat, sebagian besar pertandingan terjadi di babak-babak awal turnamen.")

# === KONTEN TAB 2: ANALISIS LAPANGAN ===
with tab2:
    st.header("Analisis Performa Berdasarkan Jenis Lapangan")
    st.markdown("Bagaimana jenis lapangan (Surface) memengaruhi hasil pertandingan?")

    # Hitung Kemenangan per Jenis Lapangan
    surface_wins = data_filtered['Surface'].value_counts().reset_index()
    surface_wins.columns = ['Surface', 'Total Matches']

    # Grafik Bar Vertikal dengan Plotly
    fig_surface = px.bar(
        surface_wins,
        x='Surface',
        y='Total Matches',
        title="Jumlah Pertandingan per Jenis Lapangan",
        labels={'Surface': 'Jenis Lapangan', 'Total Matches': 'Jumlah Pertandingan'},
        color='Surface' # Beri warna berbeda
    )
    st.plotly_chart(fig_surface, use_container_width=True)
    st.info("💡 **Insight:** Lapangan 'Hard' jelas mendominasi jumlah turnamen yang dimainkan sepanjang tahun.")

# === KONTEN TAB 3: ANALISIS UPSET & ODDS ===
with tab3:
    st.header("Analisis Upset dan Odds (Peluang)")
    st.markdown("Menganalisis frekuensi kemenangan tak terduga (upset) dan hubungannya dengan odds.")

    # KPI Khusus untuk Tab ini
    col_upset_1, col_upset_2 = st.columns(2)
    with col_upset_1:
        st.metric("Total Upset Terjadi", f"{data_filtered['upset'].sum():,}")
    with col_upset_2:
        st.metric("Rata-rata Odds Gap", f"{data_filtered['odds_gap'].mean():.2f}")

    st.markdown("---")

    # Grafik Line Chart Tren Upset Tahunan
    st.subheader("Tren Upset Rate dari Tahun ke Tahun")
    
    # Hanya jalankan jika 'Semua Tahun' dipilih
    if selected_year == "Semua Tahun":
        # Hitung rata-rata upset per tahun
        upset_trend = data[data['Surface'].isin(selected_surface)].groupby('year')['upset'].mean().reset_index()
        upset_trend.columns = ['Year', 'Upset Rate']

        # Grafik Garis dengan Plotly
        fig_line = px.line(
            upset_trend,
            x='Year',
            y='Upset Rate',
            title="Fluktuasi Upset Rate Tahunan",
            labels={'Year': 'Tahun', 'Upset Rate': 'Rata-rata Upset Rate'},
            markers=True # Tampilkan titik di setiap tahun
        )
        fig_line.update_layout(yaxis_tickformat='.0%') # Format Y-axis sebagai persentase
        st.plotly_chart(fig_line, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan apakah tenis menjadi lebih atau kurang dapat diprediksi dari waktu ke waktu. Gunakan filter 'Jenis Lapangan' untuk melihat tren di lapangan tertentu.")
    else:
        st.warning(f"Grafik tren tahunan hanya dapat ditampilkan jika Anda memilih 'Semua Tahun' di filter sidebar. (Anda sedang memilih {selected_year})")


# === KONTEN TAB 4: EXPLORE DATA ===
with tab4:
    st.header("Jelajahi Data Mentah")
    st.markdown("Lihat data yang telah difilter dalam format tabel.")
    
    # Gunakan st.expander agar tidak memakan tempat
    with st.expander("Tampilkan Data (sesuai filter)", expanded=False):
        st.dataframe(data_filtered)
        
    st.markdown(f"Menampilkan **{data_filtered.shape[0]:,} baris** dari **{data.shape[0]:,} total baris**.")
