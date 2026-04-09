MIN_RUN = 32


def get_min_run(n):
    r = 0
    while n >= MIN_RUN:
        r |= n & 1
        n >>= 1
    return n + r



# right включительно
# counter[0] хранит число шагов

def insertion_sort(arr, left, right, counter):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1

        while j >= left:
            counter[0] += 1  # сравнение
            if arr[j] > temp:
                arr[j + 1] = arr[j]
                counter[0] += 1  # сдвиг
                j -= 1
            else:
                break

        arr[j + 1] = temp
        counter[0] += 1


# слияние двух отсортированных частей:
# left..mid и mid+1..right

def merge(arr, left, mid, right, counter):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = 0
    j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        counter[0] += 1  # сравнение
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        counter[0] += 1  # запись
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1
        counter[0] += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1
        counter[0] += 1


# поиск естественной серии (run)
# если серия убывающая, переворачиваем ее

def find_run(arr, start, n, counter):
    if start == n - 1:
        return 1

    run_end = start + 1

    counter[0] += 1
    if arr[run_end] < arr[start]:
        while run_end < n:
            if run_end == start + 1:
                run_end += 1
                continue

            counter[0] += 1
            if arr[run_end] < arr[run_end - 1]:
                run_end += 1
            else:
                break

        arr[start:run_end] = arr[start:run_end][::-1]
        counter[0] += (run_end - start)
    else:
        while run_end < n:
            if run_end == start + 1:
                run_end += 1
                continue

            counter[0] += 1
            if arr[run_end] >= arr[run_end - 1]:
                run_end += 1
            else:
                break

    return run_end - start



def timsort(arr, count_steps=False):
    n = len(arr)
    counter = [0]

    if n <= 1:
        if count_steps:
            return arr, 0
        return arr, None

    min_run = get_min_run(n)
    runs = []
    i = 0

    while i < n:
        run_len = find_run(arr, i, n, counter)

        if run_len < min_run:
            right = i + min_run - 1
            if right >= n:
                right = n - 1
            insertion_sort(arr, i, right, counter)
            run_len = right - i + 1

        runs.append((i, run_len))
        i += run_len

    while len(runs) > 1:
        new_runs = []
        i = 0

        while i < len(runs):
            if i == len(runs) - 1:
                new_runs.append(runs[i])
                i += 1
            else:
                left_start, left_len = runs[i]
                right_start, right_len = runs[i + 1]

                left = left_start
                mid = left_start + left_len - 1
                right = right_start + right_len - 1

                merge(arr, left, mid, right, counter)
                new_runs.append((left_start, left_len + right_len))
                i += 2

        runs = new_runs

    if count_steps:
        return arr, counter[0]
    return arr, None


if __name__ == '__main__':
    a = [5, 1, 9, 3, 7, 2, 8, 4, 6]
    print('До сортировки:', a)
    timsort(a)
    print('После сортировки:', a)
