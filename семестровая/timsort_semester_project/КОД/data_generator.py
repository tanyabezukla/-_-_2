import os
import random


def generate_files(folder, count=100, min_size=100, max_size=10000):
    if not os.path.exists(folder):
        os.makedirs(folder)

    random.seed(42)

    if count == 1:
        sizes = [min_size]
    else:
        step = (max_size - min_size) // (count - 1)
        sizes = []
        for i in range(count - 1):
            sizes.append(min_size + i * step)
        sizes.append(max_size)

    for i in range(count):
        size = sizes[i]
        numbers = []
        for _ in range(size):
            numbers.append(random.randint(-100000, 100000))

        file_name = 'dataset_{:03d}_n{:05d}.txt'.format(i + 1, size)
        path = os.path.join(folder, file_name)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(' '.join(map(str, numbers)))

    print('Файлы с входными данными созданы в папке:', folder)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    data_folder = os.path.join(project_dir, 'data', 'input')
    generate_files(data_folder)
