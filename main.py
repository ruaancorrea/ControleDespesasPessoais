from tkinter import *
from tkinter import Tk,ttk
from tkinter import messagebox
# Importando Pillow
from view import con
from PIL import Image, ImageTk

# Importando Barra Progresso do Tkinter
from tkinter.ttk import Progressbar


# Importando Funcoes Da View
from view import bar_valores,pie_valores, inserir_categoria,ver_categorias, inserir_receita, inserir_gastos,tabela,deletar_gastos,deletar_receitas,porcentagem_valor,limpar_categorias_db

#importando Matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# tkcalendar
from tkcalendar import Calendar, DateEntry
from datetime import date

# Cores Usar Projetos

################# cores ###############
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"
co6 = "#038cfc" 
co7 = "#3fbfb9"   
co8 = "#263238"  
co9 = "#e9edf5" 

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# Criando Janela
janela = Tk()
janela.title()
janela.geometry("900x650")
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style=  ttk.Style(janela)
style.theme_use("clam")

# Criando Frames Para Divisão Da Tela

frameCima = Frame(janela, width=1043, height=50, bg=co1,  relief="flat",)
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela,width=1043, height=361,bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0,pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela,width=1043, height=300,bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_2 = Frame(frameMeio, width=580, height=250,bg=co2)
frame_gra_2.place(x=415, y=5)

# Trabalhando no frame Cima

# Abrindo Imagem

def criar_logo():
    app_img = Image.open("log.png")
    new_size = (45,45)
    app_img = app_img.resize(new_size)
    app_img = ImageTk.PhotoImage(app_img)

    app_logo = Label(frameCima, image=app_img, text=" Orçamento Pessoal", width=900,compound=LEFT, padx=5,relief=RAISED, anchor=NW, font=("Verdana 20 bold"), bg=co1, fg=co4)
    app_logo.place(x=0, y=0)
    return app_img

app_img = criar_logo()

# Definindo tree Como Global

global tree

# Funcao Inserir Categoria 

def inserir_categoria_b():
    
    nome = e_categoria.get()
    
    lista_inserir = [nome]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha Todos Os Campos")
            return

    # Passando Para Função Inserir Gastos Presente Na View
    
    inserir_categoria(lista_inserir)

    messagebox.showinfo("Sucesso", "Os Dados Foram Inseridos Com Sucesso")
    e_categoria.delete(0,"end")
    # Pegando Os Valores Da Categoria 
    categorias_funcao = ver_categorias()
    categorias = []

    for i in categorias_funcao:
        categorias.append(i[1])


    # Atualizando A Lista De Categorias

    combo_categoria_despesas["values"] = (categorias)

    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()



def limpar_categorias(con):
    limpar_categorias_db(con)
    messagebox.showinfo("Sucesso", "As categorias foram limpas com sucesso!")


# Funcao Inserir Receitas

def inserir_receita_b():
    nome = "Receita"
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha Todos Os Campos")
            return

    # Chamando a função inserir_receita presente na view
    inserir_receita(lista_inserir)

    messagebox.showinfo("Sucesso", "Os Dados Foram Inseridos Com Sucesso")

    e_cal_receitas.delete(0, "end")
    e_valor_receitas.delete(0, "end")

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

 # Funcao Inserir Despesas

def inserir_despesas_b():
    
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha Todos Os Campos")
            return
        

    # Chamando A Funcao Inserir Despesas Presente Na View
        
    inserir_gastos(lista_inserir)
        
    messagebox.showinfo("Sucesso", "Os Dados Foram Inseridos Com Sucesso")

    combo_categoria_despesas.delete(0,"end") 

    e_cal_despesas.delete(0,"end")
        
    e_valor_despesas.delete(0,"end")

        # Atualizando Dados

    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()



# Funcao Deletar ----------------

def deletar_dados():
    try:
        selected_items = tree.selection()
        
        for selected_item in selected_items:
            treev_dicionario = tree.item(selected_item)
            treev_lista = treev_dicionario["values"]
            valor = treev_lista[0]
            nome = treev_lista[1]

            if nome == "Receita":
                deletar_receitas([valor])
            else:
                deletar_gastos([valor])

        messagebox.showinfo("Sucesso", "Os Dados Selecionados Foram Deletados Com Sucesso")

        # Atualizando Dados
        mostrar_renda()
        porcentagem()
        grafico_bar()
        atualizar_resumo()
        resumo()
        grafico_pie()
    except IndexError:
        messagebox.showerror("Erro", "Selecione Um Ou Mais Dados Na Tabela")



# porcetagem -----------------------

def porcentagem():
    l_nome = Label(frameMeio, text="Porcetagem Da Receita Restante", height=1,anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMeio,length=180,style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar["value"] = porcentagem_valor()[0]

    valor = porcentagem_valor()[0]
    l_porcentagem = Label(frameMeio, text='{:,.2f} %'.format(valor), height=1,anchor=NW, font=('Verdana 12 '), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)
porcentagem()

# Função Para Grafico Barra --------------------

def grafico_bar():
    lista_categorias = ["Renda", "Despesas", "Saldo"]
    lista_valores = bar_valores()

    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    # ax.autoscale(enable=True, axis='both', tight=None)
    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)

    # create a list to collect the plt.patches data
    c = 0

    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')

        c += 1
    

    ax.set_xticks(range(len(lista_categorias)))

    ax.set_xticklabels(lista_categorias,fontsize=16)
    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

    # -----------------------------------------------------------------------------------------
grafico_bar()


