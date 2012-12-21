import collections

with_class = collections.namedtuple("Person", 'name class age gender', rename = True)
print with_class._fields

two_ages = collections.namedtuple("Person", 'name class age gender age', rename = True)

print two_ages._fields
