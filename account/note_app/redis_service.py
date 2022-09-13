import redis


class RedisCode:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379)

    def extract(self, key):
        """
        for getting the cache
        :param key: getting the key as user_id
        """
        return self.r.get(key)

    def save(self, key, value):
        """
        for inserting in the cache
        :param key: key as user_id
        :param value: value will be note data
        """
        return self.r.set(key, value)