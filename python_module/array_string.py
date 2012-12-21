import array
import binascii

s = 'This is the array'
a = array.array('c', s)

print 'As String:', s
print 'As array:', a
print 'As Hex   :', binascii.hexlify(a)
