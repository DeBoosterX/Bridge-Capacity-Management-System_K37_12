#Bagian ini memuat pustaka (library) yang dibutuhkan. 
import time #Untuk mengatur kecepatan animasi (jeda)
import random #Untuk stimulasi angka acak
import os #Untuk membersihkan layar agar tampilan tidak menumpuk ke bawah
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text
#Rich untuk membuat tampilan terminal menjadi cantik dan beranimasi. Hanya menggunakan yang diperlukan.

# A. ALASAN MENGGUNAKAN OOP (Object-Oriented Programming):
# 1. Abstraksi: Memodelkan entitas fisik jembatan yang kompleks menjadi 
#    objek digital (Class) dengan atribut (beban, kapasitas) dan perilaku.
# 2. Enkapsulasi: Mengamankan data state (beban, kesehatan) agar tidak bisa 
#    diubah sembarangan dari luar, melainkan hanya melalui method internal.
# 3. Alasan tidak memakai Inheritance/Polymorphism: Untuk menjaga efisiensi 
#    dan kesederhanaan kode (KISS), karena kendaraan disimpan sebagai Dictionary.

# ==========================================
# CLASS JEMBATAN (LOGIKA INTI / BACKEND): Menerapkan OOP (Object-Oriented Programming)
# ==========================================
class Jembatan:
    #Konstruktor adalah fungsi pertama yang dijalankan saat objek dibuat.
    #Fungsi __init__ menerima input manual dari pengguna dan menyimpannya sebagai state (keadaan) awal.
    def __init__(self, nama, kapasitas_maks, panjang_meter, kesehatan_awal, batas_waspada, batas_kritis, faktor_momen, laju_fatigue):
        # 1. Spesifikasi
        #Menerima 8 parameter input dari pengguna dan menyimpannya sebagai atribut self.
        self.nama = nama
        self.kapasitas_maks = kapasitas_maks
        self.panjang_meter = panjang_meter
        self.kesehatan_struktur = kesehatan_awal 
        self.batas_waspada = batas_waspada
        self.batas_kritis = batas_kritis
        self.faktor_momen = faktor_momen
        self.laju_fatigue = laju_fatigue

        # 2. State
        self.beban_saat_ini = 0.0
        self.status = "NORMAL"
        self.warna_status = "green"
        self.palang_tertutup = False
        self.is_runtuh = False
        self.kendaraan_aktif = []
        self.kendaraan_ditolak = 0
        self.logs = ["[SISTEM] Simulasi dimulai."]

    #Algoritma Fixed-Size Bufer (Rolling Log) dengan menyimpan 3 log terakhir
    # secara bergantian agar layar terminal tidak dipenuhi teks
    def tambah_log(self, pesan):
        self.logs.insert(0, pesan)
        if len(self.logs) > 3:
            self.logs.pop()

    def update_fsm_dan_palang(self):
        # Logika Tutup Permanen 
        if self.kesehatan_struktur <= 0 and not self.is_runtuh:
            self.is_runtuh = True
            self.status = "RUNTUH"
            self.warna_status = "red"
            self.palang_tertutup = True
            self.tambah_log("💀 JEMBATAN RUNTUH! DITUTUP PERMANEN.")
            return # Langsung keluar, tidak perlu hitung FSM normal

        if self.is_runtuh:
            return # Jika sudah runtuh, hentikan evaluasi status

        #Menghitung kapasitas real-time seiring degradasi material.
        #Jika jembatan sudah tua/rusak (kesehatan_struktur rendah), kapasitas efektifnya menurun. 
        #Lalu dihitung persentase beban saat ini. Palang akan turun ketika sudah tidak aman.
        kapasitas_efektif = self.kapasitas_maks * (self.kesehatan_struktur / 100)
        persentase = (self.beban_saat_ini / kapasitas_efektif) * 100 if kapasitas_efektif > 0 else 100

        # 1. FSM (Finite State Machine): Perubahan status dan warna UI dipicu oleh ambang batas (threshold) persentase.
        if persentase >= self.batas_kritis:
            self.status = "KRITIS"
            self.warna_status = "red"
        elif persentase >= self.batas_waspada:
            self.status = "WASPADA"
            self.warna_status = "yellow"
        else:
            self.status = "NORMAL"
            self.warna_status = "green"

        # 2. Logika Hysteresis Palang: Palang turun jika kritis. Palang hanya akan naik jika beban turun drastis di bawah 50%. 
        if self.status == "KRITIS" and not self.palang_tertutup:
            self.palang_tertutup = True
            self.tambah_log("🚨 KRITIS! PALANG DITUTUP.")

        # Palang hanya buka jika < 50% (Aman)
        elif self.palang_tertutup and persentase < 50:
            self.palang_tertutup = False
            self.tambah_log("🟢 AMAN. PALANG DIBUKA.")

    #Jika kendaraan berada di 20% area tengah jembatan, berat aslinya dikalikan dengan faktor_momen (misal 1.5x). 
    #Jika di area pilar (pinggir), beratnya normal.
    #Momen Lentur (dan tegangan/stress) mencapai titik MAKSIMAL ketika beban berada tepat di tengah bentang.
    # Jika beban berada di dekat pilar (pinggir), momen lenturnya mendekati nol (beban langsung disalurkan ke tanah).
    def hitung_beban_fisika(self, berat_asli, posisi_meter):
        titik_tengah = self.panjang_meter / 2
        if abs(posisi_meter - titik_tengah) < (self.panjang_meter * 0.2):
            return berat_asli * self.faktor_momen
        return berat_asli

    #Hitung ulang beban total secara berkala lewat looping
    def hitung_ulang_total_beban(self):
        self.beban_saat_ini = sum(
            self.hitung_beban_fisika(k["berat"], k["posisi_meter"]) for k in self.kendaraan_aktif
        )
        self.update_fsm_dan_palang()

    def datang_kendaraan(self):
        #  Tolak semua kendaraan jika jembatan sudah runtuh
        if self.is_runtuh:
            self.kendaraan_ditolak += 1
            return

        #Jika palang sedang ditutup oleh sistem FSM, kendaraan yang datang otomatis ditolak dan dihitung.
        if self.palang_tertutup:
            self.kendaraan_ditolak += 1
            if random.random() < 0.2:  # Hanya log 20% dari total yang ditolak
                self.tambah_log("🚫 Kendaraan ditolak! Palang tertutup.")
            return

        # Probabilitas kedatangan 80%
        if random.random() < 0.8:
            jenis = random.choice(["Motor", "Mobil", "Truk"])
            #Data selang berat motor, mobil, dan truk didapat dari data berat tiap kendaraan di Indonesia
            if jenis == "Motor":
                berat = random.uniform(0.1, 0.3) 
            elif jenis == "Mobil":
                berat = random.uniform(1.5, 3.0)
            else:
                berat = random.uniform(10.0, 25.0)

            # Kendaraan akan berada di jalur mana?
            # Jalur A (0->100) atau B (100->0)
            jalur = random.choice(["A", "B"])
            posisi = 0.0 if jalur == "A" else self.panjang_meter

            self.kendaraan_aktif.append({"jenis": jenis, "berat": berat, "posisi_meter": posisi, "jalur": jalur})
            self.tambah_log(f"➕ {jenis} ({berat:.1f}t) masuk Jalur {jalur}.")

    def update_pergerakan(self):
        kecepatan = self.panjang_meter / 15  # Kendaraan butuh ~15 tick untuk menyeberang
        for k in self.kendaraan_aktif[:]:
            if k["jalur"] == "A":
                k["posisi_meter"] += kecepatan
            else:
                k["posisi_meter"] -= kecepatan

            # Jika keluar jembatan, kendaraan tidak dihitung lagi
            if (k["jalur"] == "A" and k["posisi_meter"] > self.panjang_meter) or \
                    (k["jalur"] == "B" and k["posisi_meter"] < 0):
                self.kendaraan_aktif.remove(k)
                # Kurangi kesehatan (Fatigue)
                self.kesehatan_struktur -= (k["berat"] / self.kapasitas_maks) * self.laju_fatigue
                if self.kesehatan_struktur < 0:
                    self.kesehatan_struktur = 0

        self.hitung_ulang_total_beban()


