import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import streamlit.components.v1 as components

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
    if "Lamp_on" not in st.session_state:
        st.session_state.lamp_on = False

# ---------------- LOGIN ----------------
# ---------------- ABAJUR ANIMADO ----------------
# ---------------- ABAJUR PRO ----------------
if not st.session_state.lamp_on:

    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        margin: 0;
        background: #121417;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        overflow: hidden;
    }

    .lamp-container {
        position: relative;
        width: 200px;
        height: 300px;
    }

    .shade {
        width: 200px;
        height: 100px;
        background: #f5f0e6;
        border-radius: 50% 50% 0 0;
    }

    .base {
        width: 12px;
        height: 150px;
        background: #ccc;
        margin: auto;
    }

    .light {
        position: absolute;
        top: 90px;
        left: -80px;
        width: 360px;
        height: 250px;
        background: radial-gradient(circle, rgba(255,220,120,0.6), transparent);
        opacity: 0;
        transition: 0.6s;
    }

    /* corda */
    .cord {
        position: absolute;
        top: 100px;
        left: 130px;
        width: 4px;
        height: 80px;
        background: #555;
    }

    .ball {
        position: absolute;
        top: 170px;
        left: 120px;
        width: 20px;
        height: 20px;
        background: gold;
        border-radius: 50%;
        cursor: grab;
    }

    .btn {
        position: absolute;
        top: 260px;
        left: 50%;
        transform: translateX(-50%);
        padding: 10px;
        border-radius: 10px;
        border: none;
        background: gold;
        cursor: pointer;
        display: none;
    }
    </style>
    </head>

    <body>

    <div class="lamp-container">

        <div class="shade"></div>
        <div class="base"></div>
        <div class="light" id="light"></div>

        <div class="cord"></div>
        <div class="ball" id="ball"></div>

        <button class="btn" id="btn">Continuar</button>

    </div>

    <audio id="click" src="https://assets.codepen.io/605876/click.mp3"></audio>

    <script>
    let ball = document.getElementById("ball");
    let light = document.getElementById("light");
    let btn = document.getElementById("btn");
    let click = document.getElementById("click");

    let startY = 0;
    let puxado = false;

    ball.onmousedown = function(e){
        startY = e.clientY;

        document.onmousemove = function(e){
            let move = e.clientY - startY;

            if(move > 0 && move < 60){
                ball.style.top = (170 + move) + "px";
            }

            if(move > 40 && !puxado){
                puxado = true;
                light.style.opacity = 1;
                btn.style.display = "block";
                click.play();
            }
        }

        document.onmouseup = function(){
            ball.style.top = "170px";
            document.onmousemove = null;
        }
    }
    </script>

    </body>
    </html>
    """

    components.html(html_code, height=550)

    st.write("💡 Puxe a corda e depois clique em continuar")

    if st.button("Continuar"):
        st.session_state.lamp_on = True
        st.rerun()

    st.stop()

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
    st.session_state.lamp_on = False
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
