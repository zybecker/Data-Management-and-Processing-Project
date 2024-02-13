def separate_names(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    first_names = []
    last_names = []

    for line in lines:
        names = line.strip().split()
        if len(names) == 2:
            first, last = names
            first_names.append(first.lower())
            last_names.append(last.lower())

    return first_names, last_names

first_names, last_names  = separate_names('./names.txt')
first_names = first_names[:21]
last_names = last_names[:21]
# Generate tuples of all combinations of first names and last names
name_tuples = [(first, last) for first in first_names for last in last_names] 

# Print the tuples in a format that can be easily used in an SQL INSERT statement
for name_tuple in name_tuples:
    print(f"('{name_tuple[0]}', '{name_tuple[1]}'),")
