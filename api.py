from mp_api.client import MPRester
import math
import numpy as np


key = "H2RaVIDWeAR6N1y8E9lh9XYqB8mwVog7"


composto = input('digite seu material ')
s = input('Se quiser, digite a simetria ')

with MPRester(key) as mpr:
    
    def busca_material(composto,simetria):
        sistemas = ['Triclinic', 'Monoclinic', 'Orthorhombic', 'Tetragonal', 'Trigonal', 'Hexagonal','Cubic']

        if simetria in sistemas:
            docs = mpr.materials.summary.search(formula=composto,crystal_system=simetria)
            mpids = [doc.material_id for doc in docs]
            mpids = mpids[0]
            estrutura = mpr.get_structure_by_material_id(mpids)     
            dados = mpr.materials.get_data_by_id(mpids)
            internacional = dados.symmetry.number
            
        else:
            docs = mpr.materials.summary.search(formula=composto)
            mpids = [doc.material_id for doc in docs]
            mpids = mpids[0]
            print ('\n !!!  simetria não especificada  !!!  \n')   
            estrutura = mpr.get_structure_by_material_id(mpids)     
            dados = mpr.materials.get_data_by_id(mpids)
            internacional = dados.symmetry.number
        
        return internacional, estrutura

n,structure = busca_material(composto,s)

#INICIO PARTE 2 DO TRABALHO (XU E GADELHA)
with open('data_MP.txt', 'w') as file:
    file.write(str(structure))

def extrair_parametros_rede(filename):
    with open(filename, 'r') as file:
        text = file.read()

    lines = text.split('\n')

    a, b, c = None, None, None
    alpha, beta, gamma = None, None, None
    #pegar abc
    parts = lines[2].split(':')
    a, b, c = map(float, parts[1].split())
    #pegar angulos
    parts = lines[3].split(':')
    alpha, beta, gamma = map(float, parts[1].split())
    #pegar numero de atomos
    nat = int(lines[-1].split()[0])+1
    vetores = []
    for line in lines[8:]:
        line = line.split()
        vetores.append([line[1],float(line[2]),float(line[3]),float(line[4])])
    tipos_atomicos = set()
    for vetor in vetores:
        tipos_atomicos.add(vetor[0])
    
    return a, b, c, alpha, beta, gamma,nat,tipos_atomicos,vetores
def calculo_parametros_lattice(a, b, c, alpha, beta, gamma):
    # converter deg pra rad
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)

    # c = cosseno, s = seno
    ca = math.cos(alpha)
    cb = math.cos(beta)
    cg = math.cos(gamma)
    sa = math.sin(alpha)
    sb = math.sin(beta)
    sg = math.sin(gamma)

    # Volume da célula real
    V = a * b * c * np.sqrt(1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg)

    #valor de a no espaco reciproco
    ar = (b * c * sa) / V

    #seno e cosseno de gamma reciproco
    cgr = (ca * cb - cg) / (sa * sb)
    sgr = math.sqrt(1 - cgr**2)

    return ar,cgr,sgr,cb,sa,ca
def massa_atomica(elemento):
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
    return elemento_massa[elemento]

a, b, c, alpha, beta, gamma, nat, tipos_atomicos, vetores = extrair_parametros_rede('data_MP.txt')
ar,cgr,sgr,cb,sa,ca = calculo_parametros_lattice(a, b, c, alpha, beta, gamma)
diag = np.identity(3)
stdbase = np.array([[1.0 / ar, -cgr / sgr / ar, cb * a], [0.0, b * sa, b * ca], [0.0, 0.0, c]],dtype=float,)
base = np.dot(stdbase, diag)

with open(f'{composto}.in', 'w') as file: #montar o .in do composto
    file.write(f'&CONTROL\n/\n&SYSTEM\nibrav = 0\nnat = {nat}\nntyp ={len(tipos_atomicos)}\n/\n&ELECTRONS\n/\n')
    file.write("CELL_PARAMETERS angstrom\n")
    for vetor in base:
        file.write(f"   {vetor[0]:>10.8f}  {vetor[1]:>10.8f}  {vetor[2]:>10.8f}\n")
    file.write(f'ATOMIC_SPECIES\n')
    for elemento in tipos_atomicos:
        file.write(f'     {elemento} {massa_atomica(elemento)} {elemento}_pseudo\n')
    file.write('ATOMIC_POSITIONS {crystal}\n')
    for vetor in vetores:
        file.write(f' {vetor[0]} {vetor[1]:>10.8f}  {vetor[2]:>10.8}  {vetor[3]:>10.8f}\n')
    file.write('K_POINTS automatic')
