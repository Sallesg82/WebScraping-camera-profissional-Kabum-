from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

chrome_driver_path = r'C:\Program Files\chromedriver-win64\chromedriver.exe'

servicos = Service(chrome_driver_path)
controle = webdriver.ChromeOptions()
controle.add_argument('--disable-gpu')
controle.add_argument('--window-size=1080,720')
# controle.add_argument('--headless')

executador = webdriver.Chrome(service=servicos, options=controle)
time.sleep(5)

url = 'https://www.kabum.com.br/cameras-e-drones/camera-digital/camera-profissional'
executador.get(url)
time.sleep(5)

dic_produtos = {'nome': [], 'preco': []}
pagina = 1

while True:
    print(f'Coletando dados da página {pagina}...')
    
    try:
        WebDriverWait(executador, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'productCard'))
        )
        print('Elementos encontrados com sucesso!')
        
    except TimeoutException:
        print('Tempo de espera excedido')
        break
        
    produtos = executador.find_elements(By.CLASS_NAME, 'productCard')
    
    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            
            print(f'{nome} - {preco}')
            
            dic_produtos['nome'].append(nome)
            dic_produtos['preco'].append(preco)
            
        except Exception as e:
            print('Erro ao coletar dados!', e)
            
    try:
        mudar_pag = WebDriverWait(executador, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'nextLink'))
        )
        
        if mudar_pag:
            executador.execute_script('arguments[0].scrollIntoView();', mudar_pag)
            time.sleep(1)
        
            executador.execute_script('arguments[0].click();', mudar_pag)
            pagina += 1
            print(f'Indo para a página {pagina}...')
        
            time.sleep(4)
        else:
            print('Você chegou no final.')
            break
            
    except Exception as e:
        print('Erro ao avançar de página!', e)
        break

executador.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel('camera.xlsx', index=False)

print(f'Tudo certo, {len(df)} produtos foram adicionados no Excel!')