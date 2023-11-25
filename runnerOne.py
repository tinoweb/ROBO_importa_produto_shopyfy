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

# URL da página de categoria
url = 'https://www.leveshoes.com.br/categoria-produto/tenis/'

print("Iniciando a solicitação à página de categoria...")
response = requests.get(url, headers={'User-Agent': 'Custom User Agent'})

lista_de_produtos = []

if response.status_code == 200:
    print("Página de categoria carregada com sucesso.")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar a lista de produtos
    produtos = soup.find_all('li', class_='product')
    print(f"Encontrados {len(produtos)} produtos na página.")
    
    for indice, produto in enumerate(produtos, start=1):
        print(f"Processando produto {indice}/{len(produtos)}...")
        print(f"...||...")
        produto_info = {}
        
        # Extrair o link, título e preço do produto
        link_produto = produto.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
        titulo_produto = produto.find('h2', class_='woocommerce-loop-product__title').text.strip()
        preco_produto = produto.find('span', class_='price').text.strip()
        
        produto_info['link'] = link_produto
        produto_info['titulo'] = titulo_produto
        produto_info['preco'] = preco_produto

        # Obter detalhes do produto
        print(f"Obtendo detalhes para: {titulo_produto}")
        detalhes = get_product_details(link_produto)
        if detalhes:
            produto_info.update(detalhes)
            print(f"Detalhes obtidos para {titulo_produto}.")

        lista_de_produtos.append(produto_info)
    
    print("Todos os produtos foram processados. Salvando em arquivo JSON...")
    # Salvar os dados em um arquivo JSON
    with open('produtos.json', 'w', encoding='utf-8') as f:
        json.dump(lista_de_produtos, f, ensure_ascii=False, indent=4)

    print('Dados salvos em produtos.json')

else:
    print(f'Falha ao acessar a página. Código de status: {response.status_code}')