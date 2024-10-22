from mp_api.client import MPRester
import numpy as np
key = "H2RaVIDWeAR6N1y8E9lh9XYqB8mwVog7"


c = input('digite seu material ')
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

n,e = busca_material(c,s)
print (n)