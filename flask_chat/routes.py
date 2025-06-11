from flask import Blueprint, render_template, request
from datetime import datetime
import os
from .agents.tutor_agent import responder_com_tutor
from .agents.juiz_agent import avaliar_resposta
from .rag.rag_chain import responder_rag


bp = Blueprint("chat", __name__)

def registrar_log(rota, mensagem):
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/{rota}.log"
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        origem = "USUÁRIO" if rota == "usuario" else "ATENDENTE"
        with open(caminho, "a") as f:
            f.write(f"[{timestamp}] [{origem}] {mensagem}\n")

def carregar_historico(rota):
    caminho = f"logs/{rota}.log"
    linhas_coloridas = []
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            linhas = list(reversed(f.readlines()))
            for linha in linhas:
                if "[USUÁRIO]" in linha:
                    cor = "red"
                elif "[ATENDENTE]" in linha:
                    cor = "blue"
                else:
                    cor = "black"
                linhas_coloridas.append(f'<font color="{cor}">{linha.strip()}</font>')
    return linhas_coloridas

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/usuario", methods=["GET", "POST"])
def usuario():
    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("usuario", msg)
        elif "encerrar" in request.form:
            registrar_log("usuario", "CONVERSA ENCERRADA PELO USUÁRIO")
    historico = carregar_historico("usuario")
    return render_template("usuario.html", historico=historico)

@bp.route("/atendente", methods=["GET", "POST"])
def atendente():
    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("atendente", msg)
        elif "encerrar" in request.form:
            registrar_log("atendente", "CONVERSA ENCERRADA PELO ATENDENTE")
    historico = carregar_historico("atendente")
    return render_template("atendente.html", historico=historico)

@bp.route("/ia", methods=["POST"])
def ia():
    pergunta = request.form.get("mensagem")

    if pergunta:
        registrar_log("usuario", pergunta)

        resposta_tutor_rag = responder_rag(pergunta)
        avaliacao = avaliar_resposta(pergunta, resposta_tutor_rag)
        registrar_log("atendente", resposta_tutor_rag)
        registrar_log("atendente", f"AVALIAÇÃO DO JUIZ: {avaliacao}")


    historico_usuario = carregar_historico("usuario")
    historico_atendente = carregar_historico("atendente")
    
    return render_template("usuario.html", historico=historico_usuario + historico_atendente)

@bp.route("/avaliar", methods=["GET", "POST"])
def avaliar():
    resultado = None
    if request.method == "POST":
        pergunta = request.form["mensagem"]
        resposta_tutor = responder_com_tutor(pergunta)
        resultado = {
            "pergunta": pergunta,
            "resposta_tutor": resposta_tutor,
            "avaliacao": avaliar_resposta(pergunta, resposta_tutor)
        }
    return render_template("avaliar.html", resultado=resultado)
