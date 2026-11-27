class ErroValidacao(ValueError):
    """Dado informado pelo usuário não respeita uma regra de negócio."""


class SaldoInsuficiente(ErroValidacao):
    """Tentativa de retirar mais do que o saldo da meta."""


class MetaNaoEncontrada(LookupError):
    """Nenhuma meta existe com o identificador informado."""
