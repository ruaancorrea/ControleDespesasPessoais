Documentação do Sistema de Gerenciamento de Receitas e Despesas
Descrição Geral
Este sistema é uma aplicação de gerenciamento de finanças pessoais construída em Python. Utiliza a biblioteca Tkinter para a interface gráfica, Matplotlib para a criação de gráficos, SQLite para o banco de dados e Pandas para manipulação de dados. O aplicativo permite que os usuários registrem receitas e despesas, visualizem esses dados em uma tabela e em gráficos de pizza, e gerenciem categorias de despesas.

Bibliotecas e Frameworks Utilizados
tkinter: Biblioteca padrão do Python para a criação de interfaces gráficas.
tkcalendar: Biblioteca que fornece widgets de calendário para o Tkinter.
matplotlib: Biblioteca para criação de gráficos em Python.
PIL (Pillow): Biblioteca para manipulação de imagens no Python.
ttk: Subconjunto do Tkinter que fornece widgets com estilos melhorados.
sqlite3: Biblioteca para interação com bancos de dados SQLite.
pandas: Biblioteca para manipulação e análise de dados.
Estrutura do Código
Importação das Bibliotecas
Primeiramente, importamos todas as bibliotecas necessárias para o funcionamento do sistema.

python
Copiar
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import sqlite3 as lite
import pandas as pd
Conexão com o Banco de Dados
Estabelecemos uma conexão com o banco de dados SQLite chamado dados.db.

python
Copiar
# Criando Conexão
con = lite.connect("dados.db")
Funções de Inserção
Estas funções são responsáveis por inserir dados nas tabelas Categoria, Receitas e Gastos no banco de dados.

python
Copiar
# Inserir Categoria
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query, i)

# Inserir Receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Inserir Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)
Funções de Deleção
Funções para deletar dados das tabelas Receitas, Gastos e Categoria no banco de dados.

python
Copiar
# Deletar Receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

# Deletar Gastos
def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

# Deletar Categorias
def limpar_categorias_db(con):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Categoria"
        cur.execute(query)
        con.commit()
Funções para Visualizar Dados
Funções para obter dados das tabelas Categoria, Receitas e Gastos.

python
Copiar
# Ver Categorias
def ver_categorias():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver Receitas
def ver_receitas():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver Gastos
def ver_gastos():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens
Funções Auxiliares
Funções auxiliares para manipulação e agregação de dados.

python
Copiar
# Combina receitas e gastos em uma tabela única
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()
    tabela_lista = []
    for i in gastos:
        tabela_lista