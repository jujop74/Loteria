# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
from itertools import combinations
import pandas as pd

NUM_COMB_SIM = 5000

# NUM_MAX = 49
# NUM_BOLAS = 6
# glb_bloque = (
#     (3, 8),
#     (13, 16),
#     (21, 22),
#     (35, 39),
#     (40, 46))

NUM_MAX = 49
NUM_BOLAS = 6
glb_bloque = (
    (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25),
    (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24),
    (27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49),
    (26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48))

# NUM_MAX = 30
# NUM_BOLAS = 4
# glb_bloque = (
#     (1, 3, 5, 7, 9, 11, 13, 15),
#     (2, 4, 6, 8, 10, 12, 14),
#     (17, 19, 21, 23, 25, 27, 29),
#     (16, 18, 20, 22, 24, 26, 28, 30))


def get_patron_de_comb(comb):
    """Comprueba a que bloque "glb_bloque" pertenece cada uno de los elementos del parámetro "comb" y genera como
    resultado una lista con la definición del patrón.

    :param comb: Lista - Lista de números que representa la combinación.
    :return: Tupla - Patrón correspondiente a la combinación.
    """
    num_blq = len(glb_bloque)
    patron = [0] * num_blq

    for n in comb:
        for i in range(num_blq):
            if n in glb_bloque[i]:
                patron[i] += 1
                break

    return tuple(patron)


def es_patron_valido(patron):
    return sum(patron) == NUM_BOLAS


def imprime_lista_patrones(dict_patrones, titulo):
    """Escribe por la consola el censo de patron/valor del diccionario "dict_patrones".

    :param dict_patrones: Diccionario - Censo de patron/valor.
    :param titulo: String - Mensaje de cabecera.
    :return:
    """
    print(f"\n{titulo}\n")

    s_total = sum(dict_patrones.values())
    p_total = 0

    for indice, item in enumerate(dict_patrones.items()):
        prob = item[1] / s_total * 100
        p_total += prob

        print(f"{indice + 1:02d} - {item[0]} - {item[1]:8,d} - {prob:8.4f} %")

    print(f"\nProbabilidad total: {p_total:8.4f} %")
    print(f"Total de combinaciones: {s_total:8,d}\n")


def append_patron_a_lista(dict_patrones, patron):
    """Añade la lista "patron" si no existe en el diccionario "dict_patrones"; si existe, se suma 1 al valor asociado.

    :param dict_patrones: Diccionario - Censo de patron/valor.
    :param patron: Lista - Dato a validar si existe en el diccionario "dict_patrones".
    :return:
    """
    if patron in dict_patrones:
        dict_patrones[patron] += 1
    else:
        dict_patrones[patron] = 1


def genera_patrones_combinatorios():
    """ Genera todas las combinaciones posibles de "NUM_MAX" elementos posibles repetidos en grupos
de "NUM_BOLAS" elementos.

    :return: Diccionario - Censo de patrones de todas las combinaciones posibles.
    """
    dict_patrones = {}

    # Devuelve el número de elementos sin crear realmente la lista de combinaciones
    num_comb = sum(1 for _ in combinations(range(1, NUM_MAX + 1), r=NUM_BOLAS))

    cont_limit, cont_porc = [int(num_comb / 10), 0]
    i = 0

    # Generación de "NUM_BOLAS" bucles para los valores de 1 a NUM_MAX
    # (el valor final en "range" está excluido -> se debe sumar 1)
    for comb in combinations(range(1, NUM_MAX + 1), r=NUM_BOLAS):
        patron = get_patron_de_comb(comb)

        if es_patron_valido(patron):
            append_patron_a_lista(dict_patrones, patron)

        if i >= cont_limit:
            cont_porc += 10
            i = 0
            print(f"Porcentaje: {cont_porc}")
        else:
            i += 1

    # Ordenamos la lista de patrones usando como criterio de ordenación una función de tipo lambda para
    # ordenar por value (item[1])
    dict_patrones_ord = dict(sorted(dict_patrones.items(), key=lambda x: x[1], reverse=True))

    suma_total = sum(dict_patrones_ord.values())
    print(f"Suma total: {suma_total:8,d}")

    # Resumen final
    imprime_lista_patrones(dict_patrones_ord, "Censo total de patrones")

    return dict_patrones_ord


