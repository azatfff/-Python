def insertion_sort(items, key):
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and key(items[j]) > key(current):
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
    return items