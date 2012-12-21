import collections


def default_factor():
    return 'default value'


d = collections.defaultdict(default_factor, foo = 'bar')

print 'd:', d
print 'foo_>', d['foo']
print 'bar=>', d['bar']
