# padaria.py (atualizado)

import json


class Padaria:
    """Classe que gerencia os produtos da padaria com persistência em JSON.

    Arquivo padrão: padaria.json
    """

    __arquivo = "padaria.json"

    @classmethod
    def carregar(cls):
        """Carrega a lista de produtos do arquivo JSON.

        Retorna lista vazia se o arquivo não existir ou em caso de erro.
        """
        try:
            with open(cls.__arquivo, "r", encoding="utf-8") as f:
                dado = json.load(f)
                return dado
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Erro ao carregar {cls.__arquivo}: {e}")
            return []

    @classmethod
    def salvar(cls, dado):
        """Salva a lista (dado) no arquivo JSON.

        Retorna True se sucesso, False em caso de erro.
        """
        try:
            with open(cls.__arquivo, "w", encoding="utf-8") as f:
                json.dump(dado, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar {cls.__arquivo}: {e}")
            return False

    @classmethod
    def cadastrar(cls):
        """Cadastra um produto pedindo nome, preço e estoque com validações claras.

        As perguntas mostram exemplos e o que exatamente digitar.
        """
        print("#=============== Cadastro de Produto ===============#")
        nome = input("Digite o NOME do produto (ex: Pao frances, Bolo fatiado): ").strip()
        if not nome:
            print("Nome vazio. Cadastro cancelado. Por favor, informe um nome válido.")
            return

        preco = input("Digite o PREÇO do produto usando ponto como separador decimal (ex: 2.50): ").strip()
        estoque = input("Digite a QUANTIDADE em estoque (somente número inteiro, ex: 10): ").strip()

        try:
            preco_f = float(preco)
            if preco_f < 0:
                raise ValueError
        except:
            print("Preço inválido. Use um número como 2.50. Cadastro cancelado.")
            return

        try:
            estoque_i = int(estoque)
            if estoque_i < 0:
                raise ValueError
        except:
            print("Estoque inválido. Use um número inteiro não-negativo. Cadastro cancelado.")
            return

        produto = {
            "Nome": nome,
            "Preco": preco_f,
            "Estoque": estoque_i,
        }

        lista = cls.carregar()
        lista.append(produto)
        if cls.salvar(lista):
            print("Produto cadastrado com sucesso.")
        else:
            print("Falha ao salvar produto.")

    @classmethod
    def listar(cls):
        """Lista os produtos cadastrados no arquivo com instruções claras para o usuário."""
        lista = cls.carregar()
        if not lista:
            print("Nenhum produto cadastrado. Use a opção 1 para adicionar produtos.")
            return
        print("#========== Lista de produtos cadastrados ===========#\n")
        for index, p in enumerate(lista, start=1):
            nome = p.get('Nome', '---')
            preco = float(p.get('Preco', 0.0))
            estoque = p.get('Estoque', 0)
            print(f"{index}) Nome: {nome} — Preço: R$ {preco:.2f} — Estoque: {estoque}")
        print("Fim da listagem.")

    @classmethod
    def escolher_oferta_interativa(cls):
        """Interação para escolher qual produto será a promoção do dia.

        Mostra apenas produtos com estoque disponível (Estoque > 0) em um formato limpo
        e numerado. Depois pede ao usuário para escolher o número do produto e o
        percentual de desconto. Retorna o dicionário de oferta ou None se o usuário cancelar.
        """
        lista = cls.carregar()
        if not lista:
            print("Nenhum produto cadastrado para definir promoção.")
            return None

        disponiveis = [p for p in lista if int(p.get('Estoque', 0)) > 0]
        if not disponiveis:
            print("Nenhum produto com estoque disponível para promoção.")
            return None

        # Cabeçalho limpo para melhor visualização
        print("Produtos disponíveis para promoção:")
        header = f"{'Nº':<3} {'Produto':<30} {'Preço':>10} {'Estoque':>8}"
        print(header)
        print('-' * len(header))
        for idx, p in enumerate(disponiveis, start=1):
            nome = str(p.get('Nome', ''))
            preco = float(p.get('Preco', 0.0))
            estoque = int(p.get('Estoque', 0))
            # truncar nome para evitar poluição visual
            nome_vis = (nome[:27] + '...') if len(nome) > 30 else nome
            print(f"{idx:<3} {nome_vis:<30} R$ {preco:>7.2f} {estoque:>8}")
        print('-' * len(header))
       
        print(""" """)
        escolha = input("Digite o NÚMERO do produto que será a promoção (ou 'c' para cancelar): ").strip()
        print(""" """)

        if escolha.lower() == 'c':
            print("Promoção cancelada pelo usuário.")
            return None
        try:
            i = int(escolha)
            if i < 1 or i > len(disponiveis):
                raise ValueError
        except:
            print("Entrada inválida. A promoção foi cancelada. Digite um número válido na próxima vez.")
            return None

        produto = disponiveis[i-1]
        desconto_input = input("Digite o percentual de desconto a aplicar (ex: 20 para 20% — pressione Enter para usar 20%): ").strip()
        print(""" """)
        try:
            desconto = float(desconto_input) if desconto_input else 20.0
            if desconto < 0 or desconto > 100:
                raise ValueError
        except:
            print("Percentual inválido. Será usado 20% por padrão.")
            desconto = 20.0

        preco_original = float(produto.get("Preco", 0.0))
        desconto_valor = (desconto / 100.0) * preco_original
        preco_desconto = round(preco_original - desconto_valor, 2)

        oferta = {
            "Nome": produto.get("Nome"),
            "Preco_original": preco_original,
            "Preco_com_desconto": preco_desconto,
            "Estoque": produto.get("Estoque"),
            "Desconto_percentual": desconto,
        }
        return oferta

    @classmethod
    def estoque_baixo(cls, limite=5):
        """Retorna lista de produtos com estoque abaixo do 'limite'."""
        lista = cls.carregar()
        baixos = [p for p in lista if int(p.get("Estoque", 0)) < limite]
        return baixos

    @classmethod
    def exportar_json(cls, nome_saida="exportacao_padaria.json"):
        """Exporta os dados para outro arquivo JSON. Retorna True/False."""
        try:
            dados = cls.carregar()
            if not dados:
                print("Não há dados para exportar.")
                return False
            with open(nome_saida, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            print(f"Dados exportados para: {nome_saida}")
            return True
        except Exception as e:
            print(f"Erro ao exportar: {e}")
            return False

    @classmethod
    def mostrar_arquivo_json(cls):
        """Mostra o conteúdo atual do arquivo JSON (formato legível).

        Depois de mostrar, pergunta ao usuário se deseja salvar esses dados em um arquivo de
        exportação (mesma função que antes de usar .json)."""
        try:
            with open(cls.__arquivo, "r", encoding="utf-8") as f:
                texto = f.read()
                if not texto.strip():
                    print("O arquivo JSON está vazio.")
                else:
                    print("=== Conteúdo do arquivo JSON (padaria.json) ===")
                    # tenta carregar para imprimir de forma bonita
                    try:
                        dado = json.loads(texto)
                        print(json.dumps(dado, indent=4, ensure_ascii=False))
                    except:
                        # caso o arquivo esteja corrompido ou não seja JSON válido
                        print(texto)
                    print("=== Fim do conteúdo ===")
            # perguntar se deseja exportar para outro nome
            resp = input("Deseja exportar esse conteúdo para 'exportacao_padaria.json'? (s/n): ").strip().lower()
            if resp == 's':
                cls.exportar_json()
        except FileNotFoundError:
            print("Arquivo padaria.json não encontrado. Nenhum dado salvo ainda.")
        except Exception as e:
            print(f"Erro ao ler o arquivo JSON: {e}")