# ==========================================
# FUNGSI UI CLI (FRONTEND DENGAN RICH)
# ==========================================
LEBAR_LAYAR = 70  # Karakter visual


def buat_tampilan(j):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="metrik", size=5),
        Layout(name="visual", size=9),
        Layout(name="log", size=5)
    )

    # Header
    # <-- TAMBAHAN BARU: Ubah warna header jika runtuh -->
    header_style = "bold white on red" if j.is_runtuh else "bold white on blue"
    layout["header"].update(
        Panel(Text(f"🌉 BRIDGE MONITORING: {j.nama.upper()}", style=header_style, justify="center")))

    # Metrik
    prog_beban = Progress(TextColumn("Beban :"), BarColumn(bar_width=30, complete_style=j.warna_status),
                          TextColumn(f"{j.beban_saat_ini:.1f}/{j.kapasitas_maks}t"))
    prog_beban.add_task("", total=j.kapasitas_maks, completed=j.beban_saat_ini)

    # PERBAIKAN 4: Membalik persentase Fatigue agar logis (0% = baru, 100% = hancur)
    fatigue_persen = 100.0 - j.kesehatan_struktur
    prog_fatigue = Progress(TextColumn("Fatigue:"), BarColumn(bar_width=30, complete_style="magenta"),
                            TextColumn(f"{fatigue_persen:.1f}%"))
    prog_fatigue.add_task("", total=100, completed=fatigue_persen)

    # <-- TAMBAHAN BARU: Status Palang jadi TUTUP PERMANEN jika runtuh -->
    if j.is_runtuh:
        status_palang = "[bold red]TUTUP PERMANEN[/]"
    else:
        status_palang = "[bold red]TUTUP[/]" if j.palang_tertutup else "[bold green]BUKA[/]"
        
    teks_metrik = Table.grid(padding=1)
    teks_metrik.add_row(
        f"STATUS: [bold {j.warna_status}]{j.status}[/] | PALANG: {status_palang} | Ditolak: {j.kendaraan_ditolak}")
    teks_metrik.add_row(prog_beban)
    teks_metrik.add_row(prog_fatigue)
    layout["metrik"].update(Panel(teks_metrik, border_style=j.warna_status))

    # Visualisasi 2 Jalur
    jalur_a = [" "] * LEBAR_LAYAR
    jalur_b = [" "] * LEBAR_LAYAR

    # Konversi posisi meter ke karakter layar
    skala = LEBAR_LAYAR / j.panjang_meter

    for k in j.kendaraan_aktif:
        # PERBAIKAN 2: Mobil di Jalur B menghadap ke Kiri
        if k["jalur"] == "A":
            teks_k = {"Motor": "[M]>", "Mobil": "[C]>", "Truk": "[T]=>"}[k["jenis"]]
        else:
            teks_k = {"Motor": "<[M]", "Mobil": "<[C]", "Truk": "<=[T]"}[k["jenis"]]

        pos_layar = int(k["posisi_meter"] * skala)
        pos_layar = max(0, min(pos_layar, LEBAR_LAYAR - len(teks_k)))

        target = jalur_a if k["jalur"] == "A" else jalur_b
        for i, char in enumerate(teks_k):
            if pos_layar + i < LEBAR_LAYAR:
                target[pos_layar + i] = char

    teks_a = "".join(jalur_a)
    teks_b = "".join(jalur_b)

    garis = "+" + "=" * LEBAR_LAYAR + "+"

    visual_text = Text()
    
    # <-- TAMBAHAN BARU: Visual jembatan diganti X merah jika runtuh -->
    if j.is_runtuh:
        garis_runtuh = "+" + "X" * LEBAR_LAYAR + "+"
        visual_text.append(f"  {garis_runtuh}\n", style="bold red")
        visual_text.append(f"  |{' JEMBATAN RUNTUH - DITUTUP PERMANEN '.center(LEBAR_LAYAR)}|\n", style="bold white on red")
        visual_text.append(f"  {garis_runtuh}\n", style="bold red")
    else:
        visual_text.append(f"  {garis}\n", style=f"bold {j.warna_status}")
        visual_text.append(f"  |{teks_a}|\n", style="bold white")
        visual_text.append(f"  {garis}\n", style="bold yellow")
        visual_text.append(f"  |{teks_b}|\n", style="bold white")
        visual_text.append(f"  {garis}\n", style=f"bold {j.warna_status}")

    layout["visual"].update(Panel(visual_text, border_style=j.warna_status))

    # Log
    log_text = Text()
    for l in j.logs:
        if "🚨" in l or "❌" in l or "🚫" in l or "💀" in l: # <-- Tambah emoji tengkorak
            log_text.append(l + "\n", style="bold red")
        elif "🟢" in l:
            log_text.append(l + "\n", style="bold green")
        else:
            log_text.append(l + "\n", style="white")
    layout["log"].update(Panel(log_text, title="📝 Log Aktivitas"))

    return layout


