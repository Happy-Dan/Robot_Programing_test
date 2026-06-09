import sys


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    # Example: first value is n, followed by n integers.
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    print(sum(nums))


if __name__ == "__main__":
    solve()
