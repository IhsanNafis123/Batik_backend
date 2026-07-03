import os
import shutil

# Konfigurasi Folder
# Pastikan folder asal sesuai dengan lokasi dataset Anda
FOLDER_TRAIN_ASAL = "backend/dataset/train" 
FOLDER_LORA_TUJUAN = "dataset_untuk_lora"
TRIGGER_WORD = "zxcv_batik"

def siapkan_dataset_lora():
    # Buat folder tujuan jika belum ada
    if not os.path.exists(FOLDER_LORA_TUJUAN):
        os.makedirs(FOLDER_LORA_TUJUAN)

    # Cek apakah folder asal ada
    if not os.path.exists(FOLDER_TRAIN_ASAL):
        print(f"Error: Folder {FOLDER_TRAIN_ASAL} tidak ditemukan.")
        return

    total_gambar = 0

    # Mulai membaca setiap folder motif di dalam folder train
    for nama_folder_motif in os.listdir(FOLDER_TRAIN_ASAL):
        path_folder_motif = os.path.join(FOLDER_TRAIN_ASAL, nama_folder_motif)
        
        # Pastikan yang dibaca adalah folder, bukan file
        if os.path.isdir(path_folder_motif):
            # Ubah "Jawa_Barat_Megamendung" menjadi "Jawa Barat Megamendung"
            nama_motif_bersih = nama_folder_motif.replace("_", " ")
            
            # Format teks (caption) yang akan diajarkan ke AI
            caption = f"{TRIGGER_WORD}, motif {nama_motif_bersih}, pola batik tradisional indonesia, detail tinggi"

            # Baca semua gambar di dalam folder motif tersebut
            for nama_file in os.listdir(path_folder_motif):
                if nama_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    path_file_asal = os.path.join(path_folder_motif, nama_file)
                    
                    # Buat nama baru agar tidak ada nama file yang bentrok
                    # Contoh: 10005.jpg menjadi Aceh_Pintu_Aceh_10005.jpg
                    nama_file_baru = f"{nama_folder_motif}_{nama_file}"
                    path_gambar_tujuan = os.path.join(FOLDER_LORA_TUJUAN, nama_file_baru)
                    
                    # Tentukan nama file teks (.txt)
                    nama_file_txt = nama_file_baru.rsplit('.', 1)[0] + ".txt"
                    path_txt_tujuan = os.path.join(FOLDER_LORA_TUJUAN, nama_file_txt)
                    
                    # 1. Copy gambar ke folder tujuan
                    shutil.copy2(path_file_asal, path_gambar_tujuan)
                    
                    # 2. Buat file .txt yang berisi caption
                    with open(path_txt_tujuan, "w") as f:
                        f.write(caption)
                        
                    total_gambar += 1

    print(f"\nSelesai! {total_gambar} gambar dan {total_gambar} file teks telah disiapkan.")
    print(f"Silakan jadikan folder '{FOLDER_LORA_TUJUAN}' menjadi format .zip untuk di-upload ke fal.ai")

if __name__ == "__main__":
    siapkan_dataset_lora()