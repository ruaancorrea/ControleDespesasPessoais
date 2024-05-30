
Documentação do Código
O código é uma aplicação que gerencia categorias, receitas e gastos. Utiliza a biblioteca SQLite para armazenar os dados em um banco de dados local. As funções de inserção, deletar e ver dados são utilizadas para manipular as tabelas do banco de dados.

# primeira parte projeto despesas

Documentação da Primeira Parte
Criando Conexão
A primeira parte do código cria uma conexão com o banco de dados SQLite.
python
con = lite.connect("dados.db")

Criando Tabelas
As tabelas "Categoria", "Receitas" e "Gastos" são criadas utilizando comandos SQL.
python
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")
    cur.execute("CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")
    cur.execute("CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")

Funções de Inserção
As funções inserir_categoria, inserir_receita e inserir_gastos são utilizadas para inserir dados nas tabelas.
python
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
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

Funções de Deletar
As funções deletar_receitas e deletar_gastos são utilizadas para deletar dados das tabelas.
python
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

Funções de Ver Dados
A função ver_categorias é utilizada para ver todas as categorias do banco de dados.
python
# Ver Categorias
def ver_categorias():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)


