print "Enter '3' numbers to return the maximum of all three!"
one = int(raw_input("Enter your 'first' number: "))
two = int(raw_input("Enter your 'second' number: "))
three = int(raw_input("Enter your 'third' number: "))
max_of_3 = []
max_of_3.append(one), max_of_3.append(two), max_of_3.append(three)
max_of_3.sort()
print "The max number is:" ,max_of_3[2]
