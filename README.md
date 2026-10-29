**# 🌉 Bridge Capacity Management System (BCMS)

Sistem simulasi berbasis *Command Line Interface* (CLI) yang memodelkan manajemen beban lalu lintas pada sebuah jembatan secara *real-time*. Proyek ini dibangun menggunakan bahasa Python sebagai pemenuhan Tugas Besar mata kuliah **Berpikir Komputasional (WI1102) Institut Teknologi Bandung**.

## ✨ Fitur Utama

*   **Object-Oriented Programming (OOP):** Memisahkan logika kalkulasi (*Backend*) dengan antarmuka visual (*Frontend*), serta menerapkan prinsip enkapsulasi pada *state* jembatan.
*   **Finite State Machine (FSM):** Sistem peringatan dini dinamis yang mengubah status jembatan (NORMAL, WASPADA, KRITIS) berdasarkan ambang batas beban.
*   **Simulasi Fisika Heuristik:** 
    *   *Momen Lentur:* Beban kendaraan di area tengah jembatan dikalikan untuk merepresentasikan peningkatan tegangan struktural.
    *   *Fatigue (Kelelahan Material):* Kapasitas maksimal jembatan menurun secara bertahap seiring banyaknya kendaraan yang melintas.
*   **Palang Histeresis (Fail-Safe):** Logika preventif di mana palang hanya akan terbuka kembali jika beban turun drastis di bawah 50%, mencegah osilasi (buka-tutup berulang). Jika kesehatan struktur menyentuh 0, jembatan akan ditutup permanen.
*   **Interactive CLI Dashboard:** Visualisasi terminal yang mulus dan berwarna berkat pustaka `rich`, lengkap dengan *progress bar* dan animasi kendaraan (10 FPS).

## 🛠️ Prasyarat

Sebelum menjalankan program, pastikan Anda telah menginstal:
*   Python 3.x
*   Pustaka `rich` (dapat diinstal melalui langkah di bawah)

## 🚀 Cara Menjalankan Program

1. *Clone* repositori ini ke direktori lokal:
   ```bash
   git clone https://github.com/username-anda/bridge-capacity-sim.git
   cd bridge-capacity-sim**
