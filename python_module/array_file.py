import array
import binascii
import tempfile

a = array.array('i', xrange(5))
print 'A1:', a

output = tempfile.NamedTemporaryFile()
a.tofile(output.file)
output.flush()
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print 'Raw Contents:', binascii.hexlify(raw_data)

    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print 'A2:', a2