from threading import Lock


class KeyValueStore:
    def __init__(self):
        self.store = {}
        self.lock = Lock()

    def put(self, key: str, value: str):
        with self.lock:
            self.store[key] = value

    def delete(self, key: str):
        with self.lock:
            if key in self.store:
                del self.store[key]
                return True
            else:
                return False

    def get(self, key: str):
        return self.store.get(key)
