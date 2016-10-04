import sys
from entity import DecisionTree

file = open("test.csv",encoding="GBK")
#读取表头
line = file.readline()

tree = DecisionTree()
test = []
result = []
for line in file.readlines():
    d = line.rstrip('\n').split(',')
    c = int(float(d[8]) // 5)
    test.append(d)
    result.append(c)
    tree.add(c,d)

#tree.load_tree()
tree.build_tree([True,False,False,False,True,True,True,True])
#classify,split,info = tree.ContinueClassify(0,tree.data)
#print(info)
i=0
while i<len(test):
    tree.test(test[i],result[i])
    i+=1