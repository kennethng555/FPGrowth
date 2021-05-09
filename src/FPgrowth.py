from Node import Node
from Tree import Tree


# FP Growth
def FP_growth(tree, a, min_sup):
    # find if there is only 1 path
    while tree.head is not None and tree.head.get_right() is None:
        tree.head = tree.head.get_left()
    result = []

    if tree.head is None:  # if there is one path, print all combinations of all elements
        tree.head = tree.root
        print("Combination: ")
        print("----------", a, "---------")
        tree.head = tree.head.get_left()
        while tree.head is not None:
            sup = tree.head.count
            s = len(result)
            result.extend(result)
            for i in range(s, len(result)):
                if isinstance(result[i], str):
                    result[i] = [result[i]] + [tree.head.get_data()]
                else:
                    result[i] = result[i] + [tree.head.get_data()]
            result.append(tree.head.get_data())
            tree.head = tree.head.get_left()

        for i in range(len(result)):
            if isinstance(result[i], str):
                result[i] = [result[i]] + [', '.join(a)]
            else:
                result[i] = result[i] + [', '.join(a)]
            print(', '.join(result[i]), ": ", sup)
        print('\n')
    else:  # if there is more than one path use the dictionary to look up
        condpatbase = dict()  # set the leaves and form a new tree based on the paths to the
        condfreqpat = dict()  # node
        for key in tree.latest.keys():
            if tree.latest[key].count >= min_sup:
                current = tree.latest[key].link
                paths = []
                common = []
                supports = []
                subcondpatbase = dict()
                while current is not None:
                    path = []
                    start = current
                    print(key, end='\t')
                    current = current.get_parent()
                    while current.data != []:
                        if current.data in subcondpatbase:
                            subcondpatbase[current.data].count = subcondpatbase[current.data].count + start.count
                        else:
                            subcondpatbase[current.data] = Node(current.data, start.count)
                        path.insert(0, current.data)
                        print(current.get_data(), end=' ')
                        current = current.get_parent()
                    current = start
                    if path != []:
                        paths.append(path)
                        supports.append(current.count)
                        print(current.count)
                    else:
                        print('\n')
                    current = current.link

                for subkey in list(subcondpatbase.keys()):
                    if subcondpatbase[subkey].count < min_sup:
                        del subcondpatbase[subkey]

                if subcondpatbase != {}:  # if the conditional path base is not empty,
                    print()  # generate the tree and pass the tree to
                    root = Node(data=[])  # recursive call to FP Growth
                    btree = Tree(root, subcondpatbase)
                    if paths != []:
                        btree.generatesub(paths, supports)
                        condpatbase[key] = (paths, supports)
                        a.append(key)
                        FP_growth(btree, a, min_sup)
                        condfreqpat[key] = (common, min_sup)
                        a.pop()
                else:
                    print("Combination: ")
                    print("----------", a + [key], "---------")
                    print(', '.join(a + [key]), ": ", tree.latest[key].count)
                    print('\n')
        print("------------------------------------------------")
        print("--------------------New Path--------------------")
        print("------------------------------------------------")
