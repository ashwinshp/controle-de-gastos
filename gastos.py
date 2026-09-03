import tkinter as tk
import json


#abrir o arquivo gastos.json criado que armazena todos os gastos adicionados.
def carregar_gastos(): 
    try:
        with open("gastos.json", "r") as arquivo: 
            return json.load(arquivo)
    except FileNotFoundError:
        return []


gastos = carregar_gastos()
indice_editando = None


#salva todos os gastos
def salvar_gastos():
    with open("gastos.json", "w") as arquivo:
        json.dump(gastos, arquivo)


#abre a janela do programinha
janela = tk.Tk()

janela.title("Controle de Gastos")
janela.geometry("420x560")
janela.configure(bg="#f5f6f8")


#titulo do programinha
titulo = tk.Label(
    janela,
    text="Controle de Gastos",
    font=("Times", 18, "bold"),
    bg="#f5f6f8",
    fg="#4A55BB"
)

titulo.pack(pady=(18, 2))


#campos para digitação
frame_campos = tk.Frame(
    janela,
    bg="white",
    padx=18,
    pady=12
)

frame_campos.pack(
    padx=20,
    fill="x"
)


#campo de descrição
descricao_label = tk.Label(
    frame_campos,
    text="Descrição",
    font=("Times", 12, "bold"),
    bg="white",
    fg="#232158"
)

descricao_label.pack(anchor="w")

