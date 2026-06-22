import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fuzzy Penilaian Mahasiswa", page_icon="🎓", layout="wide")

def nilai_rendah(x):
    if x <= 40:
        return 1.0
    elif x < 60:
        return (60 - x) / 20
    return 0.0

def nilai_sedang(x):
    if x <= 40 or x >= 80:
        return 0.0
    elif x < 60:
        return (x - 40) / 20
    elif x == 60:
        return 1.0
    return (80 - x) / 20

def nilai_tinggi(x):
    if x <= 60:
        return 0.0
    elif x < 80:
        return (x - 60) / 20
    return 1.0

def kategori_dominan(rendah, sedang, tinggi):
    nilai_max = max(rendah, sedang, tinggi)
    if nilai_max == rendah:
        return "Rendah", "Mahasiswa perlu meningkatkan pemahaman materi dan latihan soal."
    elif nilai_max == sedang:
        return "Sedang", "Mahasiswa sudah cukup memahami materi, tetapi masih perlu belajar konsisten."
    return "Tinggi", "Mahasiswa memiliki hasil yang baik dan perlu mempertahankan prestasinya."

st.title("🎓 Logika Fuzzy: Penilaian Mahasiswa")
st.caption("Studi Kasus 1 - Input Nilai Ujian | Output: Rendah, Sedang, Tinggi")
st.markdown("---")

col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("📌 Input Nilai Ujian")
    nilai = st.slider("Masukkan nilai ujian mahasiswa", 0, 100, 75)

    rendah = nilai_rendah(nilai)
    sedang = nilai_sedang(nilai)
    tinggi = nilai_tinggi(nilai)

    kategori, interpretasi = kategori_dominan(rendah, sedang, tinggi)

    st.info(f"Nilai yang dimasukkan: **{nilai}**")

    df = pd.DataFrame({
        "Himpunan Fuzzy": ["Rendah", "Sedang", "Tinggi"],
        "Derajat Keanggotaan": [rendah, sedang, tinggi]
    })

    st.subheader("📊 Derajat Keanggotaan")
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📈 Grafik Fungsi Keanggotaan")

    x = np.linspace(0, 100, 101)
    y_rendah = [nilai_rendah(i) for i in x]
    y_sedang = [nilai_sedang(i) for i in x]
    y_tinggi = [nilai_tinggi(i) for i in x]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, y_rendah, label="Rendah", linewidth=2)
    ax.plot(x, y_sedang, label="Sedang", linewidth=2)
    ax.plot(x, y_tinggi, label="Tinggi", linewidth=2)

    ax.axvline(nilai, linestyle="--", linewidth=1.5, label=f"Nilai = {nilai}")
    ax.scatter([nilai], [rendah], s=70)
    ax.scatter([nilai], [sedang], s=70)
    ax.scatter([nilai], [tinggi], s=70)

    ax.set_title("Fungsi Keanggotaan Nilai Ujian")
    ax.set_xlabel("Nilai Ujian")
    ax.set_ylabel("μ(x)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    st.pyplot(fig)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🧮 Perhitungan Manual")
    st.latex(r"\mu_{rendah}(x)=\begin{cases}1, x\leq40\\\frac{60-x}{20}, 40<x<60\\0, x\geq60\end{cases}")
    st.latex(r"\mu_{sedang}(x)=\begin{cases}0, x\leq40\ atau\ x\geq80\\\frac{x-40}{20}, 40<x<60\\1, x=60\\\frac{80-x}{20}, 60<x<80\end{cases}")
    st.latex(r"\mu_{tinggi}(x)=\begin{cases}0, x\leq60\\\frac{x-60}{20}, 60<x<80\\1, x\geq80\end{cases}")

with col4:
    st.subheader("✅ Interpretasi Hasil")
    st.success(f"Kategori dominan: **{kategori}**")
    st.write(interpretasi)

    st.subheader("📋 Ringkasan")
    st.write(f"Nilai ujian **{nilai}** memiliki derajat keanggotaan:")
    st.write(f"- Rendah = **{rendah:.2f}**")
    st.write(f"- Sedang = **{sedang:.2f}**")
    st.write(f"- Tinggi = **{tinggi:.2f}**")

st.markdown("---")
st.caption("Dibuat menggunakan Streamlit")