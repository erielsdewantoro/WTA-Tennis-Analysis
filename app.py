# --- IMPORTS ---
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="WTA Tennis Analysis Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS KUSTOM
st.markdown("""
    <style>
    .stApp [data-testid="stHeader"] {
        font-size: 3rem; font-weight: 700; padding-top: 1rem;
    }
    .stApp h2 { font-weight: 600; }
    /* Memperkecil font di dalam selectbox H2H & Player Profile */
    .stSelectbox div[data-baseweb="select"] > div {
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CACHING DATA
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Pastikan kolom tanggal adalah datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Membuat satu daftar pemain unik untuk filter H2H & Profil
    all_players = pd.concat([data['Player_1'], data['Player_2']]).dropna().unique()
    all_players.sort()
    return data, all_players

try:
    data, all_players = load_data('wta_processed.csv') 
except FileNotFoundError:
    st.error("File 'wta_processed.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()
except Exception as e:
    st.error(f"Terjadi error saat memuat data: {e}. Pastikan file 'wta_processed.csv' Anda memiliki kolom 'Date', 'Player_1', dan 'Player_2'.")
    st.stop()

# 4. JUDUL UTAMA
st.title("🏆 WTA Tennis Match Analysis")
st.markdown("Dashboard interaktif untuk menganalisis **42,000+** pertandingan tenis WTA (2006-2025).")

# 5. SIDEBAR (FILTER UTAMA)
st.sidebar.header("Filter Data Global 📊")
st.sidebar.markdown("Filter ini memengaruhi **semua tab** kecuali 'Analisis H2H' dan 'Deep Dive Pemain'.")
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
tab_titles = [
    "Dashboard Utama 📈", 
    "Analisis Lapangan 🏟️", 
    "Upset & Odds 🎾", 
    "Jelajahi Data 📊",
    "Analisis H2H 🆚",
    "Deep Dive Pemain 🧑‍"  # --- TAB BARU V5.0 ---
]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_titles)

# === KONTEN TAB 1: DASHBOARD UTAMA ===
with tab1:
    st.header("Gambaran Umum Performa")
    st.markdown("Metrik performa kunci berdasarkan filter yang Anda pilih.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Pertandingan", f"{data_filtered.shape[0]:,}")
    with col2: st.metric("Pemain Unik", data_filtered['Winner'].nunique())
    with col3: st.metric("Rata-rata Set", f"{data_filtered['sets_played'].mean():.2f}")
    with col4: st.metric("Upset Rate", f"{data_filtered['upset'].mean() * 100:.1f}%")

    st.markdown("---")
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.subheader("Top 10 Pemain dengan Kemenangan Terbanyak")
        top_10_winners = data_filtered['Winner'].value_counts().head(10).reset_index()
        top_10_winners.columns = ['Player', 'Total Wins']
        fig_bar = px.bar(top_10_winners, x='Total Wins', y='Player', orientation='h', title="Top 10 Pemain Pemenang", labels={'Player': 'Pemain', 'Total Wins': 'Jumlah Kemenangan'}, text='Total Wins')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan pemain paling dominan. Gunakan filter tahun untuk melihat siapa yang mendominasi di tahun tertentu.")

    with col_kanan:
        st.subheader("Distribusi Pertandingan per Babak")
        round_distribution = data_filtered['Round'].value_counts().reset_index()
        round_distribution.columns = ['Round', 'Count']
        fig_pie = px.pie(round_distribution, names='Round', values='Count', title="Persentase Pertandingan per Babak", hole=0.4)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info("💡 **Insight:** Seperti yang terlihat, sebagian besar pertandingan terjadi di babak-babak awal turnamen.")

# === KONTEN TAB 2: ANALISIS LAPANGAN ===
with tab2:
    st.header("Analisis Performa Berdasarkan Jenis Lapangan")
    st.markdown("Bagaimana jenis lapangan (Surface) memengaruhi hasil pertandingan?")
    surface_wins = data_filtered['Surface'].value_counts().reset_index()
    surface_wins.columns = ['Surface', 'Total Matches']
    fig_surface = px.bar(surface_wins, x='Surface', y='Total Matches', title="Jumlah Pertandingan per Jenis Lapangan", labels={'Surface': 'Jenis Lapangan', 'Total Matches': 'Jumlah Pertandingan'}, color='Surface')
    st.plotly_chart(fig_surface, use_container_width=True)
    st.info("💡 **Insight:** Lapangan 'Hard' jelas mendominasi jumlah turnamen yang dimainkan sepanjang tahun.")

# === KONTEN TAB 3: ANALISIS UPSET & ODDS ===
with tab3:
    st.header("Analisis Upset dan Odds (Peluang)")
    st.markdown("Menganalisis frekuensi kemenangan tak terduga (upset) dan hubungannya dengan odds.")
    
    col_upset_1, col_upset_2 = st.columns(2)
    with col_upset_1: st.metric("Total Upset Terjadi", f"{data_filtered['upset'].sum():,}")
    with col_upset_2: st.metric("Rata-rata Odds Gap", f"{data_filtered['odds_gap'].mean():.2f}")

    st.markdown("---")
    st.subheader("Tren Upset Rate dari Tahun ke Tahun")
    
    if selected_year == "Semua Tahun":
        upset_trend = data[data['Surface'].isin(selected_surface)].groupby('year')['upset'].mean().reset_index()
        upset_trend.columns = ['Year', 'Upset Rate']
        fig_line = px.line(upset_trend, x='Year', y='Upset Rate', title="Fluktuasi Upset Rate Tahunan", labels={'Year': 'Tahun', 'Upset Rate': 'Rata-rata Upset Rate'}, markers=True)
        fig_line.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_line, use_container_width=True)
        st.info("💡 **Insight:** Grafik ini menunjukkan apakah tenis menjadi lebih atau kurang dapat diprediksi dari waktu ke waktu.")
    else:
        st.warning(f"Grafik tren tahunan hanya dapat ditampilkan jika Anda memilih 'Semua Tahun' di filter sidebar. (Anda sedang memilih {selected_year})")

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
    st.markdown("*(Filter sidebar tidak berlaku di tab ini)*")

    col1, col2 = st.columns(2)
    with col1:
        player_a = st.selectbox("Pilih Pemain A", all_players, index=None, placeholder="Ketik nama pemain...", key="h2h_player_a")
    with col2:
        player_b = st.selectbox("Pilih Pemain B", all_players, index=None, placeholder="Ketik nama pemain...", key="h2h_player_b")

    if player_a and player_b and (player_a != player_b):
        st.markdown("---")
        h2h_data_1 = data[ (data['Player_1'] == player_a) & (data['Player_2'] == player_b) ]
        h2h_data_2 = data[ (data['Player_1'] == player_b) & (data['Player_2'] == player_a) ]
        h2h_data = pd.concat([h2h_data_1, h2h_data_2]).sort_values(by='Date')

        if h2h_data.empty:
            st.warning(f"Tidak ditemukan riwayat pertandingan antara **{player_a}** dan **{player_b}** dalam dataset.")
        else:
            total_matches = h2h_data.shape[0]
            wins_a = h2h_data[h2h_data['Winner'] == player_a].shape[0]
            wins_b = h2h_data[h2h_data['Winner'] == player_b].shape[0]

            st.subheader(f"Rekor Pertemuan: {player_a} vs {player_b}")
            
            col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)
            col_kpi_1.metric("Total Pertemuan", total_matches)
            col_kpi_2.metric(f"Kemenangan {player_a}", wins_a)
            col_kpi_3.metric(f"Kemenangan {player_b}", wins_b)

            st.subheader("Kemenangan Berdasarkan Jenis Lapangan")
            wins_by_surface = h2h_data.groupby('Surface')['Winner'].value_counts().unstack(fill_value=0).reset_index()
            
            if player_a not in wins_by_surface.columns: wins_by_surface[player_a] = 0
            if player_b not in wins_by_surface.columns: wins_by_surface[player_b] = 0

            wins_by_surface_long = pd.melt(wins_by_surface, id_vars=['Surface'], value_vars=[player_a, player_b], var_name='Player', value_name='Wins')

            fig_h2h_surface = px.bar(wins_by_surface_long, x='Surface', y='Wins', color='Player', barmode='group', title=f"Distribusi Kemenangan H2H di Berbagai Lapangan", labels={'Surface': 'Jenis Lapangan', 'Wins': 'Jumlah Kemenangan'})
            st.plotly_chart(fig_h2h_surface, use_container_width=True)
            
            st.subheader("Detail Riwayat Pertandingan")
            st.dataframe(h2h_data[['Date', 'Tournament', 'Surface', 'Round', 'Winner', 'Score', 'upset', 'odds_gap']])
            st.info(f"💡 **Insight:** Tabel di atas menunjukkan siapa yang menang, di mana, dan apakah kemenangan itu 'upset' (nilai 1) atau tidak (nilai 0).")

    elif player_a and player_b and (player_a == player_b):
        st.error("Anda harus memilih dua pemain yang berbeda.")
    else:
        st.info("Silakan pilih dua pemain dari menu di atas untuk memulai analisis H2H.")

# === KONTEN TAB 6: DEEP DIVE PEMAIN (BARU!) ===
with tab6:
    st.header("Deep Dive Pemain 🧑‍")
    st.markdown("Pilih satu pemain untuk menganalisis statistik karier, performa di berbagai lapangan, dan riwayat pertandingan. Alat ini dirancang untuk **Coach**, **Agen**, dan **Brand**.")
    st.markdown("*(Filter sidebar tidak berlaku di tab ini)*")

    # Filter Pemain Tunggal
    player_to_analyze = st.selectbox(
        "Pilih Pemain untuk Dianalisis", 
        all_players, 
        index=None, 
        placeholder="Ketik nama pemain untuk memulai...", 
        key="player_profile_select"
    )

    if player_to_analyze:
        st.markdown("---")
        
        # Filter semua data untuk pemain ini
        player_data = data[
            (data['Player_1'] == player_to_analyze) | (data['Player_2'] == player_to_analyze)
        ].copy()
        
        if player_data.empty:
            st.warning(f"Tidak ada data pertandingan untuk **{player_to_analyze}**.")
        else:
            # Hitung KPI Utama
            total_matches_player = player_data.shape[0]
            player_wins_data = player_data[player_data['Winner'] == player_to_analyze]
            total_wins_player = player_wins_data.shape[0]
            win_rate_player = total_wins_player / total_matches_player
            
            try:
                favorite_surface = player_wins_data['Surface'].mode()[0]
            except KeyError:
                favorite_surface = "N/A" # Jika pemain belum pernah menang

            st.subheader(f"Statistik Karier: {player_to_analyze}")
            
            # Tampilkan KPI
            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            col_kpi1.metric("Total Pertandingan (di dataset)", total_matches_player)
            col_kpi2.metric("Total Kemenangan", total_wins_player)
            col_kpi3.metric("Win Rate Keseluruhan", f"{win_rate_player:.1%}")

            st.markdown("---")
            
            # Baris 2: Visual Performa
            col_vis1, col_vis2 = st.columns(2)
            
            with col_vis1:
                # Visual 1: Kemenangan per Jenis Lapangan
                st.subheader("Distribusi Kemenangan per Jenis Lapangan")
                wins_by_surface_player = player_wins_data['Surface'].value_counts().reset_index()
                wins_by_surface_player.columns = ['Surface', 'Wins']
                
                fig_surface_player = px.pie(
                    wins_by_surface_player, 
                    names='Surface', 
                    values='Wins', 
                    title="Persentase Kemenangan per Lapangan",
                    hole=0.4
                )
                fig_surface_player.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_surface_player, use_container_width=True)
                st.info("💡 **Insight:** Grafik ini menunjukkan di lapangan mana pemain ini paling 'jago' atau paling sering menang.")

            with col_vis2:
                # Visual 2: Tren Kemenangan per Tahun
                st.subheader("Tren Kemenangan per Tahun")
                wins_per_year = player_wins_data.groupby('year')['Winner'].count().reset_index()
                wins_per_year.columns = ['Year', 'Total Wins']
                
                fig_year_player = px.line(
                    wins_per_year,
                    x='Year',
                    y='Total Wins',
                    title="Fluktuasi Kemenangan Tahunan",
                    labels={'Year': 'Tahun', 'Total Wins': 'Jumlah Kemenangan'},
                    markers=True
                )
                st.plotly_chart(fig_year_player, use_container_width=True)
                st.info("💡 **Insight:** Grafik ini menunjukkan puncak performa pemain dan tren kariernya dari tahun ke tahun.")
            
            # Baris 3: Riwayat Pertandingan Terakhir
            st.subheader("Riwayat 20 Pertandingan Terakhir")
            st.markdown("Tabel ini menunjukkan performa terbaru pemain.")
            recent_matches = player_data.sort_values(by='Date', ascending=False).head(20)
            
            # Menambahkan kolom 'Result' agar mudah dibaca
            recent_matches['Result'] = recent_matches.apply(
                lambda row: "Win" if row['Winner'] == player_to_analyze else "Loss", 
                axis=1
            )
            
            st.dataframe(recent_matches[[
                'Date', 'Tournament', 'Round', 'Surface', 'Player_1', 'Player_2', 'Result', 'Score', 'upset'
            ]])
            st.info("💡 **Insight:** Gunakan tabel ini untuk *scouting*. Cek performa terbaru, skor, dan apakah mereka sering terlibat dalam pertandingan *upset*.")
            
    else:
        st.info("Silakan pilih seorang pemain untuk memulai analisis mendalam.")
