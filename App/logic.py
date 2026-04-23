"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import os
import csv
import datetime

# DONE Realice la importación del Árbol Rojo Negro
# DONE Realice la importación de ArrayList (al) o SingleLinked (sl) como estructura de datos auxiliar para sus requerimientos
# DONE Realice la importación de LinearProbing (lp) o Separate Chaining (sp) como estructura de datos auxiliar para sus requerimientos

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as slt
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Map import map_linear_probing as lp



def new_logic():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {"crimes": None,
                "dateIndex": None,
                "areaIndex": None,
                }

    analyzer["crimes"] = al.new_list()
    analyzer["dateIndex"] = rbt.new_map()
    # DONE Crear el índice ordenado por áreas reportadas
    analyzer["areaIndex"] = rbt.new_map()
    return analyzer

# Funciones para realizar la carga

def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer



# Funciones para agregar informacion al analizador


def add_crime(analyzer, crime):
    """
    funcion que agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    # DONE Actualizar el indice por areas reportadas
    update_area_index(analyzer['areaIndex'], crime)
    return analyzer

def update_area_index(map, crime):
    """
    actualiza el indice de areas reportadas con un nuevo crimen
    si el area ya existe en el indice, se adiciona el crimen a la lista
    si el area es nueva, se crea una entrada para el indice y se adiciona
    y si el area son ["", " ", None] se utiliza el valor por defecto 9999
    """
    # DONE Implementar actualizacion del indice por areas reportadas
    area = crime.get("REPORTING_AREA")
    if area == "" or area == " " or area is None:
        area = 9999
    else:
        area = int(area)
    entry = rbt.get(map, area)
    if entry is None:
        datentry = new_data_entry(crime)
        rbt.put(map, area, datentry)
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map


def update_date_index(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = rbt.get(map, crimedate.date())
    if entry is None:
        datentry = new_data_entry(crime)
        rbt.put(map, crimedate.date(), datentry)
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map


def add_date_index(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry["lstcrimes"]
    al.add_last(lst, crime)
    offenseIndex = datentry["offenseIndex"]
    offentry = lp.get(offenseIndex, crime["OFFENSE_CODE_GROUP"])
    if (offentry is None):
        entry = new_offense_entry(crime["OFFENSE_CODE_GROUP"], crime)
        al.add_last(entry["lstoffenses"], crime)
        lp.put(offenseIndex, crime["OFFENSE_CODE_GROUP"], entry)
    else:
        entry = offentry
        al.add_last(entry["lstoffenses"], crime)
    return datentry


def new_data_entry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = lp.new_map(num_elements=30,
                                        load_factor=0.5)
    entry['lstcrimes'] = al.new_list()
    return entry


def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = al.new_list()
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimes_size(analyzer):
    """
    Número de crimenes
    """
    return al.size(analyzer['crimes'])


def index_height(analyzer):
    """
    Altura del arbol
    """
    return rbt.height(analyzer["dateIndex"])


def index_size(analyzer):
    """
    Numero de elementos en el indice
    """
    return rbt.size(analyzer["dateIndex"])


def min_key(analyzer):
    """
    Llave mas pequena
    """
    return rbt.get_min(analyzer["dateIndex"])


def max_key(analyzer):
    """
    Llave mas grande
    """
    return rbt.get_max(analyzer["dateIndex"])


def index_height_areas(analyzer):
    """
    Altura del arbol por areas
    """
    # DOne Retornar la altura del árbol por areas
    return rbt.height(analyzer["areaIndex"])


def index_size_areas(analyzer):
    """
    Numero de elementos en el indice por areas
    """
    # DONE Retornar el numero de elementos en el árbol por areas
    return rbt.size(analyzer["areaIndex"])


def min_key_areas(analyzer):
    """
    Llave mas pequena por areas
    """
    # DONE Retornar la llave más pequeña del árbol por áreas
    return rbt.get_min(analyzer["areaIndex"])


def max_key_areas(analyzer):
    """
    Llave mas grande por areas
    """
    # DONE Retornar la llave más grande del árbol por áreas
    return rbt.get_max(analyzer["areaIndex"])

def get_crimes_by_range_area(analyzer, initialArea, finalArea):
    """
    Retorna el numero de crimenes en un rango de areas
    """
    # DONE Completar la consulta de crimenes por rango de areas
    if initialArea == "":
        initialArea = 0
    else:
        initialArea = int(initialArea)

    if finalArea == "":
        finalArea = 9999
    else:
        finalArea = int(finalArea)
    lst = rbt.values(analyzer["areaIndex"], initialArea, finalArea)
    totalcrimes = 0
    current = lst["first"]
    while current is not None:
        lstarea = current["info"]
        totalcrimes += al.size(lstarea["lstcrimes"])
        current = current["next"]
    return totalcrimes

def get_crimes_by_range(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    lst = rbt.values(analyzer["dateIndex"], initialDate.date(), finalDate.date())
    totalcrimes = 0
    current = lst["first"]
    while current is not None:
        lstdate = current["info"]
        totalcrimes += al.size(lstdate["lstcrimes"])
        current = current["next"]
    return totalcrimes


def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    crimedate = rbt.get(analyzer["dateIndex"], initialDate.date())
    if crimedate is not None:
        offensemap = crimedate["offenseIndex"]
        numoffenses = lp.get(offensemap, offensecode)
        if numoffenses is not None:
            return lp.size(numoffenses["lstoffenses"])
    return 0