# ==========================================
# MAIN LOOP
# ==========================================
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== INPUT SPESIFIKASI JEMBATAN ===")

    try:
        nama = input("Nama Jembatan [Jembatan Ampera]: ") or "Jembatan Ampera"
        kapasitas = float(input("Kapasitas Maksimal (Ton) [100]: ") or 100)
        panjang_m = float(input("Panjang Jembatan (Meter) [1200]: ") or 1200)
        
        # Input Kesehatan Struktur
        kesehatan_awal = float(input("Kesehatan Struktur Awal (%) [100]: ") or 100)
        
        b_waspada = float(input("Batas Waspada (%) [70]: ") or 70)
        b_kritis = float(input("Batas Kritis (%) [90]: ") or 90)
        f_momen = float(input("Faktor Momen Lentur (x) [1.5]: ") or 1.5)
        l_fatigue = float(input("Laju Fatigue (%/ton) [0.5]: ") or 0.5)
    except ValueError:
        print("Input tidak valid! Menggunakan nilai default.")
        nama, kapasitas, panjang_m = "Default Bridge", 100, 1200
        kesehatan_awal = 100 # TAMBAHAN BARU: Default jika error
        b_waspada, b_kritis, f_momen, l_fatigue = 70, 90, 1.5, 0.5

    # Menyesuaikan parameter instansiasi dengan variabel baru
    jembatan = Jembatan(nama, kapasitas, panjang_m, kesehatan_awal, b_waspada, b_kritis, f_momen, l_fatigue)

    # JALANKAN SIMULASI (150 frame)
    with Live(buat_tampilan(jembatan), refresh_per_second=10, screen=True) as live:
        for _ in range(150):
            jembatan.datang_kendaraan()
            jembatan.update_pergerakan()
            live.update(buat_tampilan(jembatan))
            time.sleep(0.1)  # Kecepatan simulasi (10 FPS)
            
            # <-- TAMBAHAN BARU: Hentikan loop jika jembatan sudah runtuh dan kosong -->
            if jembatan.is_runtuh and len(jembatan.kendaraan_aktif) == 0:
                live.update(buat_tampilan(jembatan))
                time.sleep(2) # Jeda sebentar agar teks RUNTUH bisa dibaca
                break