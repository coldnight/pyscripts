import array
import pprint

a = array.array('i', xrange(3))

print 'Initial :', a
a.extend(xrange(3))
print 'Extended:', a

print 'Slice   :', a[2:5]

print 'Iterator:'
pprint.pprint(list(enumerate(a)))
