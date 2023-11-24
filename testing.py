list1 = [1, 2, 3, 4, 5]
list2 = ["A", "B", "C", "D", "E"]
pointsList = list()
for i in range(len(list1)):
    pointsList.append(tuple((list1[i], list2[i])))

# These loops are just to show what is going on comment them out or delete them
for i in pointsList:
    print(i)
    print(f"The first element is {i[0]} and the second is {i[1]}")

for i, j in pointsList:
    if i == 3:
        print("3!")

# or let Python unpack the tuples - it depends what you want
for i, j in pointsList:
    print(i, j)

for point in pointsList:
    print(f"In the loop for find_neighbours of: {point}")
