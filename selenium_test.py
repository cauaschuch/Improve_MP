from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
texto= input('número ')
driver = webdriver.Chrome()   #usa o driver que conversa com determinado navegador (chrome ou firefox)

driver.get('https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list')  #navegar até a página desejada através do url
#assert 'Wycoff Positions' in driver.title  #afirma o título da página

elemento = driver.find_element(By.NAME,'gnum') #nome do elemento, no caso a caixa de texto, no código fonte da página
elemento.clear() #limpa o que estiver escrito previamente, se houver algo
elemento.send_keys(texto) #.send_keys reconhece strings e teclas
elemento.send_keys(Keys.ENTER) #Keys. NOME DA TECLA
input('pressione enter para fechar') #deixei este input para o código não finalizar. Sem isso, a aba do chrome fecha
