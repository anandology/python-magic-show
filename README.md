# Python Magic Show

> **magic |ˈmadʒɪk|**<br>
> noun [ mass noun ]
>
> the use of special powers to make things happen that would usually be impossible.

## **A Simple Trick!**

```
>>> for i in range(10): print(i+1)
...
1
2
3
4
5
6
7
8
9
01
```

See `rprint.py`.

## What will be the output of this program?

```
>>> x = 1
>>> y = x + 1
>>>
>>> x = 10
>>> print(y)
11
```

See `lazy.py`.

## Fun with Infinite Sequences!

```
>>> one = 1
>>> ones = one >> ones
>>> take(10, ones)
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
>>>
>>> numbers = one >> (ones + numbers)
>>> take(10, numbers)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>>
>>> fibs = one >> (one >> (fibs + tail(fibs)))
>>> take(10, fibs)
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

Try with `lazy.py`.
