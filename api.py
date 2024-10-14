from mp_api.client import MPRester
import math
import numpy as np

key = "H2RaVIDWeAR6N1y8E9lh9XYqB8mwVog7"
with MPRester(key) as mpr:
    docs = mpr.materials.summary.search(formula="Nb6Si7Ni16",crystal_system='Cubic')
    mpids = [doc.material_id for doc in docs]
    structure = mpr.get_structure_by_material_id(mpids[0])

with open('data_MP.txt', 'w') as file:
    file.write(str(structure))

def extrair_parametros_rede(filename):
    with open(filename, 'r') as file:
        text = file.read()

    lines = text.split('\n')

    a, b, c = None, None, None
    alpha, beta, gamma = None, None, None

    for line in lines:
        if 'abc' in line:
            parts = line.split(':')
            a, b, c = map(float, parts[1].split())
        elif 'angles' in line:
            parts = line.split(':')
            alpha, beta, gamma = map(float, parts[1].split())

    return a, b, c, alpha, beta, gamma

a, b, c, alpha, beta, gamma = extrair_parametros_rede('data_MP.txt')
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

ar,cgr,sgr,cb,sa,ca = calculo_parametros_lattice(a, b, c, alpha, beta, gamma)
baserot = np.identity(3)
stdbase = np.array([[1.0 / ar, -cgr / sgr / ar, cb * a], [0.0, b * sa, b * ca], [0.0, 0.0, c]],dtype=float,)
base = np.dot(stdbase, baserot)
print(base)