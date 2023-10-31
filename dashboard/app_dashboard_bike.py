import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Dataset
merged_df = pd.read_csv('https://raw.githubusercontent.com/DjulF31/Project_Bike_Sharing_dataset/2edbde7b02ddaafd5b5e7678a48860ef49a2961f/Bike-dataset/merged_dataset.csv')
dataset_selection = st.radio("Pilih Dataset Yang Akan Dilihat :", ["hour_df", "day_df"])

# Side Filter Tanggal 
min_date = pd.to_datetime(merged_df["dteday"].min()).date()
max_date = pd.to_datetime(merged_df["dteday"].max()).date()

def on_change():
    st.write("Nilai date_input berubah:", start_date, end_date)

st.sidebar.image("https://raw.githubusercontent.com/DjulF31/Project_Bike_Sharing_dataset/2edbde7b02ddaafd5b5e7678a48860ef49a2961f/Bike-dataset/Bike.png")
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# --- Jawaban No.1 ---
if dataset_selection == "hour_df":
    file_name = 'https://raw.githubusercontent.com/DjulF31/Project_Bike_Sharing_dataset/2edbde7b02ddaafd5b5e7678a48860ef49a2961f/Bike-dataset/hour.csv' 
    dataset_name = "hour_df"
elif dataset_selection == "day_df":
    file_name = 'https://raw.githubusercontent.com/DjulF31/Project_Bike_Sharing_dataset/2edbde7b02ddaafd5b5e7678a48860ef49a2961f/Bike-dataset/day.csv' 
    dataset_name = "day_df"

# Memuat data dari file CSV yang sesuai
data_df = pd.read_csv(file_name)
monthly_avg = data_df.groupby('mnth')['cnt'].mean()
monthly_weather_avg = data_df.groupby(['mnth', 'weathersit'])['cnt'].mean().unstack()

# Mulai Visualisasi
st.title(f"Analisis Bike Sharing Dataset {dataset_selection}")

# Analisis Bulan
st.header("Analisis Bulan")
st.write("Rata-rata Jumlah Peminjaman Sepeda per Bulan:")
st.write(monthly_avg)

# Visualisasi Data
st.header("Visualisasi Data")
st.write("Bar Plot Rata-rata Jumlah Peminjaman Sepeda per Bulan")
plt.figure(figsize=(8, 6))
monthly_avg.plot(kind='bar', color='skyblue')
plt.title('Rata-rata Jumlah Peminjaman Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda (cnt)')
plt.grid(axis='y')
st.pyplot(plt)

plt.figure(figsize=(12, 6))
monthly_weather_avg.plot(kind='bar', width=0.8, cmap='coolwarm')
plt.title(f'Rata-rata Jumlah Peminjaman Sepeda per Bulan berdasarkan Kondisi Cuaca ')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda (cnt)')
plt.legend(['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Berat'], loc='upper left')
plt.grid(axis='y')

st.pyplot(plt)

# Menemukan Bulan dengan Jumlah Terbanyak
bulan_terbanyak = monthly_avg.idxmax()
jumlah_terbanyak = monthly_avg.max()
st.write(f"Bulan dengan Jumlah Peminjaman Sepeda Terbanyak (cnt): {bulan_terbanyak}")
st.write(f"Jumlah Peminjaman Terbanyak (cnt) pada Bulan Tersebut: {jumlah_terbanyak}")

# Kesimpulan
st.header("Kesimpulan")
st.write(f"Berdasarkan analisis dataset {dataset_selection}, bulan dengan jumlah sepeda yang paling banyak dipinjam (cnt) adalah bulan {bulan_terbanyak}.")
st.write("========================================================================================")

# --- Jawaban No.2 ---
if dataset_selection == "hour_df":
    st.write("Silakan pilih dataset 'day_df' untuk melihat analisis Apakah musim (season) mempengaruhi rata-rata penggunaan sepeda ?")
else:
    # Statistik Deskriptif untuk "cnt" berdasarkan musim
    day_stats = data_df.groupby('season')['cnt'].agg(['mean', 'count'])
    st.write("Rata-rata Penggunaan Sepeda (cnt) berdasarkan Musim:")
    st.write(day_stats)

    # Hitung rata-rata jumlah peminjaman sepeda per musim
    seasonal_avg = data_df.groupby('season')['cnt'].mean()

    # Plot bar diagram untuk rata-rata jumlah peminjaman sepeda per musim
    plt.figure(figsize=(8, 6))
    seasonal_avg.plot(kind='bar', color='lightcoral')
    plt.title(f'Rata-rata Jumlah Peminjaman Sepeda per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda (cnt)')
    plt.xticks(range(4), ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], rotation=0)
    plt.grid(axis='y')

    st.pyplot(plt)

    st.header("Kesimpulan")
    st.write(f"Hasil menunjukkan bahwa musim atau season, mempengaruhi rata-rata penjumlah pengendara atau pinjaman per musim mungkin dipengaruhi oleh event atau lain sebagainya tetapi pada musim ke-2 hingga ke-4, ada peningkatan yang signifikan jika ada yang mengalami penurunan tidak ada penurunan yang signifikan.")