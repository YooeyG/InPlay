from my_module import find_index as fi, test

#HOW MODULES ARE LOCATED IN THIS ORDER
import sys
print(sys.path)
#directory containing the script
#python path environment variable
#standard lib directory; where you can import modules
#site packages directory for 3rd parth packages

courses = ['History', 'Math', 'Physics', 'CompSci']

index = fi(courses, "Math")
print(index)
print(test)