from DataStructures.Map import map_linear_probing as lp 
from DataStructures.Tree import rbt_node

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

