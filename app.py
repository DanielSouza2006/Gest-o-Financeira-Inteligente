import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import html


# 1. IMPORTS (O que você já tem)
from flask import Flask, request, jsonify
from flask_cors import CORS

# 2. CONFIGURAÇÃO (Logo abaixo dos imports)
app = Flask(__name__)
CORS(app)

# 3. AS ROTAS (A lógica que processa o login)
@app.route('/login', methods=['POST'])
def verificar_login():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    
    if usuario == "admin" and senha == "12345":
        return jsonify({"mensagem": "Sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Erro!"}), 401



# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Controle Financeiro", layout="centered")

def local_css(file_name):
    path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Carrega o CSS global
local_css("style.css")

# ---------------- APP PRINCIPAL ----------------
st.title("💰 Controle Financeiro")

if "transacoes" not in st.session_state:
    st.session_state.transacoes = []

# MENU
menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Adicionar Transação", "Ver Transações"]
)

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
        <div class="dark-mode"></div>
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

        # 4. START (No final de tudo)
if __name__ == '__main__':
    app.run(debug=True)
