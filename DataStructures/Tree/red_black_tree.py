from DataStructures.Map import map_linear_probing as lp 
from DataStructures.Tree import rbt_node
from DataStructures.List import single_linked_list as slt

RED = rbt_node.RED
BLACK = rbt_node.BLACK

def new_map():
    lp_map = lp.new_map(16, 0.5)
    lp_map['root'] = None
    lp_map['type'] = "RBT"
    return lp_map

def is_red(node):
    if node is None:
        return False
    return rbt_node.is_red(node)

def size_tree(node):
    if node is None:
        return 0
    return node.get("size", 1)

def rotate_left(node):
    x = node["right"]
    node["right"] = x["left"]
    x["left"] = node
    x["color"] = node["color"]
    node["color"] = RED
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return x

def rotate_right(node):
    x = node["left"]
    node["left"] = x["right"]
    x["right"] = node
    x["color"] = node["color"]
    node["color"] = RED
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return x

def flip_colors(node):
    node["color"] = not node["color"]
    if node["left"] is not None:
        node["left"]["color"] = not node["left"]["color"]
    if node["right"] is not None:
        node["right"]["color"] = not node["right"]["color"]

def put(my_rbt, key, value):
    my_rbt['root'] = insert_node(my_rbt['root'], key, value)
    if my_rbt['root'] is not None:
        my_rbt['root']["color"] = BLACK
    return my_rbt

def insert_node(root, key, value):
    if root is None:
        return rbt_node.new_node(key, value, RED)
    
    if key < root["key"]:
        root["left"] = insert_node(root["left"], key, value)
    elif key > root["key"]:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
    
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
    
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def get(my_rbt, key):
    return get_node(my_rbt['root'], key)

def get_node(root, key):
    if root is None:
        return None
    if key < root["key"]:
        return get_node(root["left"], key)
    elif key > root["key"]:
        return get_node(root["right"], key)
    else:
        return root["value"]

def remove(my_rbt, key):
    if not contains(my_rbt, key):
        return my_rbt
    
    if my_rbt['root'] is not None:
        if not is_red(my_rbt['root']["left"]) and not is_red(my_rbt['root']["right"]):
            my_rbt['root']["color"] = RED
    
    my_rbt['root'] = remove_node(my_rbt['root'], key)
    
    if my_rbt['root'] is not None:
        my_rbt['root']["color"] = BLACK
    return my_rbt

def remove_node(root, key):
    if root is None:
        return None
    
    if key < root["key"]:
        if root["left"] is not None:
            if not is_red(root["left"]) and not is_red(root["left"]["left"]):
                root = move_red_left(root)
        root["left"] = remove_node(root["left"], key)
    else:
        if is_red(root["left"]):
            root = rotate_right(root)
        if key == root["key"] and root["right"] is None:
            return None
        if root["right"] is not None:
            if not is_red(root["right"]) and not is_red(root["right"]["left"]):
                root = move_red_right(root)
        if key == root["key"]:
            min_node = get_min_node(root["right"])
            root["key"] = min_node["key"]
            root["value"] = min_node["value"]
            root["right"] = delete_min_node(root["right"])
        else:
            root["right"] = remove_node(root["right"], key)
    
    return balance(root)

def move_red_left(node):
    flip_colors(node)
    if node["right"] is not None and is_red(node["right"]["left"]):
        node["right"] = rotate_right(node["right"])
        node = rotate_left(node)
        flip_colors(node)
    return node

def move_red_right(node):
    flip_colors(node)
    if node["left"] is not None and is_red(node["left"]["left"]):
        node = rotate_right(node)
        flip_colors(node)
    return node

def balance(node):
    if node is None:
        return None
    
    if is_red(node["right"]) and not is_red(node["left"]):
        node = rotate_left(node)
    if is_red(node["left"]) and node["left"] is not None and is_red(node["left"]["left"]):
        node = rotate_right(node)
    if is_red(node["left"]) and is_red(node["right"]):
        flip_colors(node)
    
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return node

def contains(my_rbt, key):
    return get(my_rbt, key) is not None

def size(my_rbt):
    return size_tree(my_rbt['root'])

def is_empty(my_rbt):
    return my_rbt['root'] is None

def key_set(my_rbt):
    lista = slt.new_list()
    node = my_rbt['root']
    key_set_tree(node, lista)
    return lista
    
def key_set_tree(node, lista):
    if node is not None:
        key_set_tree(node["left"], lista)
        slt.add_last(lista, node["key"])
        key_set_tree(node["right"], lista)
        
def value_set(my_rbt):
    lista = slt.new_list()
    node = my_rbt['root']
    value_set_tree(node, lista)
    return lista

