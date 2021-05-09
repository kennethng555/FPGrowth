from Node import Node


class Tree(object):
    def __init__(self, root=None, data=None):
        self.root = root
        self.head = root
        self.latest = data

    def insert_left(self, node):
        self.head.set_left(node)
        self.head = node

    def insert_right(self, node):
        self.head.set_right(node)
        self.head = node

    def insert_link(self, key, node):
        node.uplink = self.latest[key]
        self.latest[key].link = node
        self.latest[key] = node

    def reset_links(self):
        for key in self.latest.keys():
            while self.latest[key].uplink is not None:
                self.latest[key] = self.latest[key].uplink

    # generate the tree from the original database
    def generate(self, ordered):
        for i in range(len(ordered)):
            for j in range(len(ordered[i])):
                if self.head.get_left() == None:
                    new_left = Node(data=ordered[i][j], count=1, parent=self.head)
                    self.insert_left(new_left)
                    self.insert_link(ordered[i][j], self.head)
                else:
                    self.head = self.head.get_left()
                    if self.head.data == ordered[i][j]:
                        self.head.set_count(self.head.get_count() + 1)
                    else:
                        while self.head.get_right() is not None and self.head.get_data() != ordered[i][j]:
                            self.head = self.head.get_right()
                        if self.head.get_right() is None and self.head.get_data() != ordered[i][j]:
                            new_right = Node(data=ordered[i][j], count=1, parent=self.head.get_parent())
                            self.insert_right(new_right)
                            self.insert_link(ordered[i][j], self.head)
                        elif self.head.get_data() == ordered[i][j]:
                            self.head.set_count(self.head.get_count() + 1)
            self.head = self.root
        self.reset_links()

    # generate sub tree based on the path with the support of the path
    def generatesub(self, paths, support):
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                if paths[i][j] in self.latest:
                    if self.head.get_left() is not None:
                        self.head = self.head.get_left()
                        if self.head.data == paths[i][j]:
                            self.head.count = self.head.count + support[i]
                        else:
                            while self.head.get_right() is not None and self.head.get_data() != paths[i][j]:
                                self.head = self.head.get_right()
                            if self.head.get_right() is None and self.head.get_data() != paths[i][j]:
                                new_right = Node(paths[i][j], count=support[i], parent=self.head.get_parent())
                                self.insert_right(new_right)
                                self.insert_link(paths[i][j], self.head)
                            elif self.head.get_data() == paths[i][j]:
                                self.head.set_count(self.head.get_count() + support[i])
                    else:
                        new_left = Node(data=paths[i][j], count=support[i], parent=self.head)
                        self.insert_left(new_left)
                        self.insert_link(paths[i][j], self.head)
            self.head = self.root
        self.reset_links()

