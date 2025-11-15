import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="WTA Tennis Match Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS KUSTOM (DARI V3.0)
st.markdown("""
    <style>
    .stApp [data-testid="stHeader"] {
        font-size: 3rem; font-weight: 700; padding-top: 1rem;
    }
    .stApp h2 { font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 3. CACHING DATA
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Membuat satu daftar pemain unik untuk filter H2H
    all_players = pd.concat([data['Player_1'], data['Player_2']]).unique()
    all_players.sort()
    return data, all_players

try:
    # Perhatikan, kita sekarang memuat data DAN daftar pemain
    data, all_players = load_data('wta_processed.csv') 
except FileNotFoundError:
    st.error("File 'wta_processed.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()
except Exception as e:
    st.error(f"Terjadi error saat memuat data: {e}")
    st.stop()

# 4. JUDUL UTAMA
st.title("🏆 WTA Tennis Match Analysis")
st.markdown("Dashboard interaktif untuk menganalisis **42,000+** pertandingan tenis WTA (2006-2025).")

# 5. SIDEBAR (FILTER UTAMA)
st.sidebar.header("Filter Data Global 📊")
unique_years = sorted(data['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + unique_years)
unique_surfaces = sorted(data['Surface'].unique())
selected_surface = st.sidebar.multiselect("Pilih Jenis Lapangan", unique_surfaces, default=unique_surfaces)

# 6. TERAPKAN FILTER KE DATA
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

# 7. KONTEN UTAMA DENGAN TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard Utama 📈", 
    "Analisis Lapangan 🏟️", 
    "Upset & Odds 🎾", 
    "Jelajahi Data 📊",
    "Analisis Head-to-Head (H2H) 🆚"  # --- TAB BARU V4.0 ---
])

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
        st.warning(f"Grafik tren tahunan only dapat ditampilkan jika Anda memilih 'Semua Tahun' di filter sidebar. (Anda sedang memilih {selected_year})")

# === KONTEN TAB 4: EXPLORE DATA ===
with tab4:
    st.header("Jelajahi Data Mentah")
    st.markdown("Lihat data yang telah difilter dalam format tabel.")
    with st.expander("Tampilkan Data (sesuai filter)", expanded=False):
        st.dataframe(data_filtered)
    st.markdown(f"Menampilkan **{data_filtered.shape[0]:,} baris** dari **{data.shape[0]:,} total baris**.")

# === KONTEN TAB 5: HEAD-TO-HEAD (H2H) ===
with tab5:
    st.header("Analisis Head-to-Head (H2H) 🆚")
    st.markdown("Pilih dua pemain untuk melihat riwayat pertemuan mereka. Fitur ini menjawab kebutuhan **Coach**, **Player**, dan **Media**.")

    col1, col2 = st.columns(2)
    with col1:
        player_a = st.selectbox("Pilih Pemain A", all_players, index=None, placeholder="Ketik nama pemain...")
    with col2:
        player_b = st.selectbox("Pilih Pemain B", all_players, index=None, placeholder="Ketik nama pemain...")

    if player_a and player_b and (player_a != player_b):
        st.markdown("---")
        
        # Logika Filter H2H
        h2h_data_1 = data[
            (data['Player_1'] == player_a) & (data['Player_2'] == player_b)
        ]
        h2h_data_2 = data[
            (data['Player_1'] == player_b) & (data['Player_2'] == player_a)
        ]
        
        h2h_data = pd.concat([h2h_data_1, h2h_data_2]).sort_values(by='Date')

        if h2h_data.empty:
            st.warning(f"Tidak ditemukan riwayat pertandingan antara **{player_a}** dan **{player_b}** dalam dataset.")
        else:
            # Tampilkan KPI H2H
            total_matches = h2h_data.shape[0]
            wins_a = h2h_data[h2h_data['Winner'] == player_a].shape[0]
            wins_b = h2h_data[h2h_data['Winner'] == player_b].shape[0]

            st.subheader(f"Rekor Pertemuan: {player_a} vs {player_b}")
            
            col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)
            col_kpi_1.metric("Total Pertemuan", total_matches)
            col_kpi_2.metric(f"Kemenangan {player_a}", wins_a)
            col_kpi_3.metric(f"Kemenangan {player_b}", wins_b)

            # Visualisasi: Kemenangan Berdasarkan Lapangan (Surface)
            st.subheader("Kemenangan Berdasarkan Jenis Lapangan")
            wins_by_surface = h2h_data.groupby('Surface')['Winner'].value_counts().unstack(fill_value=0).reset_index()
            
            if player_a not in wins_by_surface.columns:
                wins_by_surface[player_a] = 0
            if player_b not in wins_by_surface.columns:
                wins_by_surface[player_b] = 0

            wins_by_surface_long = pd.melt(wins_by_surface, id_vars=['Surface'], value_vars=[player_a, player_b], var_name='Player', value_name='Wins')

            fig_h2h_surface = px.bar(
                wins_by_surface_long,
                x='Surface',
                y='Wins',
                color='Player',
                barmode='group',
                title=f"Distribusi Kemenangan H2H di Berbagai Lapangan",
                labels={'Surface': 'Jenis Lapangan', 'Wins': 'Jumlah Kemenangan'}
            )
            st.plotly_chart(fig_h2h_surface, use_container_width=True)
            
            # Menjawab feedback "jago di lapangan apa, underdog apa engga"
            st.subheader("Detail Riwayat Pertandingan")
            st.dataframe(h2h_data[[
                'Date', 'Tournament', 'Surface', 'Round', 'Winner', 'Score', 'upset', 'odds_gap'
            ]])
            st.info(f"💡 **Insight:** Tabel di atas menunjukkan siapa yang menang, di mana, dan apakah kemenangan itu 'upset' (nilai 1) atau tidak (nilai 0).")

    elif player_a and player_b and (player_a == player_b):
        st.error("Anda harus memilih dua pemain yang berbeda.")
    else:
        st.info("Silakan pilih dua pemain dari menu di atas untuk memulai analisis H2H.")