def value_set_tree(node, lista):
    if node is not None:
        value_set_tree(node["left"], lista)
        slt.add_last(lista, node["value"])
        value_set_tree(node["right"], lista)

def get_min(my_rbt):
    node = my_rbt['root']
    if node is None:
        return None
    return get_min_node(node)["key"]

def get_min_node(node):
    if node["left"] is None:
        return node
    return get_min_node(node["left"])

def get_max(my_rbt):
    node = my_rbt['root']
    if node is None:
        return None
    else:
        max_key = get_max_node(node)
        return max_key

def get_max_node(node):
    if node["right"] is None:
        return node["key"]
    return get_max_node(node["right"])

def delete_min(my_rbt):
    if my_rbt['root'] is None:
        return my_rbt
    my_rbt['root'] = delete_min_node(my_rbt['root'])
    if my_rbt['root'] is not None:
        my_rbt['root']["color"] = BLACK
    return my_rbt

def delete_min_node(node):
    if node["left"] is None:
        return None
    if not is_red(node["left"]) and not is_red(node["left"]["left"]):
        node = move_red_left(node)
    node["left"] = delete_min_node(node["left"])
    return balance(node)

def delete_max(my_rbt):
    if my_rbt['root'] is None:
        return my_rbt
    my_rbt['root'] = delete_max_node(my_rbt['root'])
    if my_rbt['root'] is not None:
        my_rbt['root']["color"] = BLACK
    return my_rbt

def delete_max_node(node):
    if is_red(node["left"]):
        node = rotate_right(node)
    if node["right"] is None:
        return None
    if not is_red(node["right"]) and not is_red(node["right"]["left"]):
        node = move_red_right(node)
    node["right"] = delete_max_node(node["right"])
    return balance(node)

def floor(my_rbt, key):
    node = my_rbt['root']
    if node is None:
        return None
    floor_key = floor_node(node, key)
    return floor_key

def floor_node(node, key):
    if node is None:
        return None
    if key == node["key"]:
        return node["key"]
    if key < node["key"]:
        return floor_node(node["left"], key)
    floor_right = floor_node(node["right"], key)
    if floor_right is not None:
        return floor_right
    else:
        return node["key"]
    
def ceiling(my_rbt, key):
    node = my_rbt['root']
    if node is None:
        return None
    result = ceiling_key(node, key)
    return result

def ceiling_key(node, key):
    if node is None:
        return None
    if key == node["key"]:
        return node["key"]
    if key > node["key"]:
        return ceiling_key(node["right"], key)
    ceiling_left = ceiling_key(node["left"], key)
    if ceiling_left is not None:
        return ceiling_left
    else:
        return node["key"]
    
def select(my_bst, pos):
    node = my_bst['root']
    if node is None:
        return None
    result = select_key(node, pos)
    if result is not None:
        return result["key"]
    else:
        return None
    
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
    
def rank(my_bst, key):
    node = my_bst['root']
    if node is None:
        return 0
    return rank_keys(node, key)

def rank_keys(node, key):
    if node is None:
        return 0
    if key < node["key"]:
        return rank_keys(node["left"], key)
    elif key > node["key"]:
        left_size = size_tree(node["left"])
        return 1 + left_size + rank_keys(node["right"], key)
    else:
        return size_tree(node["left"])
    
def height(my_rbt):
    node = my_rbt['root']
    if node is None:
        return -1
    return height_tree(node)

def height_tree(node):
    if node is None:
        return -1
    left_height = height_tree(node["left"])
    right_height = height_tree(node["right"])
    return 1 + max(left_height, right_height)

def keys(my_bst, key_initial, key_final):
    lista = slt.new_list()
    keys_range(my_bst['root'], key_initial, key_final, lista)
    return lista

def keys_range(node, key_initial, key_final, lista):
    if node is None:
        return
    if key_initial < node["key"]:
        keys_range(node["left"], key_initial, key_final, lista)
    if key_initial <= node["key"] <= key_final:
        slt.add_last(lista, node["key"])
    if key_final > node["key"]:
        keys_range(node["right"], key_initial, key_final, lista)
        
def values(my_bst, key_initial, key_final):
    lista = slt.new_list()
    values_range(my_bst['root'], key_initial, key_final, lista)
    return lista

def values_range(node, key_initial, key_final, lista):
    if node is None:
        return
    if key_initial < node["key"]:
        values_range(node["left"], key_initial, key_final, lista)
    if key_initial <= node["key"] <= key_final:
        slt.add_last(lista, node["value"])
    if key_final > node["key"]:
        values_range(node["right"], key_initial, key_final, lista)
