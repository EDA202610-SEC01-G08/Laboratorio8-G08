from DataStructures.Tree import bst_node
from DataStructures.List import single_linked_list as ll
def new_map():
    return {"root": None}

def put(my_bst, key, value):
    """
    Agrega un nuevo nodo al árbol binario. Si la llave ya existe, se actualiza el valor del nodo.
    """
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def get(my_bst, key):
    """
    Busca un nodo en el árbol binario por su llave y devuelve su valor. Si la llave no existe, devuelve None.
    """
    return get_node(my_bst["root"], key)
    
def insert_node(node, key, value):
    if node is None:
        return bst_node.new_node(key, value)
    
    if key < node["key"]:
        node["left"] = insert_node(node["left"], key, value)
    elif key > node["key"]:
        node["right"] = insert_node(node["right"], key, value)
    else:
        node["value"] = value
    
    node["size"] = 1 + size(node["left"]) + size(node["right"])
    return node

def size(node):
    if node is None:
        return 0
    return node.get("size", 0)


def remove(my_bst, key):
    """
    Remueve un nodo del árbol binario por su llave.
    """
    my_bst["root"] = remove_node(my_bst["root"], key)
    return my_bst

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
        elif node["right"] is None:
            return node["left"]
        else:
            temp = min_value_node(node["right"])
            node["key"] = temp["key"]
            node["value"] = temp["value"]
            node["right"] = remove_node(node["right"], temp["key"])
    node["size"] = 1 + size(node["left"]) + size(node["right"])
    return node

def min_value_node(node):
    while node["left"] is not None:
        node = node["left"]
    return node

def get_node(root, key):
    if root is None:
        return None
    if key < root["key"]:
        return get_node(root["left"], key)
    elif key > root["key"]:
        return get_node(root["right"], key)
    else:
        return root["value"]

def contains(my_bst, key):
    """
    Verifica si una llave existe en el árbol binario.
    """
    return get(my_bst, key) is not None

def is_empty(my_bst):
    """
    Verifica si el árbol binario está vacío.
    """
    return my_bst["root"] is None

def key_set(my_bst):
    """
    Devuelve single linked list con las llaves del árbol binario. Usa key_set_tree() para construir la lista de llaves
    """
    keys_list = ll.new_list()
    key_set_tree(my_bst["root"], keys_list)
    return keys_list

def key_set_tree(node, keys_list):
    if node is None:
        return
    key_set_tree(node["left"], keys_list)
    ll.add_last(keys_list, node["key"])
    key_set_tree(node["right"], keys_list)


def value_set(my_bst):
    """
    Devuelve single linked list con los valores del árbol binario. Usa value_set_tree() para construir la lista de valores
    """
    values_list = ll.new_list()
    value_set_tree(my_bst["root"], values_list)
    return values_list

def value_set_tree(node, values_list):
    if node is None:
        return
    value_set_tree(node["left"], values_list)
    ll.add_last(values_list, node["value"])
    value_set_tree(node["right"], values_list)

def get_min(my_bst):
    """
    Devuelve la llave mínima del árbol binario.
    """
    return get_min_node(my_bst["root"])

def get_min_node(node):
    if node is None:
        return None
    if node["left"] is None:
        return node["key"]
    return get_min_node(node["left"])

def get_max(my_bst):
    """
    Devuelve la llave máxima del árbol binario.
    """
    return get_max_node(my_bst["root"])

def get_max_node(node):
    if node is None:
        return None
    if node["right"] is None:
        return node["key"]
    return get_max_node(node["right"])

def delete_min(my_bst):
    """
    Elimina la llave mínima del árbol binario.
    """
    return delete_min_tree(my_bst["root"])

def delete_min_tree(node):
    if node is None:
        return None
    if node["left"] is None:
        return node["right"]
    node["left"] = delete_min_tree(node["left"])
    return node

def delete_max(my_bst):
    """
    Elimina la llave máxima del árbol binario.
    """
    return delete_max_tree(my_bst["root"])

def delete_max_tree(node):
    if node is None:
        return None
    if node["right"] is None:
        return node["left"]
    node["right"] = delete_max_tree(node["right"])
    return node

def height(my_bst):
    """
    Devuelve la altura del árbol binario.
    """
    return height_tree(my_bst["root"])

def height_tree(node):
    if node is None:
        return 0
    left_height = height_tree(node["left"])
    right_height = height_tree(node["right"])
    return 1 + max(left_height, right_height)

def keys(my_bst, key_initial, key_final):
    """
    Devuelve single linked list con las llaves del árbol binario que estan en el rango [key_initial, key_final]
    """
    keys_list = ll.new_list()
    keys_range(my_bst["root"], key_initial, key_final, keys_list)
    return keys_list

def keys_range(node, key_initial, key_final, keys_list):
    if node is None:
        return
    if node["key"] > key_initial:
        keys_range(node["left"], key_initial, key_final, keys_list)
    if key_initial <= node["key"] <= key_final:
        ll.add_last(keys_list, node["key"])
    if node["key"] < key_final:
        keys_range(node["right"], key_initial, key_final, keys_list)

def values(my_bst, key_initial, key_final):
    """
    Devuelve single linked list con los valores del árbol binario que estan en el rango [key_initial, key_final]
    """
    values_list = ll.new_list()
    values_range(my_bst["root"], key_initial, key_final, values_list)
    return values_list

def values_range(node, key_initial, key_final, values_list):
    if node is None:
        return
    if node["key"] > key_initial:
        values_range(node["left"], key_initial, key_final, values_list)
    if key_initial <= node["key"] <= key_final:
        ll.add_last(values_list, node["value"])
    if node["key"] < key_final:
        values_range(node["right"], key_initial, key_final, values_list)

def floor(my_bst, key):
    """
    Devuelve la llave máxima del árbol binario que es menor o igual a la llave dada.
    """
    return floor_key(my_bst["root"], key)

def floor_key(node, key):
    if node is None:
        return None
    if node["key"] == key:
        return node["key"]
    if node["key"] > key:
        return floor_key(node["left"], key)
    if node["key"] < key:
        right_floor = floor_key(node["right"], key)
        if right_floor is None:
            return node["key"]
        return right_floor

def ceiling(my_bst, key):
    """
    Devuelve la llave mínima del árbol binario que es mayor o igual a la llave dada.
    """
    return ceiling_key(my_bst["root"], key)

def ceiling_key(node, key):
    if node is None:
        return None
    if node["key"] == key:
        return node["key"]
    if node["key"] < key:
        return ceiling_key(node["right"], key)
    if node["key"] > key:
        left_ceiling = ceiling_key(node["left"], key)
        if left_ceiling is None:
            return node["key"]
        return left_ceiling
def rank(my_bst, key):
    """
    Devuelve el número de llaves del árbol binario que son estrictamente menores que la llave dada.
    """
    return rank_key(my_bst["root"], key)

def rank_key(node, key):
    if node is None:
        return 0
    if node["key"] < key:
        return 1 + size(node["left"]) + rank_key(node["right"], key)
    elif node["key"] > key:
        return rank_key(node["left"], key)
    else:
        return size(node["left"])

def select(my_bst, k):
    """
    Devuelve la k-ésima llave más pequeña del árbol binario.
    """
    return select_key(my_bst["root"], k)

def select_key(node, k):
    if node is None:
        return None
    left_size = size(node["left"])
    if left_size == k:
        return node["key"]
    elif left_size > k:
        return select_key(node["left"], k)
    else:
        return select_key(node["right"], k - left_size - 1)
