import struct

class vec:
    def __init__(self):
        self.id = 4
        self.x = 12
        self.y = 14


v = vec()

print(v)

pospack = struct.pack("ii", v.x, v.y)
idpack = struct.pack("i", v.id)


print(pospack)
print(idpack)
print(idpack + pospack)