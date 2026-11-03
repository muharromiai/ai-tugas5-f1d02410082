import json

def muat_kb(nama_file):
    with open(nama_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def ekstrak_semua_premis(aturan_list):
    """Mengambil daftar semua fakta unik yang menjadi syarat (jika) agar bisa ditanyakan ke user"""
    premis_set = set()
    for rules in aturan_list:
        for premis in rules['if']:
            premis_set.add(premis)
    return list(premis_set)

def jalankan_forward_chaining(kb):
    print("=" * 60)
    print(f" {kb['judul']} ")
    print(f" {kb['batas']} ")
    print("=" * 60)
    print("Jawab pertanyaan berikut dengan mengetik 'y' (ya) atau 't' (tidak).\n")

    aturan_list = kb['rules']
    sumber_dict = kb['sumber']
    
    semua_premis = ekstrak_semua_premis(aturan_list)
    
    memori_fakta = set()
    jejak_alasan = {} #menyimpan aturan

    fakta_ditanyakan = set()
    
    siklus = 1
    aktif = True

    while aktif:
        aturan_baru_terpicu = False
        
        for premis in semua_premis:
            if premis not in fakta_ditanyakan and premis not in memori_fakta:
                is_hasil_aturan = any(a['then'] == premis for a in aturan_list)
                if not is_hasil_aturan:
                    jawaban = input(f"Apakah '{premis}'? (y/t) > ").strip().lower()
                    fakta_ditanyakan.add(premis)
                    if jawaban == 'y':
                        memori_fakta.add(premis)

        for rules in aturan_list:
            id_aturan = rules['id']
            syarat = rules['if']
            mode = rules['mode']
            kesimpulan = rules['then']
            kode_sumber = rules['sumber']
            nama_sumber = sumber_dict.get(kode_sumber, "Sumber Resmi")

            if kesimpulan in memori_fakta:
                continue

            #cek apakah syarat terpenuhi berdasarkan dan/atau
            terpenuhi = False
            if mode == 'dan':
                terpenuhi = all(s in memori_fakta for s in syarat)
            elif mode == 'atau':
                terpenuhi = any(s in memori_fakta for s in syarat)

            if terpenuhi:
                memori_fakta.add(kesimpulan)
                jejak_alasan[kesimpulan] = {
                    "rules": id_aturan,
                    "syarat": syarat,
                    "sumber": f"{kode_sumber} ({nama_sumber})"
                }
                aturan_baru_terpicu = True
                print(f"Siklus {siklus}: {id_aturan} -> {kesimpulan}")

        if not aturan_baru_terpicu:
            #cek fakta turunan yang belum dievaluasi
            ada_premis_turunan_belum_tanya = False
            for rules in aturan_list:
                for premis in rules['if']:
                    if premis not in fakta_ditanyakan:
                        is_hasil_aturan = any(a['then'] == premis for a in aturan_list)
                        if is_hasil_aturan and not any(a['then'] == premis and a['then'] in memori_fakta for a in aturan_list):
                            pass
            
            aktif = False
        else:
            siklus += 1

    print("\n" + "=" * 60)
    print("HASIL KESIMPULAN")
    print("=" * 60)
    
    kesimpulan_tercapai = list(jejak_alasan.keys())
    
    if not kesimpulan_tercapai:
        print("Kesimpulan: Tidak ada kesimpulan yang dapat ditarik (Kasus Negatif / Normal / Gejala tidak dikenali).")
    else:
        print(f"Fakta awal yang valid: {', '.join([f for f in memori_fakta if f in semua_premis])}")
        print("\nKesimpulan akhir yang didapat:")
        for k in kesimpulan_tercapai:
            digunakan_lagi = any(k in a['if'] for a in aturan_list)
            if not digunakan_lagi:
                print(f"  - {k.upper()}")

        print("\nAlasan (Jejak / Trace):")
        for kesimpulan, detail in jejak_alasan.items():
            syarat_str = ", ".join(detail['syarat'])
            print(f"  - {kesimpulan} <- {detail['rules']} ({detail['sumber']}) [Syarat: {syarat_str}]")

    print("=" * 60)

if __name__ == "__main__":
    try:
        kb_data = muat_kb("kb_printer.json")
        jalankan_forward_chaining(kb_data)
    except FileNotFoundError:
        print("Error: File 'kb_printer.json' tidak ditemukan! Pastikan file berada di direktori yang sama.")