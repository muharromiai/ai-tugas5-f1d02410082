# Sistem Pakar Sederhana: Diagnosis Gangguan Printer

- **Nama:** Muharromi Ali Ilham
- **NIM :** F1D02410082

## Topik dan Cara Menjalankan Program
- **Topik:** Diagnosis Gangguan Teknis pada Printer.
- **Bahasa Pemrograman:** Python 3.14.8
- **Cara Menjalankan:**
  Buka terminal atau command prompt, masuk ke direktori yang sama dengan file program, lalu jalankan perintah berikut:
  ```bash
  python sistem_pakar_printer.py

## Sumber
- S1: https://download4.epson.biz/sec_pubs/l3210_series/useg/en/index.htm?pageid=&tab=&LGW=&CNW=&OSV=&EXE=&VER=
- S2: https://oip.manual.canon/USRMA-0312-zz-CS-enGB/contents/1T0002910536.html

## Tabel Aturan
| Aturan | IF | Mode | THEN | Sumber |
| --- | --- | --- | --- | --- |
| R1 | lampu tinta berkedip bergantian OR printer mendeteksi masa pakai komponen habis | ATAU | absorber tinta penuh | S1 |
| R2 | absorber tinta penuh AND printer menolak mencetak | DAN | perlu reset waste ink pad | S1 |
| R3 | hasil cetak bergaris putih AND warna cetak tidak sesuai | DAN | printhead tersumbat | S1 |
| R4 | printhead tersumbat AND sudah dilakukan cleaning standar gagal | DAN | perlu deep cleaning manual | S2 |
| R5 | kertas ditarik miring OR kertas tidak mau masuk sama sekali | ATAU | roller kertas kotor atau aus | S2 |
| R6 | roller kertas kotor atau aus AND ada benda asing di jalur kertas	| DAN | perlu pembersihan mekanis jalur kertas	| S2 |

## Metode
- **Metode:** Forward Chaining (FC).

- **Alasan:** Metode Forward Chaining cocok digunakan untuk kasus troubleshooting. Prosesnya dimulai dengan mengumpulkan fakta-fakta berupa gejala yang sedang dialami oleh pengguna, kemudian sistem merangkai fakta-fakta tersebut ke depan untuk mencocokkannya dengan aturan guna menghasilkan kesimpulan jenis kerusakan dan solusi yang sesuai.

## Kasus Uji
![Kasus uji 1](/ai-tugas5-f1d02410082/screenshot/kasus1.png)
--------------------------------------------------------------
![Kasus uji 2](/ai-tugas5-f1d02410082/screenshot/kasus2.png)
--------------------------------------------------------------
![Kasus uji 2](/ai-tugas5-f1d02410082/screenshot/kasus3.png)

## Penggunaan Alat Bantu AI
Pembuatan sistem pakar ini dibantu oleh AI Gemini untuk:
- Mencaari topik, mencari referensi sumber, dan menstrukturkan aturan IF-THEN.
- Menghasilkan logika kode Forward Chaining dan pemformatan file JSON dasar menggunakan Python.