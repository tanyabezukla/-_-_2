import csv
import math
import os
import statistics
import sys
import time

import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from timsort import timsort


def read_numbers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().split()
    return [int(x) for x in text]


def measure_time(numbers, repeats=3):
    times = []
    for _ in range(repeats):
        arr = numbers.copy()
        start = time.perf_counter()
        timsort(arr)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return statistics.median(times)


def measure_steps(numbers):
    arr = numbers.copy()
    _, steps = timsort(arr, True)
    return steps


def save_table(rows, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['dataset', 'file_name', 'size', 'time_ms', 'steps', 'n_log2_n'])
        for row in rows:
            writer.writerow(row)


def make_graph(sizes, values, ylabel, title, file_path):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, values)
    plt.xlabel('Размер входного массива, n')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(file_path, dpi=200)
    plt.close()


def main():
    project_dir = os.path.dirname(current_dir)
    input_dir = os.path.join(project_dir, 'data', 'input')
    results_dir = os.path.join(project_dir, 'results')

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    files = sorted([name for name in os.listdir(input_dir) if name.endswith('.txt')])

    rows = []
    sizes = []
    times = []
    steps_list = []

    for index, file_name in enumerate(files, start=1):
        file_path = os.path.join(input_dir, file_name)
        numbers = read_numbers(file_path)
        n = len(numbers)

        time_ms = measure_time(numbers)
        steps = measure_steps(numbers)
        n_log = round(n * math.log2(n), 3)

        rows.append([index, file_name, n, round(time_ms, 6), steps, n_log])
        sizes.append(n)
        times.append(time_ms)
        steps_list.append(steps)

        print('Обработан файл:', file_name)

    save_table(rows, os.path.join(results_dir, 'benchmark_results.csv'))

    make_graph(
        sizes,
        times,
        'Время сортировки, мс',
        'Зависимость времени сортировки Timsort от размера массива',
        os.path.join(results_dir, 'time_vs_size.png')
    )

    make_graph(
        sizes,
        steps_list,
        'Количество шагов',
        'Зависимость количества шагов Timsort от размера массива',
        os.path.join(results_dir, 'steps_vs_size.png')
    )

    with open(os.path.join(results_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write('Количество наборов данных: ' + str(len(rows)) + '\n')
        f.write('Минимальный размер массива: ' + str(min(sizes)) + '\n')
        f.write('Максимальный размер массива: ' + str(max(sizes)) + '\n')
        f.write('Минимальное время, мс: ' + str(round(min(times), 6)) + '\n')
        f.write('Максимальное время, мс: ' + str(round(max(times), 6)) + '\n')
        f.write('Минимальное количество шагов: ' + str(min(steps_list)) + '\n')
        f.write('Максимальное количество шагов: ' + str(max(steps_list)) + '\n')

    print('Готово. Результаты сохранены в папке results')


if __name__ == '__main__':
    main()
