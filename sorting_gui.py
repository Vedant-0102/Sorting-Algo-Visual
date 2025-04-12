
import streamlit as st
import matplotlib.pyplot as plt
import time
import random

if 'data' not in st.session_state:
    st.session_state.data = []
    st.session_state.sorting = False
    st.session_state.speed = 0.1
    st.session_state.swaps = 0
    st.session_state.start_time = 0

st.title("Sorting Visualizer ")

st.sidebar.header("Settings")
speed_option = st.sidebar.radio("Select Speed Multiplier:", options=["0.5x", "0.75x", "1x", "1.5x", "2x"], index=2)

speed_mapping = {"0.5x": 2.0, "0.75x": 1.33, "1x": 1.0, "1.5x": 0.66, "2x": 0.5}
speed = speed_mapping[speed_option]
algorithm = st.sidebar.selectbox("Choose Sorting Algorithm", [
    "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort",
    "Quick Sort", "Heap Sort", "Shell Sort"
])
array_input = st.text_input("Enter numbers (space separated):")

if st.button("Generate Random Array"):
    st.session_state.data = random.sample(range(10, 100), 12)
    st.session_state.swaps = 0

if array_input:
    try:
        st.session_state.data = list(map(int, array_input.strip().split()))
        st.session_state.swaps = 0
    except:
        st.error("Invalid input. Please enter integers only.")

# Visualize
plot_area = st.empty()
fig, ax = plt.subplots()
def draw_data(data, color_map):
    ax.clear()
    bars = ax.bar(range(len(data)), data, color=color_map)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1, str(data[i]), ha='center', va='bottom', fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    plot_area.pyplot(fig)

# Sorting Algorithms

def bubble_sort():
    data = st.session_state.data
    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                st.session_state.swaps += 1
            draw_data(data, ['red' if x == j or x == j+1 else 'gray' for x in range(len(data))])
            time.sleep(speed)


def selection_sort():
    data = st.session_state.data
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
            draw_data(data, ['red' if x == j or x == min_idx else 'gray' for x in range(len(data))])
            time.sleep(speed)
        data[i], data[min_idx] = data[min_idx], data[i]
        st.session_state.swaps += 1


def insertion_sort():
    data = st.session_state.data
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
            draw_data(data, ['red' if x == j + 1 or x == i else 'gray' for x in range(len(data))])
            time.sleep(speed)
            st.session_state.swaps += 1
        data[j + 1] = key


def merge_sort(data, l, r):
    if l < r:
        m = (l + r) // 2
        merge_sort(data, l, m)
        merge_sort(data, m + 1, r)
        merge(data, l, m, r)

def merge(data, l, m, r):
    L = data[l:m + 1]
    R = data[m + 1:r + 1]
    i = j = 0
    k = l
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            data[k] = L[i]
            i += 1
        else:
            data[k] = R[j]
            j += 1
        draw_data(data, ['red' if x == k else 'gray' for x in range(len(data))])
        time.sleep(speed)
        st.session_state.swaps += 1
        k += 1
    while i < len(L):
        data[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        data[k] = R[j]
        j += 1
        k += 1


def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            st.session_state.swaps += 1
        draw_data(data, ['red' if x == i or x == j else 'gray' for x in range(len(data))])
        time.sleep(speed)
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1


def heap_sort():
    data = st.session_state.data
    n = len(data)

    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r
        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            st.session_state.swaps += 1
            draw_data(data, ['red' if x == i or x == largest else 'gray' for x in range(len(data))])
            time.sleep(speed)
            heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        st.session_state.swaps += 1
        draw_data(data, ['green' if x >= i else 'gray' for x in range(len(data))])
        time.sleep(speed)
        heapify(i, 0)


def shell_sort():
    data = st.session_state.data
    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            while j >= gap and data[j - gap] > temp:
                data[j] = data[j - gap]
                j -= gap
                st.session_state.swaps += 1
                draw_data(data, ['red' if x == j or x == i else 'gray' for x in range(len(data))])
                time.sleep(speed)
            data[j] = temp
        gap //= 2

# Run selected sort
if st.button("Start Sorting") and st.session_state.data:
    st.session_state.start_time = time.time()
    if algorithm == "Bubble Sort":
        bubble_sort()
    elif algorithm == "Selection Sort":
        selection_sort()
    elif algorithm == "Insertion Sort":
        insertion_sort()
    elif algorithm == "Merge Sort":
        merge_sort(st.session_state.data, 0, len(st.session_state.data) - 1)
    elif algorithm == "Quick Sort":
        quick_sort(st.session_state.data, 0, len(st.session_state.data) - 1)
    elif algorithm == "Heap Sort":
        heap_sort()
    elif algorithm == "Shell Sort":
        shell_sort()
    elapsed = time.time() - st.session_state.start_time
    draw_data(st.session_state.data, ['green'] * len(st.session_state.data))
    st.success(f"Done! Time: {elapsed:.2f}s | Swaps: {st.session_state.swaps}")
