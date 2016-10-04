from math import log2
from math import inf
import json
class DecisionTree:
    data = {}
    attr_type = []
    Tree = {}

    def load_tree(self):
        file = open("test.json")
        self.Tree = json.load(file)

    def build_tree(self,attr_type):
        type_set = []
        i=0
        while i < len(attr_type):
            type_set.append({"order":i,"type":attr_type[i]})
            i += 1
        self.tree_builder(self.data,type_set,self.Tree)
        file = open("test.json","w")
        file.write(json.dumps(self.Tree,indent=1,ensure_ascii=False))

    def cut_tree(self,D):
        for key in D:
            if key != "attribute" and key != "split":
                if type(D[key]) == int:
                    return D[key]

    def tree_builder(self,D,attr_type,parent):
        data_info = self.Info(D)
        gain_rate = 0
        split = 0
        attr_sel = 0
        classify = {}
        i=0
        while i < len(attr_type):
            if attr_type[i]["type"]:
                classify1, split1, info1 = self.ContinueClassify(attr_type[i]["order"], D)
            else :
                classify1,info1 = self.DiscreteClassify(attr_type[i]["order"],D)
            split_info = self.SplitInfo(classify1)
            if split_info > 0:
                gain_rate1 = (data_info - info1) / split_info

                if gain_rate1 > gain_rate:
                    gain_rate = gain_rate1
                    classify = classify1
                    attr_sel = i
                    if attr_type[i]["type"]:
                        split = split1
            i+=1

        parent["attribution"] = attr_type[attr_sel]["order"]
        if attr_type[attr_sel]["type"]:
            parent["split"] = split

        if len(attr_type) > 1:
            for attr in classify:
                if len(classify[attr]) <= 1:#仅有一类
                    parent[attr] = list(classify[attr].keys())[0]
                else:
                    parent[attr] = {}
                    self.tree_builder(classify[attr], attr_type, parent[attr])

        else:
            for attr in classify:
                most = 0
                for k in classify[attr]:
                    if most < len(classify[attr][k]):
                        most = len(classify[attr][k])
                        o = k
                parent[attr] = o

    def Info(self,D):
        result = 0
        total = 0
        cList = []
        for i in D:
            cLen = len(D[i])
            if (cLen > 0):
                cList.append(cLen)
                total += cLen
        for c in cList:
            result -= (c / total) * log2(c / total)
        return result

    def InfoA(self,As):
        result = 0
        total = 0
        for a in As:
            total += len(As[a])
        for a in As:
            result += self.Info(As[a]) * len(As[a]) / total
        return result

    def SplitInfo(self,Ds):
        result = 0
        total = 0
        for j in Ds:
            total += len(Ds[j])
        for j in Ds:
            if (len(Ds[j]) > 0):
                result -= log2(len(Ds[j]) / total) * len(Ds[j]) / total
        return result

    def DiscreteClassify(self,attr,D):
        result = {}
        for i in D:#分类
            for t in D[i]:#属性的值
                if t[attr] not in result:
                    result[t[attr]] = {}
                if i in result[t[attr]]:
                    result[t[attr]][i].append(t)
                else:
                    result[t[attr]][i] = [t]
        return result,self.InfoA(result)

    def ContinueClassify(self,attr,D):
        result = {}
        order = []
        for i in D:
            order += D[i]
        order.sort(key=lambda x:float(x[attr]))

        classify = self.getClassify(order[0],D)
        InfoA = inf
        value_counter = 0
        i=1
        split = order[0][attr]
        mid = {}
        while i < len(order):#遍历已排序数组
            classify1 = self.getClassify(order[i],D)
            if classify != classify1:#分类产生变化，计算以该两值的中值作为分割的GainInfo
                value_counter += 1# 累计可能的分割点个数
                mid = {True:{},False:{}}
                classify = classify1
                split1 = (float(order[i][attr]) + float(order[i-1][attr]))/2
                for x in D:
                    for y in D[x]:
                            if x in mid[float(y[attr]) > split1]:
                                mid[float(y[attr]) > split1][x].append(y)
                            else:
                                mid[float(y[attr]) > split1][x] = [y]
                InfoA0 = self.InfoA(mid)
                if InfoA0 < InfoA:#InfoA越小，GainInfo越大
                    split = split1
                    InfoA = InfoA0
                    result = mid
            i += 1
        if value_counter == 0:
            return {classify:D},split,0
        else:
            return result,split,InfoA-log2(value_counter)/len(order)#纠正连续值得gain_info

    def add(self,c,d):
        if(c in self.data):
            self.data[c].append(d)
        else:
            self.data[c] = [d];

    def getClassify(self,item,D):
        for i in D:
            if D[i].count(item)>0:
                return i

    def test(self,data,tResult):
        test_tree = self.Tree
        while type(test_tree) != int:
            if "split" in test_tree:
                race = float(data[test_tree["attribution"]]) > test_tree["split"]
                if race in test_tree:
                    test_tree = test_tree[race]
                else:
                    print(data)
                    test_tree = -1
            else:
                test_tree = test_tree[data[test_tree["attribution"]]]
        print("%d:%d" % (test_tree,tResult))