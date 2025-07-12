import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========== BACA DATA ==========
file_path = "MINANGKABAU.xlsx"
df = pd.read_excel(file_path)

# Membersihkan nama kolom
df.columns = df.columns.str.strip()

# Rename kolom (ubah sesuai isi file Anda)
rename_map = {
    "Tavg": "Suhu",
    "RR": "Curah_Hujan",
    "Tx": "Suhu_Max",
    "Tn": "Suhu_Min"
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# Hitung rentang & anomali suhu
df["Rentang_Suhu"] = df["Suhu_Max"] - df["Suhu_Min"]
baseline = df[(df["Tahun"] >= 1985) & (df["Tahun"] <= 2023)]["Suhu"].mean()
df["Anomali_Suhu"] = df["Suhu"] - baseline

# ========== DASHBOARD ==========
st.set_page_config(page_title="Dashboard Iklim Sumatera Barat", layout="wide")
st.title("🌤️ Dashboard Analisis Iklim Provinsi Sumatera Barat")
st.markdown("Visualisasi data iklim tahunan berdasarkan suhu, curah hujan, dan parameter lainnya.")

# Tampilkan tabel
st.subheader("📄 Data Iklim Tahunan")
st.dataframe(df)

# Grafik tren suhu
st.subheader("🌡️ Tren Suhu Rata-rata Tahunan")
st.line_chart(df.set_index("Tahun")["Suhu"])

# Curah hujan
st.subheader("🌧️ Curah Hujan Tahunan")
st.bar_chart(df.set_index("Tahun")["Curah_Hujan"])

# Rentang suhu
st.subheader("📉 Rentang Suhu (Max - Min)")
st.line_chart(df.set_index("Tahun")["Rentang_Suhu"])

# Anomali suhu
st.subheader("📈 Anomali Suhu terhadap Rata-rata 1985–2023")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(x="Tahun", y="Anomali_Suhu", data=df, palette="coolwarm", ax=ax1)
ax1.axhline(0, color="black", linestyle="--")
ax1.set_ylabel("Anomali (°C)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Korelasi suhu dan hujan
st.subheader("🔍 Korelasi Suhu vs Curah Hujan")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="Suhu", y="Curah_Hujan", ax=ax2)
sns.regplot(data=df, x="Suhu", y="Curah_Hujan", scatter=False, color="red", ax=ax2)
st.pyplot(fig2)

# Rata-rata per dekade
st.subheader("📊 Rata-rata Suhu & Curah Hujan per Dekade")
df["Dekade"] = (df["Tahun"] // 10) * 10
avg_dekade = df.groupby("Dekade")[["Suhu", "Curah_Hujan"]].mean().round(2)
st.dataframe(avg_dekade)
fig3, ax3 = plt.subplots()
avg_dekade.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Rata-rata")
st.pyplot(fig3)

# Tahun ekstrem
st.subheader("📌 Tahun Ekstrem")
st.markdown(f"""
- 🌡️ **Tahun Terpanas**: {df.loc[df['Suhu'].idxmax()]['Tahun']} ({df['Suhu'].max():.2f} °C)  
- ❄️ **Tahun Terdingin**: {df.loc[df['Suhu'].idxmin()]['Tahun']} ({df['Suhu'].min():.2f} °C)  
- 🌧️ **Hujan Terbanyak**: {df.loc[df['Curah_Hujan'].idxmax()]['Tahun']} ({df['Curah_Hujan'].max():.1f} mm)  
- ☀️ **Hujan Terkering**: {df.loc[df['Curah_Hujan'].idxmin()]['Tahun']} ({df['Curah_Hujan'].min():.1f} mm)
""")

# Kelembaban
if "kelembaban" in df.columns:
    st.subheader("💧 Distribusi Kelembaban Tahunan")
    fig4, ax4 = plt.subplots()
    sns.histplot(df["kelembaban"], kde=True, bins=20, color="skyblue", ax=ax4)
    st.pyplot(fig4)
    st.subheader("💨 Tren Kelembaban Tahunan")
    st.line_chart(df.set_index("Tahun")["kelembaban"])

# Matahari
if "matahari" in df.columns:
    st.subheader("🌞 Durasi Penyinaran Matahari")
    st.line_chart(df.set_index("Tahun")["matahari"])

# Kecepatan angin
if "kecepatan_angin" in df.columns:
    st.subheader("🍃 Kecepatan Angin Tahunan")
    st.line_chart(df.set_index("Tahun")["kecepatan_angin"])

# Tekanan udara
if "Tekanan" in df.columns:
    st.subheader("🧭 Tekanan Udara Tahunan")
    st.line_chart(df.set_index("Tahun")["Tekanan"])

# Korelasi antar variabel
st.subheader("📌 Korelasi Antar Variabel Iklim")
fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)
