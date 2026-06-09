# Python Cheat Sheet

## 標準入力

```python
s = input()
n = int(input())
a, b = map(int, input().split())
nums = list(map(int, input().split()))
```

複数行:

```python
import sys

lines = sys.stdin.read().splitlines()
```

## リスト

```python
xs = [3, 1, 2]
xs.append(4)
xs.sort()
ys = sorted(xs, reverse=True)
```

## 辞書

```python
count = {}
for x in xs:
    count[x] = count.get(x, 0) + 1
```

## ループ

```python
for i in range(n):
    print(i)

for i, x in enumerate(xs):
    print(i, x)
```

## 関数

```python
def add(a, b):
    return a + b
```

## よくある確認

```python
if x in xs:
    print("found")

if key in count:
    print(count[key])
```
