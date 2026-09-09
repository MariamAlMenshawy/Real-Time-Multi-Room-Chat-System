from django.core.cache import cache

class CacheQuerysetMixin:
    cache_key = None
    cache_timeout = 60

    def get_queryset(self):
        if self.cache_key:
            cached = cache.get(self.cache_key)

            if cached is not None:
                print('✓ Cache HIT')
                return cached
            
            print('X Cache MISS - fetching from DB')
            queryset = super().get_queryset()
            cache.set(self.cache_key,queryset,self.cache_timeout)
            return queryset

        # لو مفيش مفتاح كاش اصلا
        return super().get_queryset()