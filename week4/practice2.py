hh = ["23", 23, "a", 56, 9.0, 10.1111, (3, 0), 8]
total_number = 0
total_set = 0
total_string = 0
def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)
print(len(hh))
print(range(len(hh)))
for i in range(len(hh)):
    # print(i)
    # print(hh[i])
    # print(".")
    print(hh[i])
    print(is_number(hh[i]))
# print("=============================================")
# for datatype in hh:
#     print(datatype)
#     print(".")
# print(datatype)