from DataStructures.Map import map_linear_probing as lp 
from DataStructures.Tree import rbt_node
from DataStructures.List import single_linked_list as sl

RED = rbt_node.RED
BLACK = rbt_node.BLACK

def new_map():
    """
    Crea una tabla de simbolos ordenada basa en un árbol rojo-negro (RBT) vacia

    Se crea una tabla de simbolos ordenada con root = None y type = "RBT"
    """
    lp_map = lp.new_map(16, 0.5)
    lp_map['root'] = None
    lp_map['type'] = "RBT"
    return lp_map

def is_red(node):
    """
    Verifica si un nodo es rojo.
    """
    if node is None:
        return False
    return rbt_node.is_red(node)

def size_tree(node):
    """
    Retorna el tamaño del subárbol.
    """
    if node is None:
        return 0
    return node["size"]


def rotate_left(node):
    """
    Rotación a la izquierda.
    """
    x = node["right"]
    node["right"] = x["left"]
    x["left"] = node
    x["color"] = node["color"]
    node["color"] = RED
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return x

def rotate_right(node):
    """
    Rotación a la derecha.
    """
    x = node["left"]
    node["left"] = x["right"]
    x["right"] = node
    x["color"] = node["color"]
    node["color"] = RED
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    return x

def flip_colors(node):
    """
    Invierte los colores del nodo y sus hijos.
    """
    node["color"] = not node["color"]
    if node["left"] is not None:
        node["left"]["color"] = not node["left"]["color"]
    if node["right"] is not None:
        node["right"]["color"] = not node["right"]["color"]

def put(my_rbt, key, value):
    """
    Inserta un par clave/valor en el árbol.
    Si la clave ya existe, actualiza el valor. Usa insert_node()
    """
    my_rbt['root'] = insert_node(my_rbt['root'], key, value)
    if my_rbt['root'] is not None:
        my_rbt['root']["color"] = BLACK
    return my_rbt

def insert_node(root, key, value):
    """
    Ingresa una pareja llave,valor. Si la llave ya existe, se reemplaza el valor.
    Es usada en la función insert()
    """
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
    if is_red(root["left"]) and root["left"] is not None and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
    
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def get(my_rbt, key):
    """
    Retorna el valor asociado a la llave. 
    Usa get_node() para buscar la llave en el arbol
    """
    return get_node(my_rbt['root'], key)

def get_node(root, key):
    """
    Busca un nodo en el árbol.
    """
    if root is None:
        return None
    if key < root["key"]:
        return get_node(root["left"], key)
    elif key > root["key"]:
        return get_node(root["right"], key)
    else:
        return root["value"]

def remove(my_rbt, key):
    """
    Elimina un nodo del árbol.
    Usa remove_node() para eliminar el nodo
    """
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
    """
    Elimina un nodo del árbol.
    """
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
    """
    Mueve un enlace rojo a la izquierda.
    """
    flip_colors(node)
    if node["right"] is not None and is_red(node["right"]["left"]):
        node["right"] = rotate_right(node["right"])
        node = rotate_left(node)
        flip_colors(node)
    return node

def move_red_right(node):
    """
    Mueve un enlace rojo a la derecha.
    """
    flip_colors(node)
    if node["left"] is not None and is_red(node["left"]["left"]):
        node = rotate_right(node)
        flip_colors(node)
    return node

def balance(node):
    """
    Restaura el balance del árbol rojo-negro.
    """
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

def get_min_node(node):
    """
    Obtiene el nodo con la llave mínima.
    """
    if node["left"] is None:
        return node
    return get_min_node(node["left"])

def delete_min_node(node):
    """
    Elimina el nodo con la llave mínima.
    """
    if node["left"] is None:
        return None
    if not is_red(node["left"]) and not is_red(node["left"]["left"]):
        node = move_red_left(node)
    node["left"] = delete_min_node(node["left"])
    return balance(node)

def contains(my_rbt, key):
    """
    Verifica si la llave está en el árbol. 
    Usa get() para buscar la llave en el arbol
    """
    return get(my_rbt, key) is not None

def size(my_rbt):
    """
    Retorna el número de entradas en el árbol.
    Usa size_tree() para contar los nodos
    """
    return size_tree(my_rbt['root'])

def is_empty(my_rbt):
    """
    Verifica si el árbol está vacío.
    """
    return my_rbt['root'] is None

def key_set(my_rbt):
    """
    Retorna un single linked list con las llaves del árbol. Usa key_set_tree()
    """
    keys_list = sl.new_list()
    key_set_tree(my_rbt['root'], keys_list)
    return keys_list
 
def key_set_tree(node, keys_list):
    """
    Retorna un single linked list con las llaves del árbol.
    """
    if node is None:
        return
    key_set_tree(node['left'], keys_list)
    sl.add_last(keys_list, node['key'])
    key_set_tree(node['right'], keys_list)

def value_set(my_rbt):
    """
    Retorna un single linked list con los valores del árbol. Usa value_set_tree()
    """
    values_list = sl.new_list()
    value_set_tree(my_rbt['root'], values_list)
    return values_list
 
def value_set_tree(node, values_list):
    """
    Retorna un single linked list con los valores del árbol.
    """
    if node is None:
        return
    value_set_tree(node['left'], values_list)
    sl.add_last(values_list, node['value'])
    value_set_tree(node['right'], values_list)

def get_min(my_rbt):
    """
    Retorna la llave mínima. Usa get_min_node()
    """
    if my_rbt['root'] is None:
        return None
    node = get_min_node(my_rbt['root'])
    return node['key']



