from mp_api.client import MPRester
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait


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
texto= n
driver = webdriver.Chrome()   #usa o driver que conversa com determinado navegador (chrome ou firefox)

driver.get('https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list')  #navegar até a página desejada através do url
#assert 'Wycoff Positions' in driver.title  #afirma o título da página

elemento = driver.find_element(By.NAME,'gnum') #nome do elemento, no caso a caixa de texto, no código fonte da página
elemento.clear() #limpa o que estiver escrito previamente, se houver algo
elemento.send_keys(texto) #.send_keys reconhece strings e teclas
elemento.send_keys(Keys.ENTER) #Keys. NOME DA TECLA
input('pressione enter para fechar')
