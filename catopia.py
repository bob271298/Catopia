import requests
from datetime import datetime
import pytz
import time
import random
from colorama import Fore, Style, init
import os

def welcome():
    print(r"""
          
NGWE YOK
          """)
    print(Fore.GREEN + Style.BRIGHT + "Catopia BOT")
    print(Fore.GREEN + Style.BRIGHT + "By: @Tipang27\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_color():
    colors = [Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
    return random.choice(colors)

def login():
    url = "https://api.catopia.io/api/v1/auth/telegram"
    headers = {
        "Authorization": "Bearer",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "initData": "query_here"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        response_json = response.json()
        access_token = response_json.get('data', {}).get('accessToken', None)
        return access_token
    else:
        print(f"Login request failed with status code {response.status_code}")
        return None

def cek_tanaman(access_token):
    url = "https://api.catopia.io/api/v1/players/plant?limit=3000"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', [])
        
        if not data:
            print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Tidak ada benih, melakukan pembelian benih...")
            beli_benih(access_token)
        else:
            for item in data:
                menanam(item.get('id'), access_token)
    else:    
        main()

def ubah_ke_wib(gmt_time_str):
    gmt_format = "%a, %d %b %Y %H:%M:%S GMT"
    gmt_time = datetime.strptime(gmt_time_str, gmt_format)
    gmt_timezone = pytz.timezone('GMT')
    gmt_time = gmt_timezone.localize(gmt_time)
    wib_timezone = pytz.timezone('Asia/Jakarta')
    wib_time = gmt_time.astimezone(wib_timezone)
    wib_format = "%Y-%m-%d %H:%M:%S %Z"
    return wib_time.strftime(wib_format)

def cek_panen(grownAt_str):
    wib_format = "%Y-%m-%d %H:%M:%S %Z"
    wib_time = datetime.strptime(grownAt_str, wib_format)
    wib_timezone = pytz.timezone('Asia/Jakarta')
    wib_time = wib_timezone.localize(wib_time)
    now = datetime.now(wib_timezone)
    if now >= wib_time:
        return "Siap Panen",
    else:
        remaining_seconds = (wib_time - now).total_seconds()
        return "Belum Siap Panen", remaining_seconds

def display_countdown(remaining_seconds):
    while remaining_seconds > 0:
        minutes, seconds = divmod(int(remaining_seconds), 60)
        time_format = f"{minutes:02}:{seconds:02}"
        colortime = get_random_color()
        print(f"\r[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Waktu Panen Selanjutnya: {colortime}{time_format}{Style.RESET_ALL}", end='')
        time.sleep(1)
        remaining_seconds -= 1
    print()

def panen(plantId, landId, access_token):
    url = "https://api.catopia.io/api/v1/players/plant/harvest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "plantId": plantId,
        "landId": landId
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Panen berhasil untuk plantId {plantId} di landId {landId}")
        cek_tanah(access_token)
    else:
        main()

def beli_benih(access_token):
    url = "https://api.catopia.io/api/v1/store/buy"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "storeId": 17,
        "price": 16000.0,
        "unit": 1
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Pembelian benih berhasil")
        cek_tanaman(access_token)
    else:
        main()

def cek_tanah(access_token):
    url = "https://api.catopia.io/api/v1/players/land?limit=3000"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json().get('data', {})
        empty_land = data.get('emptyLand', [])
        occupied_land = data.get('occupiedLand', [])
        
        ids_grownAt = [{'id': land['id'], 'plantId': land.get('plantId'), 'plantName': land['plantName'], 'grownAt': land['grownAt']} for land in occupied_land]
        
        for item in ids_grownAt:
            clear_console()
            results(access_token)
            id_value = item.get('id', 'empty')
            plant_name = item.get('plantName', 'empty')
            for _ in range(len(ids_grownAt)):
                print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Id: {Fore.LIGHTMAGENTA_EX}{id_value}{Style.RESET_ALL} | Jenis: {Fore.LIGHTMAGENTA_EX}{plant_name}{Style.RESET_ALL}")
            
            item['grownAt'] = ubah_ke_wib(item['grownAt'])
            status, *rest = cek_panen(item['grownAt'])
            
            if status == "Siap Panen":
                print(f"[{Fore.LIGHTBLUE_EX}Info{Style.RESET_ALL}] Saatnya Panen")
                panen(item['plantId'], item['id'], access_token)
            else:
                remaining_seconds = rest[0]
                display_countdown(remaining_seconds)
                cek_tanah(access_token)
                return
                
        if empty_land:
            print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Jumlah tanah kosong: {len(empty_land)}")
            print(f"[{Fore.LIGHTBLUE_EX}Info{Style.RESET_ALL}] Menanam Benih.....")
            for _ in empty_land:
                cek_tanaman(access_token)
    else:
        main()

def menanam(plantId, access_token):
    url = "https://api.catopia.io/api/v1/players/plant"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    empty_land_url = "https://api.catopia.io/api/v1/players/land?limit=3000"
    empty_land_response = requests.get(empty_land_url, headers=headers)
    
    if empty_land_response.status_code == 200:
        empty_land_data = empty_land_response.json().get('data', {}).get('emptyLand', [])
        if empty_land_data:
            for land in empty_land_data:
                landId = land.get('id')
                data = {
                    "plantId": plantId,
                    "landId": landId
                }
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 201:
                    print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Penanaman berhasil untuk plantId {plantId} di landId {landId}")
                else:
                    cek_tanaman(access_token)
            cek_tanah(access_token)
        else:
            print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Tidak ada tanah kosong untuk penanaman.")
            cek_tanah(access_token)
    else:
        main()

def cek_data_user(access_token):
    url = "https://api.catopia.io/api/v1/user/me?limit=3000"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      response.raise_for_status()
      return response.json()
    
    else:
         main()

def cek_coin(access_token):
    url = "https://api.catopia.io/api/v1/user-collection?limit=3000"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      response.raise_for_status()
      return response.json()
    
    else:
         main()
    
def results(access_token):
    data_user_response = cek_data_user(access_token)
    coin_response = cek_coin(access_token)
    full_name = data_user_response.get('data', {}).get('fullName')
    level = data_user_response.get('data', {}).get('level')
    golden_coin = coin_response.get('data', {}).get('goldenCoin')
    gem = coin_response.get('data', {}).get('gem')
    separator = '=' * len(full_name)

    welcome()
    print(f"{Fore.LIGHTCYAN_EX}=========={full_name}=========={Style.RESET_ALL}")
    print(f"Balance: {Fore.LIGHTGREEN_EX}{golden_coin}{Style.RESET_ALL}")
    print(f"Diamond: {Fore.LIGHTGREEN_EX}{gem}{Style.RESET_ALL}")
    print(f"Level: {Fore.LIGHTGREEN_EX}{level}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}===================={separator}{Style.RESET_ALL}")

def main():
    init()
    clear_console()
    welcome()
    print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Login...")
    access_token = login()
    
    if access_token:
        print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Berhasil login, cek tanaman...")
        cek_tanaman(access_token)
    else:
        print(f"[{Fore.LIGHTYELLOW_EX}Info{Style.RESET_ALL}] Login gagal. Mengulangi...")
        time.sleep(10)
        main()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"[{Fore.RED}Error{Style.RESET_ALL}] {e}. Mengulangi...")
            time.sleep(10)
            
