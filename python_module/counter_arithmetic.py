import collections

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'd'])
c2 = collections.Counter('alphabet')


print 'C1:', c1
print 'C2:', c2

print '\nCombined counts:'
print c1 + c2

print '\nSubtraction:'
print c1 - c2


print '\nintersection (taking positive minimums): '
print c1 & c2

print '\nUnion (taking maximums):'
print c1 | c2
