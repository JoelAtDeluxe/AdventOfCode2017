from typing import List


class Node(object):
    def __init__(self, name:str, weight:int, child_names=[]):
        self.name:str = name
        self.weight:int = weight
        self.child_names:List[str] = child_names
        self.child_nodes = {}

    def set_child(self, name, value):
        self.child_nodes[name] = value
        self.child_names = [n for n in self.child_names if n != name]


def parse_file(file_path):
    nodes = []
    added_node_names = []
    with open(file_path, 'r') as fh:
        for line in fh:
            components = [s.strip() for s in line.split('->')]
            named_children = []
            if len(components) > 1:
                named_children = [s.strip() for s in components[1].split(',')]
            node_name, weight = components[0].split(' ')
            weight = int(weight[1:len(weight)-1])
            node = Node(node_name, weight, named_children)
            
            if node_name not in added_node_names:
                nodes.append(node)
                added_node_names.append(node.name)

    return nodes


def main():
    unsorted_nodes = parse_file('./input.txt')

    

    # hashed = { node.name: node for node in unsorted_nodes }
    
    # for k, v in hashed.items():
        
    #     for name in v.child_names:
    #         v.set_child()

    # Somthing is wrong with this
    orphans = [node for node in unsorted_nodes if node.child_names == []]
    adults = [node for node in unsorted_nodes if node.child_names != []]
    while len(adults) > 0:
        # import pdb; pdb.set_trace()
        for adult in adults:
            kid_names = adult.child_names
            kids = [node for node in orphans if node.name in kid_names]
            orphans = [node for node in orphans if node.name not in kid_names]
            for kid in kids:
                adult.set_child(kid.name, kid)
        orphans = [node for node in adults if node.child_names == []] 
        adults = [node for node in adults if node.child_names != []]
    
    elder = orphans[0]
    print(elder.name)    

if __name__ == "__main__":
    main()