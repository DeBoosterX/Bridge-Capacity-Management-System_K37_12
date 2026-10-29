# 🌉 Simulasi Manajemen Kapasitas Jembatan (BCMS)

Repository ini dibuat dalam rangka memenuhi Tugas Besar mata kuliah Berpikir Komputasional WI1102 di Institut Teknologi Bandung. Kelompok kami terdiri dari:

*   Muhammad Alif Fahmi Jati (19626137)
*   Muhammad Hisyam M.R. Arisyi (16526029)
*   Beryl Raditya Ahmad (16526131)
*   Fawwaz Muhammad Zaahiy (19626029)
*   Tristan Pudyameka Sakti (19626101)

## 📖 Deskripsi Program

Secara umum, program ini akan mensimulasikan manajemen kapasitas beban lalu lintas pada sebuah jembatan secara *real-time*. Pengguna dapat memasukkan spesifikasi jembatan (kapasitas, panjang, dan kesehatan awal), lalu sistem akan memunculkan kendaraan secara acak (motor, mobil, truk) yang melintas dari dua arah. 

Program ini dibangun utamanya menggunakan paradigma *Object-Oriented Programming* (OOP), logika *Finite State Machine* (FSM), perulangan `while`, fungsi (`def`), logika-dasar (`if-else`), serta mengimpor beberapa modul bawaan Python seperti `os`, `time`, dan `random`. Program ini juga memanfaatkan library `rich` untuk merender antarmuka terminal.

## ✨ Kemampuan Program

Program ini memiliki beberapa kemampuan utama, di antaranya:

*   **Simulasi Stokastik:** Mensimulasikan kedatangan kendaraan secara acak dengan bobot dan jenis yang bervariasi.
*   **Heuristik Fisika:** Menghitung akumulasi beban dinamis dengan menerapkan prinsip momen lentur (beban di area tengah jembatan dianggap lebih berat).
*   **Degradasi Material (Fatigue):** Memantau dan mengurangi tingkat kesehatan struktur jembatan secara bertahap seiring berjalannya waktu.
*   **Sistem Peringatan Dini:** Memberikan peringatan dengan mengubah status jembatan (Normal, Waspada, Kritis) berdasarkan persentase beban saat ini.
*   **Palang Preventif (Hysteresis):** Mengoperasikan palang otomatis yang hanya terbuka jika beban turun drastis, serta dilengkapi fitur penutupan permanen jika jembatan dinyatakan runtuh.
*   **Interactive CLI:** Menampilkan visualisasi antarmuka terminal yang interaktif, berwarna, dan beranimasi mulus tanpa kedipan layar.
