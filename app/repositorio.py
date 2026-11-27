import json
import threading
from dataclasses import replace
from datetime import date
from decimal import Decimal
from pathlib import Path

from .dominio.erros import MetaNaoEncontrada
from .dominio.meta import Meta


class RepositorioMetas:
    """Guarda metas em memória e, se houver caminho, em um arquivo JSON."""

    def __init__(self, caminho=None):
        self._caminho = Path(caminho) if caminho else None
        self._metas = {}
        self._proximo_id = 1
        self._trava = threading.Lock()
        if self._caminho and self._caminho.exists():
            self._carregar()

    def adicionar(self, meta):
        with self._trava:
            nova = replace(meta, id=self._proximo_id)
            self._metas[nova.id] = nova
            self._proximo_id += 1
            self._salvar()
            return nova

    def obter(self, meta_id):
        try:
            return self._metas[meta_id]
        except KeyError:
            raise MetaNaoEncontrada(f"Meta {meta_id} não encontrada.")

    def listar(self):
        return [self._metas[i] for i in sorted(self._metas)]

    def atualizar(self, meta):
        with self._trava:
            self.obter(meta.id)
            self._metas[meta.id] = meta
            self._salvar()
            return meta

    def remover(self, meta_id):
        with self._trava:
            self.obter(meta_id)
            del self._metas[meta_id]
            self._salvar()

    def _salvar(self):
        if not self._caminho:
            return
        dados = {
            "proximo_id": self._proximo_id,
            "metas": [
                {
                    "id": m.id,
                    "nome": m.nome,
                    "alvo": str(m.alvo),
                    "prazo": m.prazo.isoformat(),
                    "saldo": str(m.saldo),
                }
                for m in self.listar()
            ],
        }
        self._caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    def _carregar(self):
        dados = json.loads(self._caminho.read_text(encoding="utf-8"))
        self._proximo_id = dados["proximo_id"]
        for item in dados["metas"]:
            self._metas[item["id"]] = Meta(
                id=item["id"],
                nome=item["nome"],
                alvo=Decimal(item["alvo"]),
                prazo=date.fromisoformat(item["prazo"]),
                saldo=Decimal(item["saldo"]),
            )
