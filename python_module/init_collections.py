import collections
print collections.Counter(['a', 'b', 'c', 'd'])
print collections.Counter({'a':2, 'b':3, 'c':4})
print collections.Counter(a=2, b = 3, c = 4)
print collections.Counter("abcdef")

c = collections.Counter()
print 'initial :', c

c.update("abcdaab")
print "Sequence: ", c

c.update({"a":1, "b":2})
print "Dict   :", c

for letter in 'abcde':
    print "{0} : {1}".format(letter, c[letter])

print list(c.elements())
