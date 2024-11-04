from mp_api.client import MPRester
import math
import numpy as np
from decimal import Decimal

key = "H2RaVIDWeAR6N1y8E9lh9XYqB8mwVog7"


composto = input('digite seu material ')
s = input('Se quiser, digite a simetria ')

with MPRester(key) as mpr:
    
    def busca_material(composto,simetria = ''):
        sistemas = ['Triclinic', 'Monoclinic', 'Orthorhombic', 'Tetragonal', 'Trigonal', 'Hexagonal','Cubic']
        
        if simetria in sistemas:
            docs = mpr.materials.summary.search(formula=composto,crystal_system=simetria)
            mpids = [doc.material_id for doc in docs]
            mpids = mpids[0] 

        else:
            docs = mpr.materials.summary.search(formula=composto)
            mpids = [doc.material_id for doc in docs]
            mpids = mpids[0]
            print ('\n !!!  simetria não especificada  !!!  \n')   
        estrutura = mpr.get_structure_by_material_id(mpids)     
        dados = mpr.materials.get_data_by_id(mpids)
        estrut_nome = dados.symmetry.crystal_system      
        internacional = dados.symmetry.number

        return internacional, estrutura, estrut_nome

N_internacional,estrutura, estrut_nome = busca_material(composto,s)

def qe_input(estrutura):
    with open('data_MP.txt', 'w') as file:
        file.write(str(estrutura))
    a, b, c, alpha, beta, gamma, nat, tipos_atomicos, vetores, prefix = extrair_parametros_rede('data_MP.txt')
    ar,cgr,sgr,cb,sa,ca = calculo_parametros_lattice(a, b, c, alpha, beta, gamma)
    diag = np.identity(3)
    stdbase = np.array([[1.0 / ar, -cgr / sgr / ar, cb * a], [0.0, b * sa, b * ca], [0.0, 0.0, c]],dtype=float,)
    base = np.dot(stdbase, diag)

    with open(f'{composto}.in', 'w') as file: 
        file.write(f"&CONTROL\nprefix = '{prefix}'\n/\n&SYSTEM\nibrav = 0\nnat = {nat}\nntyp = {len(tipos_atomicos)}\n/\n&ELECTRONS\n/\n")
        file.write("CELL_PARAMETERS angstrom\n")
        for vetor in base:
            v_1 = Decimal(vetor[0]).quantize(Decimal('0.00000000'))
            v_2 = Decimal(vetor[1]).quantize(Decimal('0.00000000'))
            v_3 = Decimal(vetor[2]).quantize(Decimal('0.00000000'))
            file.write(f"   {v_1:>10.8f}  {v_2:>10.8f}  {v_3:>10.8f}\n")
        file.write(f'ATOMIC_SPECIES\n')
        for elemento in tipos_atomicos:
            file.write(f'     {elemento} {massa_atomica(elemento)} {elemento}_pseudo\n')
        file.write('ATOMIC_POSITIONS {crystal}\n')
        for vetor in vetores:
            v_1 = Decimal(vetor[1]).quantize(Decimal('0.00000000'))
            v_2 = Decimal(vetor[2]).quantize(Decimal('0.00000000'))
            v_3 = Decimal(vetor[3]).quantize(Decimal('0.00000000'))
            file.write(f' {vetor[0]} {v_1:>10.8f}  {v_2:>10.8f}  {v_3:>10.8f}\n')
        file.write('K_POINTS automatic')
        print(f'Seu input {composto}.in está pronto.')

