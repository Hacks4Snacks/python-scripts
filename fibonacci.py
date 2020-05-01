#!/bin/env python3
# simple computer science problem solving with python
# fibonacci sequence
# fib(n) = fib(n - 1) + fib(n - 2)

def fib(n: int) -> int:
    if n == 0: return n
    last: int = 0
    next: int = 1
    for _ in range(1,n):
        last, next = next, last + next
    return next

if __name__ == "__main__":
    print(f'Please input fibonacci sequence number: ')
    fib_num = input()
    print(f'The {fib_num}th sequence number value is: ')
    print(fib(int(fib_num)))