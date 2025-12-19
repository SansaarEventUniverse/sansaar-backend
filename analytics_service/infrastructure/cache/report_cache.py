class ReportCache:
    def __init__(self):
        self._cache = {}

    def set(self, key: int, value: dict):
        self._cache[key] = value

    def get(self, key: int):
        return self._cache.get(key)
