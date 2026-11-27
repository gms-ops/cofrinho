import os

from flask import Flask, render_template

from .dominio.erros import MetaNaoEncontrada
from .dominio.formatacao import formatar_data, formatar_moeda, formatar_percentual
from .repositorio import RepositorioMetas


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "chave-de-desenvolvimento"),
        ARQUIVO_DADOS=os.environ.get("COFRINHO_DADOS", "dados.json"),
        HOJE=None,
    )
    if config:
        app.config.update(config)

    app.extensions["repositorio"] = RepositorioMetas(app.config["ARQUIVO_DADOS"])
    app.add_template_filter(formatar_moeda, "moeda")
    app.add_template_filter(formatar_data, "data")
    app.add_template_filter(formatar_percentual, "percentual")

    from .rotas import bp

    app.register_blueprint(bp)

    @app.errorhandler(MetaNaoEncontrada)
    def meta_nao_encontrada(_erro):
        return render_template("404.html"), 404

    return app
