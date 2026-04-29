import sys

collection = sys.argv[1]
output_file_path = sys.argv[2]

results = list()

for element in collection.split(','):
    element_file = open(element, "r")
    results.append(*element_file)
    element_file.close()

output_file = open(output_file_path, "w")
index = 0
for result in results:
    output_file.write(f'{result}\n')
    index += 1
output_file.close()

