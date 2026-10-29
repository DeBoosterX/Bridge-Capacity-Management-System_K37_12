Repository ini dibuat dalam rangka memenuhi Tugas Besar mata kuliah Berpikir Komputasional. Kelompok kami terdiri dari

Muhammad Alif Fahmi Jati (19626137)
Muhammad Hisyam M.R. Arisyi (16526029)
Beryl Raditya Ahmad (16526131)
Fawwaz Muhammad Zaahiy (19626029)
Tristan Pudyameka Sakti (19626101)

Secara umum, program ini akan mensimulasikan manajemen kapasitas beban lalu lintas pada sebuah jembatan secara real-time. Pengguna dapat memasukkan spesifikasi jembatan (kapasitas, panjang, dan kesehatan awal), lalu sistem akan memunculkan kendaraan secara acak (motor, mobil, truk) yang melintas dari dua arah. Program ini dibangun utamanya menggunakan paradigma Object-Oriented Programming (OOP), logika Finite State Machine (FSM), perulangan while, fungsi (def), logika-dasar (if-else), serta mengimpor beberapa modul bawaan Python seperti os, time, dan random, dan memanfaatkan library rich untuk antarmuka terminal. Program ini memiliki beberapa kemampuan, diantaranya :

Mensimulasikan kedatangan kendaraan secara stokastik (acak) dengan bobot yang bervariasi.
Menghitung akumulasi beban dinamis dengan menerapkan heuristik fisika momen lentur (beban di tengah jembatan lebih berat).
Memantau dan mengurangi tingkat kesehatan struktur (fatigue) jembatan seiring berjalannya waktu.
Memberikan peringatan dini dengan mengubah status jembatan (Normal, Waspada, Kritis) berdasarkan persentase beban.
Mengoperasikan palang preventif otomatis (hysteresis) yang hanya terbuka jika beban turun drastis, serta fitur tutup permanen jika jembatan runtuh.
Menampilkan visualisasi antarmuka CLI yang interaktif, berwarna, dan beranimasi tanpa kedipan layar.
