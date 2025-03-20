import requests
import sys
import concurrent.futures
from tqdm import tqdm

# Cấu hình
TARGET_URL = "https://vku.udn.vn"  # Thay đổi URL mục tiêu
WORDLIST_FILE = "common.txt"  # File chứa danh sách thư mục để brute-force
TIMEOUT = 10  # Giới hạn thời gian chờ request
MAX_WORKERS = 40  # Số luồng song song (tăng tốc độ)

# Các mã trạng thái HTTP hợp lệ
VALID_STATUS_CODES = {200, 301, 302, 403, 401}

def check_directory(directory):
    """Kiểm tra một thư mục trên website."""
    full_url = f"{TARGET_URL.rstrip('/')}/{directory}"
    try:
        response = requests.get(full_url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        if response.status_code in VALID_STATUS_CODES:
            tqdm.write(f"[+] Found: {full_url} ({response.status_code})")
            return (full_url, response.status_code)
    except requests.RequestException:
        pass  # Bỏ qua lỗi kết nối hoặc timeout
    return None

def scan_directory(wordlist):
    """Quét thư mục của một trang web với danh sách từ wordlist bằng cách sử dụng đa luồng."""
    results = []
    with open(wordlist, "r") as file:
        directories = [line.strip() for line in file.readlines()]
    
    with tqdm(total=len(directories), desc="Scanning", unit="dir") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(check_directory, directory): directory for directory in directories}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                pbar.update(1)
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TARGET_URL = sys.argv[1]  # Nhập URL từ dòng lệnh
    print(f"Starting scan on {TARGET_URL}\n")
    found_dirs = scan_directory(WORDLIST_FILE)
    print("\nScan completed. Found directories:")
    for url, status in found_dirs:
        print(f"{url} ({status})")