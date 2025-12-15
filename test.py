class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        value = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return value

    def display(self):
        current = self.front
        if not current:
            print("Queue is empty")
            return
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


def insertion_sort(row):
    for i in range(1, len(row)):
        x = row[i]
        j = i - 1
        while j >= 0 and row[j] > x:
            row[j + 1] = row[j]
            j -= 1
        row[j + 1] = x
    return row


def column_average_below_main_diagonal(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = []

    for j in range(m):
        values = []
        for i in range(j + 1, n):
            values.append(matrix[i][j])
        if values:
            result.append(sum(values) / len(values))

    return result


def product(values):
    result = 1
    for v in values:
        result *= v
    return result


def main():
    q = Queue()
    q.enqueue("Order #101")
    q.enqueue("Order #102")
    q.enqueue("Order #103")

    print("Queue:")
    q.display()
    print("Processed:", q.dequeue())
    q.display()

    A = [
        [1, 16, 21, 11, 6],
        [2, 17, 22, 12, 7],
        [3, 18, 23, 13, 8],
        [4, 19, 24, 14, 9],
        [5, 20, 25, 15, 10],
    ]

    print("\nMatrix:")
    for row in A:
        print(row)

    for i in range(len(A)):
        A[i] = insertion_sort(A[i])

    print("\nSorted matrix:")
    for row in A:
        print(row)

    f_values = column_average_below_main_diagonal(A)
    F_value = product(f_values)

    print("\nf(a_ij):", f_values)
    print("F(f(a_ij)) =", F_value)


if __name__ == "__main__":
    main()
