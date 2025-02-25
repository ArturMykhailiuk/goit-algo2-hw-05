import time
from collections import Counter
from hyperloglog import HyperLogLog
import json


def load_data(file_path: str) -> list:
    """
    Завантажує дані з лог-файлу, ігноруючи некоректні рядки.
    Повертає список IP-адрес.
    """
    ip_addresses = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                continue

    return ip_addresses


def exact_unique_count(ip_addresses: list) -> int:
    """
    Повертає точну кількість унікальних IP-адрес за допомогою set.
    """
    return len(set(ip_addresses))


def hyperloglog_unique_count(ip_addresses: list, error_rate: float = 0.01) -> int:
    """
    Повертає наближену кількість унікальних IP-адрес за допомогою HyperLogLog.
    """
    hll = HyperLogLog(error_rate)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


if __name__ == "__main__":
    # Завантаження даних
    file_path = "lms-stage-access.log"
    ip_addresses = load_data(file_path)

    # Точний підрахунок унікальних IP-адрес
    start_time = time.time()
    exact_count = exact_unique_count(ip_addresses)
    exact_time = time.time() - start_time

    # Підрахунок унікальних IP-адрес за допомогою HyperLogLog
    start_time = time.time()
    hll_count = hyperloglog_unique_count(ip_addresses)
    hll_time = time.time() - start_time

    # Виведення результатів
    print("Результати порівняння:")
    print(f"{' ':<25} {'Точний підрахунок':<20} {'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<25} {exact_count:<20.1f} {hll_count:<20.1f}")
    print(f"{'Час виконання (сек.)':<25} {exact_time:<20.6f} {hll_time:<20.6f}")