def hay_repetidos(lista):
    if len(lista) == len(set(lista)):
        return False
    else:
        return True


def simula_combinaciones(dict_patrones):
    """ Simulación de combinaciones de números a partir de la librería random.randint.

    :param dict_patrones: Diccionario - Censo de patron/valor.
    :return:
    """
    # Copia de diccionario inicializado a 0
    dict_combinaciones = {clave: 0 for clave in dict_patrones.keys()}

    for i in range(NUM_COMB_SIM):
        while True:
            comb = [randint(1, NUM_MAX) for _ in range(NUM_BOLAS)]

            # Las combinaciones con números repetidos no se tienen en cuenta
            if not hay_repetidos(comb):
                break

        patron = get_patron_de_comb(comb)

        if es_patron_valido(patron):
            dict_combinaciones[patron] += 1

    imprime_lista_patrones(dict_combinaciones, "Combinaciones simuladas")


def pd_excel_existe_combinacion(df, comb):
    """ Función que devuelve "True" si el parámetro "comb" existe en alguna fila del objeto "df".
    "False" en caso contrario.

    :param df: DataFrame - Datos leídos de la Excel de resultados.
    :param comb: Lista - Combinación a validar si existe en el DataFrame.
    :return: Devuelve "True" si el parámetro "comb" existe en alguna fila del objeto "df". "False" en caso contrario.
    """
    # Se asigna una nueva columna que contiene un objeto de tipo "List" formado por los 6 valores Nx.
    df_aux = pd.DataFrame()
    df_aux["C_Nx"] = df[["N1", "N2", "N3", "N4", "N5", "N6"]].values.tolist()

    # Se ordena los números para cada fila.
    df_aux["C_Nx"].apply(lambda x: x.sort())

    # Se ordena la lista de entrada ("sort" ordena sobre la propia lista, no devuelve ninguna lista nueva).
    comb.sort()

    # Se compara el campo "C_Nx" con el parámetro "comb" ordenado usando la función "pandas.apply" y una
    # función "lambda".
    # Los valores obtenidos al comparar se pasan a la función "pandas.loc" para seleccionar únicamente las filas con
    # valor cierto ("True").
    df_res = df_aux.loc[df_aux.apply(lambda x: True if x["C_Nx"] == comb else False, axis=1)]

    # Se devuelve "True" si el número de filas obtenidas es mayor o igual que 1. "False" en caso contrario.
    if df_res.shape[0] >= 1:
        return True
    else:
        return False


def pd_excel_lee_resultados():
    df = pd.read_excel("Resultados_Primitiva.xlsx", sheet_name=0)

    df_aux = pd.DataFrame()
    df_aux["C_Nx"] = df[["N1", "N2", "N3", "N4", "N5", "N6"]].values.tolist()
    df_aux["C_Nx"].apply(lambda x: x.sort())

    buscar = [1, 13, 25, 34, 48, 44]
    existe = pd_excel_existe_combinacion(df, buscar)

    print(existe)


def pd_excel_combinaciones(dict_patrones):
    df = pd.read_excel("Resultados_Primitiva.xlsx", sheet_name=0)

    # Copia de diccionario inicializado a 0
    dict_combinaciones = {clave: 0 for clave in dict_patrones.keys()}

    for f_comb in df[["N1", "N2", "N3", "N4", "N5", "N6"]].values.tolist():
        patron = get_patron_de_comb(f_comb)

        if es_patron_valido(patron):
            dict_combinaciones[patron] += 1

    imprime_lista_patrones(dict_combinaciones, "Combinaciones reales")


def main():
    dict_patrones = genera_patrones_combinatorios()

    # pd_excel_lee_resultados()

    simula_combinaciones(dict_patrones)
    pd_excel_combinaciones(dict_patrones)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
