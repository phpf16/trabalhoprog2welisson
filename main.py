# main.py
from padaria import Padaria


def menu():
    while True:
        print("""
#========== 🥐 MENU - Padaria Criativa 🥐 ==========# 
1 - Cadastrar produto
2 - Listar produtos
3 - Oferta do dia (escolha manual)
4 - Relatório: itens com estoque abaixo de X
5 - Sair
#===================================================#
""")
        op = input("Opção (digite o número correspondente, ex: 1): ").strip()
        print(""" """)
        
        
        

        if op == "1":
            Padaria.cadastrar()
        elif op == "2":
            Padaria.listar()
        elif op == "3":
            # nova interação para escolher oferta
            oferta = Padaria.escolher_oferta_interativa()
            if oferta:
                print("""======= OFERTA DO DIA =======""")
                print(f"Produto: {oferta['Nome']}")
                print(f"Preço original: R$ {oferta['Preco_original']:.2f}")
                print(f"Desconto aplicado: {oferta['Desconto_percentual']}%")
                print(f"Preço com desconto: R$ {oferta['Preco_com_desconto']:.2f}")
                print(f"Estoque disponível: {oferta['Estoque']}")
                print("=============================")
        elif op == "4":
            limite = input("Mostrar itens com estoque abaixo de (digite um número inteiro; pressione Enter para usar 5): ").strip()
            try:
                lim = int(limite) if limite else 5
            except:
                print("Entrada inválida. Será usado o valor padrão 5.")
                lim = 5
            baixos = Padaria.estoque_baixo(lim)
            if not baixos:
                print("Nenhum produto com estoque abaixo do limite informado.")
            else:
                print(""" """)
                print("====== ITENS COM ESTOQUE BAIXO ======")
                for p in baixos:
                    print(f"- {p.get('Nome')} (estoque: {p.get('Estoque')})")
                print("=====================================")
        elif op.lower() == ".json":
            # mostra o conteúdo do JSON e pergunta se deseja exportar também
            Padaria.mostrar_arquivo_json()
        elif op == "5":
            print("Saindo. Volte sempre à padaria :)")
            break
        else:
            print("Opção inválida. Digite o número correspondente às opções do menu (ex: 2).")


if __name__ == "__main__":
    menu()