def get_max(my_rbt):
    """
    Retorna la llave máxima. Usa get_max_node()
    """
    if my_rbt['root'] is None:
        return None
    node = get_max_node(my_rbt['root'])
    return node['key']

def get_max_node(node):
    """
    Obtiene el nodo con la llave máxima.
    """
    if node is None:
        return None
    if node["right"] is None:
        return node
    return get_max_node(node["right"])

def delete_min(my_rbt):
    """
    Elimina el nodo con la llave mínima. Usa delete_min_node()
    """
    if my_rbt['root'] is None:
        return my_rbt
    if not is_red(my_rbt['root']['left']) and not is_red(my_rbt['root']['right']):
        my_rbt['root']['color'] = RED
    my_rbt['root'] = delete_min_node(my_rbt['root'])
    if my_rbt['root'] is not None:
        my_rbt['root']['color'] = BLACK
    return my_rbt

def delete_max(my_rbt):
    """
    Elimina el nodo con la llave máxima. Usa delete_max_node()
    """
    if my_rbt['root'] is None:
        return my_rbt
    if not is_red(my_rbt['root']['left']) and not is_red(my_rbt['root']['right']):
        my_rbt['root']['color'] = RED
    my_rbt['root'] = delete_max_node(my_rbt['root'])
    if my_rbt['root'] is not None:
        my_rbt['root']['color'] = BLACK
    return my_rbt

def delete_max_node(node):
    """
    Elimina el nodo con la llave máxima.
    """
    if is_red(node['left']):
        node = rotate_right(node)
    if node['right'] is None:
        return None
    if not is_red(node['right']) and not is_red(node['right']['left']):
        node = move_red_right(node)
    node['right'] = delete_max_node(node['right'])
    return balance(node)

def floor(my_rbt, key):
    """
    Retorna el nodo con la llave máxima menor o igual a la clave. Usa floor_key()
    """
    return floor_key(my_rbt['root'], key)

def floor_key(root, key):
    """
    Obtiene la llave máxima menor o igual a la clave.
    """
    if root is None:
        return None
    if key == root['key']:
        return root['key']
    if key < root['key']:
        return floor_key(root['left'], key)
    right_floor = floor_key(root['right'], key)
    if right_floor is not None:
        return right_floor
    return root['key']

def ceiling(my_rbt, key):
    """
    Retorna el nodo con la llave mínima mayor o igual a la clave. Usa ceiling_key()
    """
    return ceiling_key(my_rbt['root'], key)

def ceiling_key(root, key):
    """
    Obtiene la llave mínima mayor o igual a la clave.
    """
    if root is None:
        return None
    if key == root['key']:
        return root['key']
    if key > root['key']:
        return ceiling_key(root['right'], key)
    left_ceiling = ceiling_key(root['left'], key)
    if left_ceiling is not None:
        return left_ceiling
    return root['key']

def select(my_rbt, pos):
    """
    Retorna el nodo con la posición pos en el árbol. Usa select_key()
    """
    return select_key(my_rbt['root'], pos)

def select_key(root, pos):
    """
    Obtiene la llave en la posición pos en el árbol.
    """
    if root is None:
        return None
    left_size = size_tree(root['left'])
    if pos < left_size:
        return select_key(root['left'], pos)
    if pos == left_size:
        return root['key']
    return select_key(root['right'], pos - left_size - 1)

def rank(my_rbt, key):
    """
    Retorna la posición de la llave en el árbol. Usa rank_keys()
    """
    return rank_keys(my_rbt['root'], key)

def rank_keys(root, key):
    """
    Obtiene la posición de la llave en el árbol.
    """
    if root is None:
        return 0
    if key < root['key']:
        return rank_keys(root['left'], key)
    if key == root['key']:
        return root['size']
    return rank_keys(root['right'], key) + root['size'] + 1

def height(my_rbt):
    """
    Retorna la altura del árbol. Usa height_tree()
    """
    return height_tree(my_rbt['root'])

def height_tree(node):
    """
    Obtiene la altura del nodo.
    """
    if node is None:
        return -1
    return 1 + max(height_tree(node['left']), height_tree(node['right']))

def keys(my_rbt, key_initial, key_final):
    """
    Retorna una lista con todas las llaves del árbol entre key_initial y key_final. Usa keys_range()
    """
    return keys_range(my_rbt['root'], key_initial, key_final)

def keys_range(node, key_initial, key_final):
    """
    Obtiene una lista con todas las llaves del nodo entre key_initial y key_final.
    """
    if node is None:
        return []
    if node['key'] >= key_initial and node['key'] <= key_final:
        return keys_range(node['left'], key_initial, key_final) + [node['key']] + keys_range(node['right'], key_initial, key_final)
    if node['key'] < key_initial:
        return keys_range(node['right'], key_initial, key_final)
    return keys_range(node['left'], key_initial, key_final)

def values(my_rbt, key_initial, key_final):
    """
    Retorna una lista con todos los valores del árbol entre key_initial y key_final. Usa values_range()
    """
    return values_range(my_rbt['root'], key_initial, key_final)

def values_range(node, key_initial, key_final):
    """
    Obtiene una lista con todos los valores del nodo entre key_initial y key_final.
    """
    if node is None:
        return []
    if node['key'] >= key_initial and node['key'] <= key_final:
        return values_range(node['left'], key_initial, key_final) + [node['value']] + values_range(node['right'], key_initial, key_final)
    if node['key'] < key_initial:
        return values_range(node['right'], key_initial, key_final)
    return values_range(node['left'], key_initial, key_final)