def extrair_parametros_rede(filename):
    """
    Extrai parâmetros de rede e informações sobre o material desejado de um arquivo de texto
    obtido do Materials Project.

    Args:
        filename (str): Caminho para o arquivo de texto que contém os dados dos parâmetros de rede e posições atômicas.

    Returns:
        tuple: Uma tupla contendo:
            - a (float): Comprimento da aresta `a` da célula unitária.
            - b (float): Comprimento da aresta `b` da célula unitária.
            - c (float): Comprimento da aresta `c` da célula unitária.
            - alpha (float): Ângulo entre as arestas `b` e `c` (em graus).
            - beta (float): Ângulo entre as arestas `a` e `c` (em graus).
            - gamma (float): Ângulo entre as arestas `a` e `b` (em graus).
            - nat (int): Número total de átomos na célula unitária.
            - tipos_atomicos (set): Conjunto contendo os tipos de átomos únicos presentes no material.
            - vetores (list): Lista contendo as posições e tipos dos átomos, onde cada elemento é uma lista no formato 
              `[tipo_atomo, x, y, z]` com as coordenadas `x`, `y`, `z`.
            - prefix (str): Nome do composto.

    Raises:
        FileNotFoundError: Se o arquivo especificado não for encontrado.
    """
    try:
        with open(filename, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return None
    lines = text.split('\n')
    a, b, c = None, None, None
    alpha, beta, gamma = None, None, None
    
    parts = lines[2].split(':')
    a, b, c = map(float, parts[1].split())
    
    parts = lines[3].split(':')
    alpha, beta, gamma = map(float, parts[1].split())
    
    nat = int(lines[-1].split()[0])+1
    vetores = []

    prefix = lines[1].split()[-1]

    for line in lines[8:]:
        line = line.split()
        vetores.append([line[1],float(line[2]),float(line[3]),float(line[4])])
    tipos_atomicos = set()

    for vetor in vetores:
        tipos_atomicos.add(vetor[0])
    
    return a, b, c, alpha, beta, gamma,nat,tipos_atomicos,vetores, prefix 
def calculo_parametros_lattice(a, b, c, alpha, beta, gamma):
    """Cálcula parametros necessários para a criação do CELL_PARAMETERS.

    Args:
        a (float): Largura do paralelepípedo.
        b (float): Comprimento do paralelepípedo.
        c (float): Altura do paralelepípedo.
        alpha (float): Ângulo entre as arestas b e c do paralelepípedo.
        beta (float): Ângulo entre as arestas a e c do paralelepípedo.
        gamma (float): Ângulo entre as arestas a e b do paralelepípedo.

   
    Returns:
        tuple: Uma tupla contendo os seguintes valores calculados:
            - ar (float): Largura do paralelepípedo no espaço reciproco.
            - cgr (float): Cosseno do ângulo gamma no espaço reciproco.
            - sgr (float): Seno do ângulo gamma no espaço reciproco.
            - cb (float): Cosseno do ângulo beta.
            - sa (float): Seno do ângulo alpha.
            - ca (float): Cosseno do ângulo alpha.

    Raises:
        ValueError: Caso os valores dos ângulos fornecidos resultem em um valor de volume inválido (zero ou negativo).
    """
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)

    ca = math.cos(alpha)
    cb = math.cos(beta)
    cg = math.cos(gamma)
    sa = math.sin(alpha)
    sb = math.sin(beta)

    V = a * b * c * np.sqrt(1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg)
    if V <= 0:
        raise ValueError("Volume inválido.")

    ar = (b * c * sa) / V

    cgr = (ca * cb - cg) / (sa * sb)
    sgr = math.sqrt(1 - cgr**2)

    return ar,cgr,sgr,cb,sa,ca
def massa_atomica(elemento):
    """Encontra a massa atômica de um Elemento.

    Args:
        elemento (str): Nome do elemento.

    Returns:
        float: Massa atomica do elemento.

    Raises:
        ValueError: Caso o elemento não esteja no dicionário.
    """
    elemento_massa = {
        "H": 1.00784,
        "He": 4.002602,
        "Li": 6.938,
        "Be": 9.0121831,
        "B": 10.806,
        "C": 12.011,
        "N": 14.0067,
        "O": 15.999,
        "F": 18.998403163,
        "Ne": 20.1797,
        "Na": 22.98976928,
        "Mg": 24.305,
        "Al": 26.9815385,
        "Si": 28.085,
        "P": 30.973761998,
        "S": 32.06,
        "Cl": 35.45,
        "Ar": 39.948,
        "K": 39.0983,
        "Ca": 40.078,
        "Sc": 44.955908,
        "Ti": 47.867,
        "V": 50.9415,
        "Cr": 51.9961,
        "Mn": 54.938044,
        "Fe": 55.845,
        "Co": 58.933194,
        "Ni": 58.6934,
        "Cu": 63.546,
        "Zn": 65.38,
        "Ga": 69.723,
        "Ge": 72.63,
        "As": 74.921595,
        "Se": 78.971,
        "Br": 79.904,
        "Kr": 83.798,
        "Rb": 85.4678,
        "Sr": 87.62,
        "Y": 88.90584,
        "Zr": 91.224,
        "Nb": 92.90637,
        "Mo": 95.95,
        "Tc": 98.0,
        "Ru": 101.07,
        "Rh": 102.90550,
        "Pd": 106.42,
        "Ag": 107.8682,
        "Cd": 112.414,
        "In": 114.818,
        "Sn": 118.710,
        "Sb": 121.760,
        "Te": 127.60,
        "I": 126.90447,
        "Xe": 131.293,
        "Cs": 132.90545196,
        "Ba": 137.327,
        "La": 138.90547,
        "Ce": 140.116,
        "Pr": 140.90766,
        "Nd": 144.242,
        "Pm": 145.0,
        "Sm": 150.36,
        "Eu": 151.964,
        "Gd": 157.25,
        "Tb": 158.92535,
        "Dy": 162.500,
        "Ho": 164.93033,
        "Er": 167.259,
        "Tm": 168.93422,
        "Yb": 173.045,
        "Lu": 174.9668,
        "Hf": 178.49,
        "Ta": 180.94788,
        "W": 183.84,
        "Re": 186.207,
        "Os": 190.23,
        "Ir": 192.217,
        "Pt": 195.084,
        "Au": 196.966569,
        "Hg": 200.592,
        "Tl": 204.38,
        "Pb": 207.2,
        "Bi": 208.98040,
        "Th": 232.0377,
        "Pa": 231.03588,
        "U": 238.02891
    }
    if elemento not in elemento_massa:
        raise ValueError("Não há esse elemento no nosso banco de dados.")
    return elemento_massa[elemento]

qe_input(estrutura)