import logging
import time
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor

def factorize(numbers):
    result_list = []
    for number in numbers:
        result_list.append([num for num in range(1, number + 1) if number % num == 0])
    return result_list

def factorize_multy(number):
    return [num for num in range(1, number + 1) if number % num == 0]

if __name__ == "__main__":

    # Налаштувати ведення логів
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    lst = [128, 255, 99999, 10651060, 123658500, 654364600]

    # Синхронна версія
    start_time = time.time()
    a, b, c, d, *_ = factorize(lst)
    end_time = time.time()
    print(f"Sync time is: {end_time - start_time}")
    print("Success synchron")

    # Тест
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # Паралельна версія з мультіпроцесінгом
    count_core = cpu_count()
    start_time_multy = time.time()
    with Pool(processes=count_core) as pool:
        result_parallel = pool.map(factorize_multy, lst)
    end_time_multy = time.time()
    print(f"Multy_pool time is: {end_time_multy - start_time_multy}")

    # Паралельна версія з concurrent.futures.ProcessPoolExecutor
    start_time_multy2 = time.time()
    with ProcessPoolExecutor(count_core) as executor:
        result_parallel2 = list(executor.map(factorize_multy, lst))
    end_time_multy2 = time.time()
    print(f"Sync time mylty concarent is: {end_time_multy2 - start_time_multy2}")
        
    # Результати логування
    logger.debug(result_parallel)
    logger.debug(result_parallel2)