def atualizar_resumo():
    valor = bar_valores()

    l_total_renda_valor.config(text='R$ {:.2f}'.format(valor[0]))
    l_total_despesas_valor.config(text='R$ {:.2f}'.format(valor[1]))
    l_total_saldo_valor.config(text='R$ {:.2f}'.format(valor[2]))

def resumo():
    global l_total_renda_valor, l_total_despesas_valor, l_total_saldo_valor

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('arial 1 '), bg='#545454')
    l_linha.place(x=309, y=52)
    l_total_renda_label = Label(frameMeio, text="Total Renda Mensal      ".upper(), height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_total_renda_label.place(x=306, y=35)
    l_total_renda_valor = Label(frameMeio, text='R$ 0.00', height=1, anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_total_renda_valor.place(x=306, y=70)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('arial 1 '), bg='#545454')
    l_linha.place(x=309, y=132)
    l_total_despesas_label = Label(frameMeio, text="Total Despesas Mensais".upper(), height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_total_despesas_label.place(x=306, y=115)
    l_total_despesas_valor = Label(frameMeio, text='R$ 0.00', height=1, anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_total_despesas_valor.place(x=306, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('arial 1 '), bg='#545454')
    l_linha.place(x=309, y=207)
    l_total_saldo_label = Label(frameMeio, text="Total Saldo da Caixa    ".upper(), height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_total_saldo_label.place(x=306, y=190)
    l_total_saldo_valor = Label(frameMeio, text='R$ 0.00', height=1, anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_total_saldo_valor.place(x=306, y=220)

    atualizar_resumo()

resumo()



# ----------------------------------------------------------------------------------------
# funcao grafico pie
def grafico_pie():
    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)
    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = []
    for i in lista_categorias:
        explode.append(0.05)
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_2)
    canva_categoria.get_tk_widget().grid(row=0,column=0)

grafico_pie()




# Criando Frames Dentro Do Frame Baixo

frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0,column=0)


frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0,column=1,padx=5)


frame_configuracao = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_configuracao.grid(row=0,column=2, padx=5)


#Tabela Renda Mensal -----------------------------------------------

app_tabela = Label(frameMeio, text="Tabela Receitas E Despesas", anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)


#Funcao Para Mostrar Tabela -------------------

def mostrar_renda():

    # creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()

    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])

        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)
mostrar_renda()

# Configuracoes Despesas

l_descricao = Label(frame_operacoes, text="Insira Novas Despesas", height=1,anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
l_descricao.place(x=10,y=10)

# Categoria

l_categoria = Label(frame_operacoes, text="Categoria", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

# Criar ComboBox (PEGANDO CATEGORIAS) -------

categoria_funcao = ver_categorias()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1]) #isso pegara apenas categoria deixando o id para la na pos = 0

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=("Ivy 10"))
combo_categoria_despesas["values"] = (categoria)
combo_categoria_despesas.place(x=110, y=41) 

# Despesas -------------

l_cal_despesas = Label(frame_operacoes, text="Data", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12, background="darkblue", foreground="white", borderwidth=2, year=2024)
e_cal_despesas.place(x=110,y=71)


# Valor ---------------

l_valor_despesas = Label(frame_operacoes, text="Quantia Total", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)


e_valor_despesas = Entry(frame_operacoes, width=14, justify="left", relief="solid")
e_valor_despesas.place(x=110,y=101)


# Botao Inserir

img_add_despesas = Image.open("add.png")
new_size = (45,45)
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes,command=inserir_despesas_b, image=img_add_despesas, text=" Adicionar".upper(), width=80,compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)




# Botao Excluir
l_excluir = Label(frame_operacoes, text="Excluir Ação", height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)


img_delete = Image.open("delete.png")
new_size = (45,45)
img_delete = img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes,command=deletar_dados,image=img_delete, text=" Deletar".upper(), width=80,compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE)
botao_deletar.place(x=110, y=190)



# Configuracoes Receitas ---------------------

l_descricao = Label(frame_configuracao, text="Insira Novas Receitas", height=1,anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
l_descricao.place(x=10,y=10)


# Calendario -------------

l_cal_receitas = Label(frame_configuracao, text="Data", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background="darkblue", foreground="white", borderwidth=2, year=2024)
e_cal_receitas.place(x=110,y=41)


# Valor -------------

l_valor_receitas = Label(frame_configuracao, text="Quantia Total", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify="left", relief="solid")
e_valor_receitas.place(x=110,y=71)


# Botao Inserir

img_add_receitas = Image.open("add.png")
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao,command=inserir_receita_b, image=img_add_receitas, text=" Adicionar".upper(), width=80,compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=101)

# Operação Nova Categoria ---------------------

l_descricao = Label(frame_configuracao, text="Categoria", height=1,anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
l_descricao.place(x=10,y=160)


e_categoria = Entry(frame_configuracao, width=14, justify="left", relief="solid")
e_categoria.place(x=110,y=160)

# Botao Inserir Categoria

img_add_categoria = Image.open("add.png")
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_receitas = Button(frame_configuracao,command=inserir_categoria_b, image=img_add_categoria, text=" Adicionar".upper(), width=80,compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=180)


# Botao Limpar Categorias

img_delete_categoria = Image.open("delete.png")
img_delete_categoria = img_delete_categoria.resize((17,17))
img_delete_categoria = ImageTk.PhotoImage(img_delete_categoria)
botao_limpar_categorias = Button(frame_configuracao, text="Limpar Categorias", command=lambda: limpar_categorias(con), image=img_delete_categoria, compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE)
botao_limpar_categorias.place(x=110, y=210)


janela.mainloop()