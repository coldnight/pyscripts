import collections

c = collections.Counter()

with open(r'/data/home/vim/.zhistory', 'rt') as f:
    for line in f:
        c.update({line.strip().lower().split(" ")[0]:1})

print 'Most Command:'

for letter, count in c.most_common(10):
    print "{0}: {1}".format(letter, count)
