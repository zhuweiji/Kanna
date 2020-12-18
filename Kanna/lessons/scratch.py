from services import listify


a = ['1', '2', 'e']
b = [1,2,3]
c = "'1', '2', '3'"

foo = [a,b,c]
for arr in foo:
    print(listify(arr))