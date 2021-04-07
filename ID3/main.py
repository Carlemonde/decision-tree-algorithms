import pandas as pd
import numpy as np
import sys
import math
import json
from copy import deepcopy
from decision_tree import *

dtree = DecisionTree()
dtree_path = []

#==================================
# ID3 algorithm.
def id3(data, target, parent='root', branch=None):
    global dtree  
    if data.empty:
        return dtree
    value = same_class(data, target)
    if value is not None:
        dtree.add_leaf(parent, value, branch)
        return dtree
    attr_best = get_best(data, target)
    dtree.new_node(parent,attr_best, branch)
    attr_list = data[attr_best].tolist() 
    partitions = unique(attr_list)
    for partition in partitions:
        subset = data.loc[data[attr_best]==partition].drop(attr_best, axis=1)
        id3(data=subset,target=target,parent=attr_best, branch=partition)

#==================================
# The best splitting attribute,
# according to information gain.
def get_best(data, target):
    data_info = compute_data_info(data,target)
    gain_list = {}
    for attr in data.drop(target, axis=1).columns:
        attr_info = compute_attr_info(attr, data, target)
        attr_gain = data_info - attr_info
        gain_list[attr] = attr_gain
    best = max(gain_list, key=lambda k:gain_list[k]) 
    return best

#==================================
# Check if tuples in 'data'
# belong to same class.
def same_class(data, target):
    target_list = data[target].tolist() 
    if target_list.count(target_list[0]) == len(target_list):
        return target_list[0]
    else:
        return None

#==================================
# Get unique values from list.
def unique(values):
    x = np.array(values)
    return np.unique(x)


#==================================
# The expected information needed 
# to classify a tuple in 'data'.
def compute_data_info(data, target):
    target_list = data[target].tolist() 
    groups = unique(target_list)
    data_info = 0
    for group in groups:
        prob = target_list.count(group) / len(target_list)
        data_info -= prob*(math.log(prob,2))
    return round(data_info,2)

#==================================
# The expected information needed 
# to classify a tuple in 'data',
# based on the partitioning by 'attr'.
def compute_attr_info(attr, data, target):
    attr_list = data[attr].tolist() 
    partitions = unique(attr_list)
    attr_info = 0
    for partition in partitions:
        prob = attr_list.count(partition) / len(attr_list)
        info_partition = compute_data_info(data.loc[data[attr] == partition],target)
        attr_info += prob*info_partition
    return round(attr_info,2)


#==================================
# Classify new instance against
# decision tree.
def classify(new_instance, decision_tree):
    global dtree_path
    dtree_copy = deepcopy(decision_tree)
    if isinstance(dtree_copy.root, Leaf):
        dtree_path.append(dtree_copy.root.value)
        return dtree_copy.root.value
    else:
        dtree_path.append(dtree_copy.root.value)
        branch_path = new_instance[dtree_copy.root.value]
        for branch, obj in dtree_copy.root.children.items():
            if branch == branch_path:
                temp_tree = DecisionTree()
                if isinstance(obj, Leaf):
                    return obj.value
                else:
                    temp_tree.add_node(parent='root',node=obj,branch=None)
                    result = classify(new_instance,temp_tree)
                    return result


if __name__ == "__main__": 
    args = sys.argv
    if len(args) < 3:
        sys.exit("Error - This program requires at least 2 arguments")

    filepath = args[1]
    class_label = args[2]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    else:
        sys.exit("Error - This program only accepts csv or excel files")

    id3(df,class_label)

    print("-------------------")
    print("Generated Tree:")
    print("-------------------")
    print(str(dtree))
    print("-------------------")

    if len(args) == 4:
        file_input = args[3]
        if file_input.endswith(".json"):
            with open(file_input) as json_file:
                tuple_input = json.load(json_file)
        else:
            sys.exit("Error - The tuple input must be on a JSON file")
  
        print("-------------------")
        print("New Instance Input:")
        print("-------------------")
        print(tuple_input)
        print("-------------------")

        result = classify(tuple_input, dtree)
        print("Classified as: "+str(result))

        print("Classification Path:")
        path_str = ""
        for item in dtree_path:
            path_str += "->"+str(item)
        print(path_str)



    

  
        
