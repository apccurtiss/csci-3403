from difflib import Differ 

file_1 = open('differ_test_1.txt', 'r')
file_2 = open('differ_test_2.txt', 'r')
file_out = open('differ_output.txt', 'w')
  
# with open('file1.txt') as file_1, open('file2.txt') as file_2: 
differ = Differ() 

for line in differ.compare(file_1.readlines(), file_2.readlines()): 
    # print(line) 
    file_out.write(line)
    # file_out.write("\n")

file_1.close() 
file_2.close() 
file_out.close() 