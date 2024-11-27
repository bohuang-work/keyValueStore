from threading import Lock


class KeyValueStore:
    """A thread-safe in-memory key-value store.

    This class provides methods to store, retrieve, and delete key-value pairs.
    It uses a lock to ensure thread safety for concurrent access to the underlying data.

    Attributes:
        store (dict): The dictionary that holds the key-value pairs.
        lock (Lock): A lock to synchronize access to the store.
    """

    def __init__(self):
        """Initializes the KeyValueStore with an empty dictionary and a lock.

        Args:
            None

        Returns:
            None
        """
        self.store = {}
        self.lock = Lock()

    def put(self, key: str, value: str) -> None:
        """Adds or updates a key-value pair in the store.

        If the key already exists, the value will be updated.

        Args:
            key (str): The key to store.
            value (str): The value associated with the key.

        Returns:
            None
        """
        with self.lock:
            self.store[key] = value

    def delete(self, key: str) -> bool:
        """Deletes a key-value pair from the store.

        If the key does not exist, returns False.

        Args:
            key (str): The key to delete.

        Returns:
            bool: True if the key was found and deleted, False otherwise.
        """
        with self.lock:
            if key in self.store:
                del self.store[key]
                return True
            else:
                return False

    def get(self, key: str) -> str | None:
        """Retrieves the value associated with the given key.

        If the key does not exist, returns None.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str | None: The value associated with the key, or None if not found.
        """
        return self.store.get(key)
