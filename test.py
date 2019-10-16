import functools
import json

arr = [2, 3, 4, 5, 1, 5, 3, 7]


def quick_sort(arr):
    if len(arr) > 1:
        mid_num = arr[len(arr) // 2]

        arr.remove(mid_num)
        left, right = [], []
        right = [num for num in arr if num >= mid_num]
        left = [num for num in arr if num < mid_num]
        return quick_sort(left) + [mid_num] + quick_sort(right)
    return arr


def nearly_swap_change(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def choice_sort(arr):
    for i in range(len(arr) - 1):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] > arr[min_index]:
                min_index = j
        arr[min_index], arr[i] = arr[i], arr[min_index]


# choice_sort(arr)
# print(arr)

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__, '被调用')
        return func(*args, **kwargs)

    return wrapper


@log
def now():
    json.loads()
    print("2019")


@log
class Test:
    pass
