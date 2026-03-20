import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Controle Financeiro", layout="centered")

# ---------------- ARQUIVO USUÁRIOS ----------------
ARQUIVO = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w") as f:
            json.dump([], f)
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO, "w") as f:
        json.dump(usuarios, f, indent=4)

def cadastrar_usuario(usuario, senha):
    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            return False

    usuarios.append({"usuario": usuario, "senha": senha})
    salvar_usuarios(usuarios)
    return True

def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            return True
    return False

# ---------------- SESSION ----------------
if "logado" not in st.session_state:
    st.session_state.logado = False

# ---------------- LOGIN ----------------
if not st.session_state.logado:

    st.title("🔐 Login")

    opcao = st.radio("Escolha", ["Login", "Cadastrar"])

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if opcao == "Login":
        if st.button("Entrar"):
            if verificar_login(usuario, senha):
                st.session_state.logado = True
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

    if opcao == "Cadastrar":
        if st.button("Cadastrar"):
            if usuario and senha:
                if cadastrar_usuario(usuario, senha):
                    st.success("Usuário criado com sucesso!")
                else:
                    st.error("Usuário já existe")
            else:
                st.warning("Preencha todos os campos")

    st.stop()

# ---------------- APP PRINCIPAL ----------------
st.title("💰 Controle Financeiro")

if "transacoes" not in st.session_state:
    st.session_state.transacoes = []

# MENU
menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Adicionar Transação", "Ver Transações"]
)

# BOTÃO SAIR (CORRIGIDO)
if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

# TEMA
tema = st.sidebar.selectbox(
    "Escolha o tema",
    ["Claro", "Escuro"]
)

if tema == "Escuro":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- TELAS ----------------

if menu == "Adicionar Transação":

    st.header("Adicionar Transação")

    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])

    categoria = st.selectbox(
        "Categoria",
        ["Salário", "Alimentação", "Transporte", "Lazer", "Outros"]
    )

    valor = st.number_input("Valor", min_value=0.0)

    descricao = st.text_input("Descrição")

    if st.button("Salvar"):
        transacao = {
            "tipo": tipo,
            "categoria": categoria,
            "valor": valor,
            "descricao": descricao
        }

        st.session_state.transacoes.append(transacao)
        st.success("Transação salva!")

elif menu == "Ver Transações":

    st.header("Transações")

    df = pd.DataFrame(st.session_state.transacoes)
    st.write(df)

elif menu == "Dashboard":

    st.header("Dashboard")

    df = pd.DataFrame(st.session_state.transacoes)

    if not df.empty:

        receitas = df[df["tipo"] == "Receita"]["valor"].sum()
        despesas = df[df["tipo"] == "Despesa"]["valor"].sum()

        saldo = receitas - despesas

        st.metric("Receitas", f"R${receitas:.2f}")
        st.metric("Despesas", f"R${despesas:.2f}")
        st.metric("Saldo", f"R${saldo:.2f}")

        gastos = df[df["tipo"] == "Despesa"]

        if not gastos.empty:

            grafico = gastos.groupby("categoria")["valor"].sum()

            fig, ax = plt.subplots()
            grafico.plot(kind="pie", autopct="%1.1f%%", ax=ax)

            st.pyplot(fig)

            media_gastos = gastos["valor"].mean()
            st.metric("Média de gastos", f"R$ {media_gastos:.2f}")

    else:
        st.write("Nenhuma transação cadastrada.")