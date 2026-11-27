from .calculos import calcular_progresso
from .erros import ErroValidacao

STATUS_VALIDOS = ("todas", "andamento", "concluidas")
ORDENS_VALIDAS = ("nome", "prazo", "progresso")


def filtrar_por_status(metas, status):
    if status == "todas":
        return list(metas)
    if status == "andamento":
        return [m for m in metas if not m.concluida]
    if status == "concluidas":
        return [m for m in metas if m.concluida]
    raise ErroValidacao("Situação inválida.")


def buscar_por_nome(metas, termo):
    termo = (termo or "").strip().casefold()
    return [m for m in metas if termo in m.nome.casefold()]


def ordenar_metas(metas, criterio):
    if criterio == "nome":
        return sorted(metas, key=lambda m: m.nome.casefold())
    if criterio == "prazo":
        return sorted(metas, key=lambda m: m.prazo)
    if criterio == "progresso":
        return sorted(metas, key=calcular_progresso, reverse=True)
    raise ErroValidacao("Ordenação inválida.")
