import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CustomList:
    def __init__(self, data=None):
        self._data = [int(x) for x in data] if data else []

    def __getitem__(self, i): return self._data[i]
    def __setitem__(self, i, v): self._data[i] = int(v)
    def __len__(self): return len(self._data)
    def __contains__(self, item): return item in self._data

    def __iadd__(self, other):
        self._data += other._data if isinstance(other, CustomList) else [int(other)]
        return self

    def __isub__(self, other):
        for x in (other._data if isinstance(other, CustomList) else [int(other)]):
            if x in self._data: self._data.remove(x)
        return self

    def __imul__(self, other):
        self._data *= int(other)
        return self

    def __repr__(self): return str(self._data)


with open("numbers.txt", "r", encoding="utf-8") as f:
    text = f.read()

cl = CustomList(re.findall(r'-?\d+', text))

print(f"Числа: {cl}")
print(f"Кількість: {len(cl)}")
print(f"Сума: {sum(cl._data)}")
print(f"Є хоча б одне з {{1,3,1984,7777}}: {any(x in cl for x in [1,3,1984,7777])}")
print(f"Ненульових чисел: {sum(1 for x in cl._data if x != 0)}")