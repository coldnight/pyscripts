import collections

Person = collections.namedtuple('Person', 'name age gender')

print 'Type of Person:', type(Person)

bob = Person(name = 'Bob', age = 30, gender = 'male')
print '\nRepresentation:', bob

join = Person(name = 'Join', age = 29, gender = 'female')
print '\n Field by name:', join.name

print '\nFields by index:'
for p in (bob, join):
    print '%s is a %d year old %s' % p
