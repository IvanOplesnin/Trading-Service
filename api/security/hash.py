import hashlib


class Hash:

    def __init__(self, string: str):
        self._hash = hashlib.sha256(string.encode()).hexdigest()

    def compare_hash(self, string: str) -> bool:
        return hashlib.sha256(string.encode()).hexdigest() == self._hash

    def __call__(self) -> str:
        return self._hash


if __name__ == "__main__":
    hash = Hash("hello world")
    print(hash())
    print(hash.compare_hash("hello world"))
    print(hash.compare_hash("hello worl"))
