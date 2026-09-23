# Tema: Rede Social
# Integrantes: Beatriz Neves, Gabriel Borges, Joice Celestino e Victor (Vic) Novo
# 15 usuarios: Ana, Bruno, Carla, Daniel, Sabrina, Felipe, Gabriela, Henrique, Isabela, João, Karen, Luis, Marina, Nicolas, Olivia.

# Amizades:
# Ana - Bruno, Carla, Sabrina
# Bruno - Daniel, Felipe, Ana
# Carla - Daniel, Gabriela, Ana
# Daniel - Henrique, Bruno, Carla
# Sabrina - Gabriela, Isabela, Ana
# Felipe - Henrique, João, Bruno
# Gabriela - Henrique, Karen, Carla, Sabrina
# Henrique - Luis, Daniel, Felipe, Gabriela
# Isabela - Marina, Karen, Sabrina
# João - Luis, Nicolas, Felipe
# Karen - Luis, Isabela, Gabriela
# Luis - Marina, Olivia, Henrique, João, Karen
# Marina - Nicolas, Luis, Isabela
# Nicolas - Olivia, João, Marina
# Olivia - Luis, Nicolas

from collections import deque

amizades = [
    ("Ana", "Bruno"), ("Ana", "Carla"), ("Ana", "Sabrina"),
    ("Bruno", "Daniel"), ("Bruno", "Felipe"),
    ("Carla", "Daniel"), ("Carla", "Gabriela"),
    ("Daniel", "Henrique"),
    ("Sabrina", "Gabriela"), ("Sabrina", "Isabela"),
    ("Felipe", "Henrique"), ("Felipe", "Joao"),
    ("Gabriela", "Henrique"), ("Gabriela", "Karen"),
    ("Henrique", "Luis"),
    ("Isabela", "Marina"), ("Isabela", "Karen"),
    ("Joao", "Luis"), ("Joao", "Nicolas"),
    ("Karen", "Luis"),
    ("Luis", "Marina"), ("Luis", "Olivia"),
    ("Marina", "Nicolas"),
    ("Nicolas", "Olivia"),
]


class RedeSocial:
    def __init__(self):
        # cada usuário guarda o conjunto dos seus amigos
        self.adjacencia = {}

    def add_usuario(self, nome):
        if nome not in self.adjacencia:
            self.adjacencia[nome] = set()

    def add_amizade(self, usuario1, usuario2):
        self.add_usuario(usuario1)
        self.add_usuario(usuario2)
        self.adjacencia[usuario1].add(usuario2)
        self.adjacencia[usuario2].add(usuario1)

    def sao_amigos(self, usuario1, usuario2):
        # usado no menu pra não cadastrar a mesma amizade duas vezes
        return usuario2 in self.adjacencia[usuario1]

    def imprimir_lista_adjacencia(self):
        for usuario, amigos in sorted(self.adjacencia.items()):
            print(usuario, "->", sorted(amigos))

    def matriz_adjacencia(self):
        usuarios = sorted(self.adjacencia.keys())
        n = len(usuarios)
        matriz = [[0] * n for _ in range(n)]  # cria a matriz vazia
        indice = {nome: posicao for posicao, nome in enumerate(usuarios)}
        for i, usuario in enumerate(usuarios):
            for amigo in self.adjacencia[usuario]:
                j = indice[amigo]
                matriz[i][j] = 1
        return usuarios, matriz

    # bfs - busca em largura - fila
    def bfs(self, inicio):
        visitados = {inicio}
        ordem = [inicio]
        fila = deque([inicio])

        while fila:
            atual = fila.popleft()
            for vizinho in sorted(self.adjacencia[atual]):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    ordem.append(vizinho)
                    fila.append(vizinho)
        return ordem

    # dfs - busca em profundidade
    def dfs(self, inicio):
        visitados = set()
        ordem = []

        def _visita(atual):
            visitados.add(atual)
            ordem.append(atual)
            for vizinho in sorted(self.adjacencia[atual]):
                if vizinho not in visitados:
                    _visita(vizinho)

        _visita(inicio)
        return ordem

    def caminho(self, origem, destino):
        if origem == destino:
            return [origem]

        visitados = {origem}
        pai = {origem: None}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()

            for vizinho in sorted(self.adjacencia[atual]):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pai[vizinho] = atual

                    if vizinho == destino:
                        caminho = [destino]

                        # volta seguindo os pais até chegar na origem
                        while pai[caminho[-1]] is not None:
                            caminho.append(pai[caminho[-1]])
                        caminho.reverse()
                        return caminho

                    fila.append(vizinho)
        return None


