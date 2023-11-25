import csv
import json
import re  # Importando o módulo de expressões regulares

# Carregar os dados dos produtos a partir do arquivo produtos.json
with open('produtos.json', 'r', encoding='utf-8') as file:
    produtos = json.load(file)
    print("Inicio da Conversao ...")

with open('ConvertidosVariacao.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # Cabeçalhos do arquivo CSV
    writer.writerow(["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Product Type", "Tags", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Variant SKU", "Variant Price", "Compare At Price", "Image Src", "Published", "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Requires Shipping", "Variant Taxable", "Gift Card", "SEO Title", "SEO Description", "Status"])
    
    for produto in produtos:
        # ... [restante da configuração dos campos do produto]
        if "cores" not in produto or not produto["cores"]:
            print(f"Produto {produto.get('nome', 'Desconhecido')} ignorado: sem cores")
            continue  # Pular produtos sem cores
        if "tamanhos" not in produto or not produto["tamanhos"]:
            print(f"Produto {produto.get('nome', 'Desconhecido')} ignorado: sem tamanhos")
            continue  # Pular produtos sem tamanhos
        if "imagens" not in produto or not produto["imagens"]:
            print(f"Produto {produto.get('nome', 'Desconhecido')} ignorado: sem imagens")
            continue  # Pular produtos sem imagens

        handle = produto["nome"]
        title = produto["titulo"]
        body_html = re.sub(r'(<br>[\s\r\n]+)+', '<br><br>', produto["descricao"].replace("\n", "<br>"))
        vendor = "Vendor Padrão"
        product_category = "Vestuário e acessórios > Sapatos"
        product_type = "tenis"
        tags = "Tênis Puma"
        price = produto["valor"].replace("R$", "").replace(",", ".").strip()
        compare_at_price = ""  # Se disponível
        published = "TRUE"
        inventory_tracker = "shopify"
        inventory_qty = "100"
        inventory_policy = "continue"
        fulfillment_service = "manual"
        requires_shipping = "TRUE"
        taxable = "TRUE"
        gift_card = "FALSE"
        seo_title = title
        seo_description = body_html[:320]  # Limitar a 320 caracteres
        status = "active"

       # Primeiro, escreva as informações principais do produto e a primeira variação
        writer.writerow([handle, title, body_html, vendor, product_category, product_type, tags, "Color", produto["cores"][0], "Size", produto["tamanhos"][0], "", price, compare_at_price, produto["imagens"][0] if produto["imagens"] else "", published, inventory_tracker, inventory_qty, inventory_policy, fulfillment_service, requires_shipping, taxable, gift_card, seo_title, seo_description, status])
        
        # Adicione as demais variações do produto
        for cor in produto["cores"]:
            for tamanho in produto["tamanhos"]:
                if cor != produto["cores"][0] or tamanho != produto["tamanhos"][0]:  # Evitar duplicar a primeira variação
                    writer.writerow([handle, "", "", "", "", "", "", "Color", cor, "Size", tamanho, "", price, compare_at_price, "", published, inventory_tracker, inventory_qty, inventory_policy, fulfillment_service, requires_shipping, taxable, "", "", "", status])
        
        # Adicione as demais imagens do produto
        for i, image_src in enumerate(produto["imagens"], start=1):
            if i > 1:  # Pular a primeira imagem, já que foi adicionada com a primeira variação
                writer.writerow([handle, "", "", "", "", "", "", "", "", "", "", "", "", "", image_src, "", "", "", "", "", "", "", "", "", "", ""])

    print("Finalizado com sucesso ...")