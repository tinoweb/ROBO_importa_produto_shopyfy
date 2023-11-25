import requests
from bs4 import BeautifulSoup
import json

# Função para obter detalhes do produto
def get_product_details(url):
    response = requests.get(url, headers={'User-Agent': 'Custom User Agent'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Nome do produto
        nome = soup.find('h1', class_='product_title').text.strip()

        # Valor do produto (considerando a tag <ins>)
        price_tag = soup.find('p', class_='price').find('ins')
        if price_tag:
            valor = price_tag.get_text().strip()
        else:
            # Se a tag <ins> não estiver presente, pegar o valor normal
            valor = soup.find('p', class_='price').get_text().strip()

        # Variações de cores e tamanhos
        cores = [option.text.strip() for option in soup.find_all('select', {'name': 'attribute_pa_cor'})[0].find_all('option')[1:]] if soup.find('select', {'name': 'attribute_pa_cor'}) else []
        tamanhos = [option.text.strip() for option in soup.find_all('select', {'name': 'attribute_pa_tamanho'})[0].find_all('option')[1:]] if soup.find('select', {'name': 'attribute_pa_tamanho'}) else []

        # Descrição do produto
        descricao = soup.find('div', {'id': 'tab-description'}).get_text(separator='\n').strip()

        # Link do vídeo (se existir)
        iframe = soup.find('iframe')
        link_video = iframe['src'] if iframe else ''

        # Extrair links das imagens do produto
        imagens = []
        container_imagens = soup.find_all('div', class_='woocommerce-product-gallery__image')
        for div in container_imagens:
            img = div.find('img')
            if img and img.has_attr('src'):
                imagens.append(img['src'])

        return {
            "nome": nome,
            "valor": valor,
            "cores": cores,
            "tamanhos": tamanhos,
            "descricao": descricao,
            "link_video": link_video,
            "imagens": imagens 
        }
    else:
        return None

# URL inicial da categoria
url_categoria = 'https://www.leveshoes.com.br/categoria-produto/tenis-vans/'

lista_de_produtos = []

def processar_pagina(url):
    print(f"Iniciando a solicitação à página: {url}")
    response = requests.get(url, headers={'User-Agent': 'Custom User Agent'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        produtos = soup.find_all('li', class_='product')
        print(f"Encontrados {len(produtos)} produtos.")

        for produto in produtos:
            link_produto = produto.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
            titulo_produto = produto.find('h2', class_='woocommerce-loop-product__title').text.strip()
            
            detalhes = get_product_details(link_produto)
            if detalhes:
                detalhes['titulo'] = titulo_produto  # Adicionando o título ao dicionário
                lista_de_produtos.append(detalhes)

        # Encontrar link da próxima página
        next_page_link = soup.find('a', class_='next')
        return next_page_link['href'] if next_page_link else None

    else:
        print(f'Falha ao carregar a página. Código de status: {response.status_code}')
        return None

url_atual = url_categoria

while url_atual:
    proxima_url = processar_pagina(url_atual)
    if proxima_url:
        url_atual = proxima_url
    else:
        break

# Salvar os dados em um arquivo JSON
with open('produtos.json', 'w', encoding='utf-8') as f:
    json.dump(lista_de_produtos, f, ensure_ascii=False, indent=4)

print('Dados salvos em produtos.json')