# ---------- funções do menu ----------

def buscar_usuario(rede, texto):
    # procura o nome sem ligar pra maiúscula/minúscula
    # e devolve do jeito que está cadastrado (ou None se não achar)
    texto = texto.strip().lower()
    for nome in rede.adjacencia:
        if nome.lower() == texto:
            return nome
    return None


def pedir_usuario(rede, mensagem):
    # repete a pergunta até o nome existir, enter em branco cancela
    while True:
        texto = input(mensagem)
        if texto.strip() == "":
            return None
        nome = buscar_usuario(rede, texto)
        if nome is not None:
            return nome
        print("Usuário não encontrado, confere a grafia (a opção 1 mostra todos).")


def mostrar_menu():
    print("\n===== REDE SOCIAL =====")
    print("1 - Lista de adjacência")
    print("2 - Matriz de adjacência")
    print("3 - BFS a partir de um usuário")
    print("4 - DFS a partir de um usuário")
    print("5 - Caminho mais curto entre duas pessoas")
    print("6 - Adicionar usuário")
    print("7 - Adicionar amizade")
    print("0 - Sair")


def ver_matriz(rede):
    usuarios, matriz = rede.matriz_adjacencia()
    # só as 3 primeiras letras no cabeçalho pra caber na tela
    cabecalho = "".ljust(10) + "".join(u[:3].rjust(4) for u in usuarios)
    print(cabecalho)
    for usuario, linha in zip(usuarios, matriz):
        print(usuario.ljust(10) + "".join(str(v).rjust(4) for v in linha))


def menu_bfs(rede):
    inicio = pedir_usuario(rede, "Começar por quem? (enter cancela): ")
    if inicio is None:
        return
    print(f"\n=== BFS a partir de '{inicio}' ===")
    print(" -> ".join(rede.bfs(inicio)))


def menu_dfs(rede):
    inicio = pedir_usuario(rede, "Começar por quem? (enter cancela): ")
    if inicio is None:
        return
    print(f"\n=== DFS a partir de '{inicio}' ===")
    print(" -> ".join(rede.dfs(inicio)))


def menu_caminho(rede):
    origem = pedir_usuario(rede, "Origem (enter cancela): ")
    if origem is None:
        return
    destino = pedir_usuario(rede, "Destino (enter cancela): ")
    if destino is None:
        return

    caminho_encontrado = rede.caminho(origem, destino)
    print(f"\n=== Caminho entre '{origem}' e '{destino}' ===")
    if caminho_encontrado:
        print(" -> ".join(caminho_encontrado))
        print(f"Distancia: {len(caminho_encontrado) - 1} amizade(s)")
    else:
        print("Não há caminho entre esses usuarios.")


def menu_add_usuario(rede):
    nome = input("Nome do novo usuário (enter cancela): ").strip().title()
    if nome == "":
        return
    if buscar_usuario(rede, nome) is not None:
        print(f"{nome} já está na rede.")
        return
    rede.add_usuario(nome)
    print(f"{nome} entrou na rede, ainda sem amigos.")


def menu_add_amizade(rede):
    usuario1 = pedir_usuario(rede, "Primeiro usuário (enter cancela): ")
    if usuario1 is None:
        return
    usuario2 = pedir_usuario(rede, "Segundo usuário (enter cancela): ")
    if usuario2 is None:
        return

    if usuario1 == usuario2:
        print("Não dá pra ser amigo de si mesmo.")
        return
    if rede.sao_amigos(usuario1, usuario2):
        print(f"{usuario1} e {usuario2} já são amigos.")
        return

    rede.add_amizade(usuario1, usuario2)
    print(f"Pronto, {usuario1} e {usuario2} agora são amigos.")


def main():
    rede = RedeSocial()

    # carrega as amizades iniciais da lista lá de cima
    for usuario1, usuario2 in amizades:
        rede.add_amizade(usuario1, usuario2)

    print(f"Total de usuarios: {len(rede.adjacencia)}")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n=== LISTA DE ADJACENCIA ===")
            rede.imprimir_lista_adjacencia()
        elif opcao == "2":
            print("\n=== MATRIZ DE ADJACENCIA ===")
            ver_matriz(rede)
        elif opcao == "3":
            menu_bfs(rede)
        elif opcao == "4":
            menu_dfs(rede)
        elif opcao == "5":
            menu_caminho(rede)
        elif opcao == "6":
            menu_add_usuario(rede)
        elif opcao == "7":
            menu_add_amizade(rede)
        elif opcao == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida, tenta de novo.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # ctrl+c ou fim da entrada, sai sem mostrar erro
        print("\nEncerrado.")