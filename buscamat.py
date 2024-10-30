from mp_api.client import MPRester
import numpy as np
key = "H2RaVIDWeAR6N1y8E9lh9XYqB8mwVog7"


#composto = input('digite seu material ')
#simetria = input('Se quiser, digite a simetria ')


with MPRester(key) as mpr:
    
    def busca_material(composto,simetria):
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

    def busca_chem(chem):
        docs =  mpr.materials.summary.search(chemsys=chem)
        mpids = [doc.material_id for doc in docs]
        compostos = []
        for mpid in mpids:
           # estrutura += f'\n\n{mpr.get_structure_by_material_id(mpid)}'
            dados = mpr.materials.get_data_by_id(mpid)
            compostos += [dados.formula_pretty]
            estrut_nome = dados.symmetry.crystal_system      
            internacional = dados.symmetry.number
        return compostos, mpids, estrut_nome, internacional

chem = input('A-B-C ')   
c,m,nome,i = busca_chem(chem)
print(c)
'''
n,e,nome = busca_material(composto,simetria)
chem = input('A-B-C ')'''