descricao = tk.Entry(
    frame_campos,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

descricao.pack(
    fill="x",
    pady=(3, 8)
)


#categoria
categoria_label = tk.Label(
    frame_campos,
    text="Categoria",
    font=("Times", 12, "bold"),
    bg="white",
    fg="#232158"
)

categoria_label.pack(anchor="w")

categoria = tk.Entry(
    frame_campos,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

categoria.pack(
    fill="x",
    pady=(3, 8)
)


#valor
valor_label = tk.Label(
    frame_campos,
    text="Valor",
    font=("Times", 12, "bold"),
    bg="white",
    fg="#232158"
)

valor_label.pack(anchor="w")

valor = tk.Entry(
    frame_campos,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

valor.pack(
    fill="x"
)


#lista dos gastos ordenados
lista_titulo = tk.Label(
    janela,
    text="Seus gastos",
    font=("Times", 14, "bold"),
    bg="#f5f6f8",
    fg="#232158"
)

lista_titulo.pack(
    anchor="w",
    padx=20,
    pady=(14, 5)
)


lista_gastos = tk.Listbox(
    janela,
    height=7,
    font=("Arial", 9),
    relief="solid",
    bd=1,
    bg="white",
    fg="#333333",
    selectbackground="#4a90e2",
    selectforeground="white"
)

lista_gastos.pack(
    padx=20,
    fill="x"
)


#total
total_label = tk.Label(
    janela,
    text="Total: R$ 0.00",
    font=("Times", 13, "bold"),
    bg="#f5f6f8",
    fg="#D30000"
)

total_label.pack(
    anchor="w",
    padx=20,
    pady=(10, 2)
)


#mensagem
mensagem_label = tk.Label(
    janela,
    text="",
    font=("Arial", 8),
    bg="#f5f6f8",
    fg="#666666"
)

mensagem_label.pack(
    pady=(0, 6)
)


#função atualizar total
def atualizar_total():

    total = 0

    for gasto in gastos:
        total = total + gasto["valor_gasto"]

    total_label.config(
        text=f"Total: R$ {total:.2f}"
    )


#função adicionar gasto
def adicionar_gasto():

    if descricao.get() == "":
        mensagem_label.config(
            text="Digite uma descrição!"
        )
        return

    if categoria.get() == "":
        mensagem_label.config(
            text="Digite uma categoria!"
        )
        return

    try:
        valor_gasto = float(valor.get())

    except ValueError:
        mensagem_label.config(
            text="Digite um valor válido!"
        )
        return

    gasto = {
        "descricao": descricao.get(),
        "categoria": categoria.get(),
        "valor_gasto": valor_gasto
    }

    gastos.append(gasto)

    salvar_gastos()

    lista_gastos.insert(
        tk.END,
        f"{descricao.get()} • {categoria.get()} • R$ {valor_gasto:.2f}"
    )

    atualizar_total()

    descricao.delete(0, tk.END)
    categoria.delete(0, tk.END)
    valor.delete(0, tk.END)

    mensagem_label.config(
        text="Gasto adicionado com sucesso!"
    )


#função excluir gasto
def excluir_gasto():

    selecionado = lista_gastos.curselection()

    if selecionado == ():
        mensagem_label.config(
            text="Selecione um gasto para excluir!"
        )
        return

    indice = selecionado[0]

    gastos.pop(indice)

    salvar_gastos()

    lista_gastos.delete(indice)

    atualizar_total()

    mensagem_label.config(
        text="Gasto excluído com sucesso!"
    )


#função editar gasto
def editar_gasto():

    global indice_editando

    selecionado = lista_gastos.curselection()

    if selecionado == ():
        mensagem_label.config(
            text="Selecione um gasto para editar!"
        )
        return

    indice = selecionado[0]

    indice_editando = indice

    gasto = gastos[indice]

    descricao.delete(0, tk.END)
    descricao.insert(0, gasto["descricao"])

    categoria.delete(0, tk.END)
    categoria.insert(0, gasto["categoria"])

    valor.delete(0, tk.END)
    valor.insert(0, gasto["valor_gasto"])

    mensagem_label.config(
        text="Edite os dados e salve a alteração."
    )


#função salvar alteração
def salvar_alteracao():

    global indice_editando

    if indice_editando is None:
        mensagem_label.config(
            text="Selecione um gasto e clique em EDITAR."
        )
        return

    if descricao.get() == "":
        mensagem_label.config(
            text="Digite uma descrição!"
        )
        return

    if categoria.get() == "":
        mensagem_label.config(
            text="Digite uma categoria!"
        )
        return

    try:
        valor_gasto = float(valor.get())

    except ValueError:
        mensagem_label.config(
            text="Digite um valor válido!"
        )
        return

    gastos[indice_editando] = {
        "descricao": descricao.get(),
        "categoria": categoria.get(),
        "valor_gasto": valor_gasto
    }

    salvar_gastos()

    lista_gastos.delete(0, tk.END)

    for gasto in gastos:

        lista_gastos.insert(
            tk.END,
            f"{gasto['descricao']} • {gasto['categoria']} • R$ {gasto['valor_gasto']:.2f}"
        )

    atualizar_total()

    descricao.delete(0, tk.END)
    categoria.delete(0, tk.END)
    valor.delete(0, tk.END)

    indice_editando = None

    mensagem_label.config(
        text="Gasto alterado com sucesso!"
    )


#mostrar gastos salvos
for gasto in gastos:

    lista_gastos.insert(
        tk.END,
        f"{gasto['descricao']} • {gasto['categoria']} • R$ {gasto['valor_gasto']:.2f}"
    )


atualizar_total()


#botões
frame_botoes = tk.Frame(
    janela,
    bg="#f5f6f8"
)

frame_botoes.pack(
    padx=20,
    fill="x"
)


#adicionar
botao_adicionar = tk.Button(
    frame_botoes,
    text="ADICIONAR GASTO",
    command=adicionar_gasto,
    font=("Arial", 9, "bold"),
    bg="#4a90e2",
    fg="white",
    relief="flat",
    padx=8,
    pady=7,
    cursor="hand2"
)

botao_adicionar.pack(
    fill="x",
    pady=(0, 6)
)


#editar
botao_editar = tk.Button(
    frame_botoes,
    text="EDITAR",
    command=editar_gasto,
    font=("Arial", 9, "bold"),
    bg="#e9ecef",
    fg="#333333",
    relief="flat",
    padx=5,
    pady=6,
    cursor="hand2"
)

botao_editar.pack(
    side="left",
    expand=True,
    fill="x",
    padx=(0, 3)
)


#salvar
botao_salvar_alteracao = tk.Button(
    frame_botoes,
    text="SALVAR",
    command=salvar_alteracao,
    font=("Arial", 9, "bold"),
    bg="#e9ecef",
    fg="#333333",
    relief="flat",
    padx=5,
    pady=6,
    cursor="hand2"
)

botao_salvar_alteracao.pack(
    side="left",
    expand=True,
    fill="x",
    padx=3
)


#excluir
botao_excluir = tk.Button(
    frame_botoes,
    text="EXCLUIR",
    command=excluir_gasto,
    font=("Arial", 9, "bold"),
    bg="#e9ecef",
    fg="#333333",
    relief="flat",
    padx=5,
    pady=6,
    cursor="hand2"
)

botao_excluir.pack(
    side="left",
    expand=True,
    fill="x",
    padx=(3, 0)
)


#iniciar programa
janela.mainloop()