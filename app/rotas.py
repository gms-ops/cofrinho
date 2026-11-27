from datetime import date
from decimal import Decimal

from flask import (Blueprint, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)

from .dominio.calculos import (calcular_faltante, calcular_mensalidade,
                               calcular_progresso, esta_atrasada,
                               meses_restantes)
from .dominio.erros import ErroValidacao
from .dominio.filtros import buscar_por_nome, filtrar_por_status, ordenar_metas
from .dominio.meta import criar_meta, depositar, editar_meta, retirar

bp = Blueprint("metas", __name__)


def _repo():
    return current_app.extensions["repositorio"]


def _hoje():
    return current_app.config.get("HOJE") or date.today()


def _resumo(meta):
    hoje = _hoje()
    return {
        "meta": meta,
        "progresso": calcular_progresso(meta),
        "faltante": calcular_faltante(meta),
        "mensalidade": calcular_mensalidade(meta, hoje),
        "meses": meses_restantes(meta, hoje),
        "atrasada": esta_atrasada(meta, hoje),
    }


@bp.get("/saude")
def saude():
    return jsonify(status="ok")


@bp.get("/")
def index():
    todas = _repo().listar()
    q = request.args.get("q", "")
    status = request.args.get("status", "todas")
    ordem = request.args.get("ordem", "prazo")
    try:
        metas = ordenar_metas(buscar_por_nome(filtrar_por_status(todas, status), q), ordem)
    except ErroValidacao as erro:
        flash(str(erro), "erro")
        q, status, ordem = "", "todas", "prazo"
        metas = ordenar_metas(todas, ordem)
    total = sum((m.saldo for m in todas), Decimal("0.00"))
    return render_template(
        "index.html",
        resumos=[_resumo(m) for m in metas],
        total=total,
        q=q,
        status=status,
        ordem=ordem,
    )


@bp.post("/metas")
def criar():
    try:
        meta = criar_meta(
            request.form.get("nome"),
            request.form.get("alvo"),
            request.form.get("prazo"),
            _hoje(),
        )
        _repo().adicionar(meta)
        flash("Meta criada.", "ok")
    except ErroValidacao as erro:
        flash(str(erro), "erro")
    return redirect(url_for("metas.index"))


@bp.post("/metas/<int:meta_id>/deposito")
def fazer_deposito(meta_id):
    meta = _repo().obter(meta_id)
    try:
        atualizada = depositar(meta, request.form.get("valor"))
    except ErroValidacao as erro:
        flash(str(erro), "erro")
        return redirect(url_for("metas.index"))
    _repo().atualizar(atualizada)
    if atualizada.concluida and not meta.concluida:
        flash(f"Parabéns! Você alcançou a meta {meta.nome}.", "ok")
    else:
        flash("Depósito registrado.", "ok")
    return redirect(url_for("metas.index"))


@bp.post("/metas/<int:meta_id>/retirada")
def fazer_retirada(meta_id):
    meta = _repo().obter(meta_id)
    try:
        _repo().atualizar(retirar(meta, request.form.get("valor")))
        flash("Retirada registrada.", "ok")
    except ErroValidacao as erro:
        flash(str(erro), "erro")
    return redirect(url_for("metas.index"))


@bp.route("/metas/<int:meta_id>/editar", methods=["GET", "POST"])
def editar(meta_id):
    meta = _repo().obter(meta_id)
    if request.method == "POST":
        try:
            atualizada = editar_meta(
                meta,
                nome=request.form.get("nome"),
                alvo=request.form.get("alvo"),
                prazo=request.form.get("prazo"),
                hoje=_hoje(),
            )
            _repo().atualizar(atualizada)
            flash("Meta atualizada.", "ok")
            return redirect(url_for("metas.index"))
        except ErroValidacao as erro:
            flash(str(erro), "erro")
    return render_template("editar.html", meta=meta)


@bp.post("/metas/<int:meta_id>/remover")
def remover(meta_id):
    _repo().remover(meta_id)
    flash("Meta removida.", "ok")
    return redirect(url_for("metas.index"))
