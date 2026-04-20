from DataStructures.Tree import bst_node
from DataStructures.List import single_linked_list as slt

def new_map():
    return {"root": None}

def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def insert_node(node, key, value):
    if node is None:
        return bst_node.new_node(key, value)
    
    if key < node["key"]:
        node["left"] = insert_node(node["left"], key, value)
    elif key > node["key"]:
        node["right"] = insert_node(node["right"], key, value)
    else:
        node["value"] = value
    
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return node

def size(tree):
    if tree["root"] is None:
        return 0
    return tree["root"]["size"]

def size_tree(node):
    if node is None:
        return 0
    return node.get("size", 1)


def min_value_node(node):
    while node["left"] is not None:
        node = node["left"]
    return node

def get(my_bst, key):
    return get_node(my_bst["root"], key)

def get_node(root, key):
    if root is None:
        return None
    if key < root["key"]:
        return get_node(root["left"], key)
    elif key > root["key"]:
        return get_node(root["right"], key)
    else:
        return root["value"]
    
def remove(tree,key):
    node = tree["root"]
    tree["root"] = remove_node(node,key)
    return tree

def remove_node(node, key):
    if node is None:
        return None
    if key < node["key"]:
        node["left"] = remove_node(node["left"], key)
    elif key > node["key"]:
        node["right"] = remove_node(node["right"], key)
    else:
        if node["left"] is None:
            return node["right"]
        if node["right"] is None:
            return node["left"]

        temp = min_value_node(node["right"])
        node["key"] = temp["key"]
        node["value"] = temp["value"]
        node["right"] = remove_node(node["right"], temp["key"])

    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return node

def contains(tree,key):
    return not get(tree,key) is None

def is_empty(tree):
    return tree["root"] is None

def key_set(tree):
    lista = slt.new_list()
    node = tree["root"]
    key_set_node(node, lista)
    return lista
    
def key_set_node(node, lista):
    if node is None:
        return
    key_set_node(node["left"], lista)
    slt.add_last(lista,node["key"])
    key_set_node(node["right"], lista)
    
def value_set(tree):
    lista = slt.new_list()
    node = tree["root"]
    value_set_node(node, lista)
    return lista
    
def value_set_node(node, lista):
    if node is None:
        return
    value_set_node(node["left"], lista)
    slt.add_last(lista,node["value"])
    value_set_node(node["right"], lista)

def get_min(tree):
    node = tree["root"]
    return min_tree(node)
    
def min_tree(node):
    if node is None:
        return None
    while node["left"] is not None:
        node = node["left"]
    return node["key"]

def get_max(tree):
    node = tree["root"]
    return max_tree(node)

def max_tree(node):
    if node is None:
        return None
    while node["right"] is not None:
        node = node["right"]
    return node["key"]

def delete_min(tree):
    tree["root"] = delete_min_tree(tree["root"])
    return tree

def delete_min_tree(node):

    if node is None:
        return None

    if node["left"] is None:
        return node["right"]

    node["left"] = delete_min_tree(node["left"])
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])

    return node

def delete_max(tree):
    tree["root"] = delete_max_tree(tree["root"])
    return tree

def delete_max_tree(node):

    if node is None:
        return None

    if node["right"] is None:
        return node["left"]

    node["right"] = delete_max_tree(node["right"])
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])

    return node

def floor(tree,key):
    node = tree["root"]
    return floor_node(node,key)

def floor_node(node, key):
    if node is None:
        return None
    if node["key"] == key:
        return node["key"]

    if key < node["key"]:
        return floor_node(node["left"], key)
    temp = floor_node(node["right"], key)
    if temp is not None:
        return temp
    return node["key"]
    
def ceiling(tree,key):
    node = tree["root"]
    return ceiling_node(node,key)

def ceiling_node(node, key):
    if node is None:
        return None
    if node["key"] == key:
        return node["key"]
    if key > node["key"]:
        return ceiling_node(node["right"], key)
    temp = ceiling_node(node["left"], key)
    if temp is not None:
        return temp
    return node["key"]
    
def select(tree, pos):
    node = select_key(tree["root"], pos)
    if node is None:
        return None
    return node["key"]

def select_key(node, pos):
    if node is None:
        return None
    left_size = size_tree(node["left"])
    if pos < left_size:
        return select_key(node["left"], pos)
    elif pos > left_size:
        return select_key(node["right"], pos - left_size - 1)
    else:
        return node
    
def rank(tree, key):
    return rank_key(tree["root"], key)

def rank_key(node, key):
    if node is None:
        return 0
    if key < node["key"]:
        return rank_key(node["left"], key)
    elif key > node["key"]:
        return 1 + size_tree(node["left"]) + rank_key(node["right"], key)
    else:
        return size_tree(node["left"])
    
def height(tree):
    return height_tree(tree["root"])

def height_tree(node):
    if node is None:
        return 0
    left = height_tree(node["left"])
    right = height_tree(node["right"])
    return 1 + max(left, right)

def keys(tree,minimo,maximo):
    lista = slt.new_list()
    keys_range(tree["root"],minimo,maximo, lista)
    return lista

def keys_range(node, minimo, maximo, lista):
    if node is None:
        return
    if minimo < node["key"]:
        keys_range(node["left"], minimo, maximo, lista)
    if minimo <= node["key"] <= maximo:
        slt.add_last(lista, node["key"])
    if maximo > node["key"]:
        keys_range(node["right"], minimo, maximo, lista)
        
def values(tree,minimo,maximo):
    lista = slt.new_list()
    values_range(tree["root"],minimo,maximo, lista)
    return lista

def values_range(node, minimo, maximo, lista):
    if node is None:
        return
    if minimo < node["key"]:
        values_range(node["left"], minimo, maximo, lista)
    if minimo <= node["key"] <= maximo:
        slt.add_last(lista, node["value"])
    if maximo > node["key"]:
        values_range(node["right"], minimo, maximo, lista)