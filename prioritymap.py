import heapq
from typing import Iterable, Optional, Tuple, TypeVar

TKey = TypeVar("TKey")
TVal = TypeVar("TVal")


class prioritymap:
    def __init__(self, other: Optional[Iterable[Tuple[TKey, TVal]]] = None):
        self.__heap = []
        self.__dict = {}

        for key, val in other if other is not None else []:
            self[key] = val

    def __contains__(self, key: TKey) -> bool:
        return key in self.__dict

    def __getitem__(self, key: TKey) -> TVal:
        return self.__dict[key]

    def __iter__(self) -> Iterable[TKey]:
        return iter(self.__heap)

    def __len__(self):
        return len(self.__dict)

    def __setitem__(self, key: TKey, value: TVal) -> None:
        heapq.heappush(self.__heap, key)
        self.__dict[key] = value

    def min(self) -> Tuple[TKey, TVal]:
        return self.__heap[0], self.__dict[self.__heap[0]]

    def pop(self) -> Tuple[TKey, TVal]:
        key = heapq.heappop(self.__heap)
        val = self.__dict[key]
        self.__dict.pop(key)
        return key, val

    def items(self) -> Iterable[Tuple[TKey, TVal]]:
        for key in self.__heap:
            yield key, self.__dict[key]

    def values(self) -> Iterable[TVal]:
        for key in self.__heap:
            yield self.__dict[key]
