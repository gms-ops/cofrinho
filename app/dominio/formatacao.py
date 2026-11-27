from decimal import ROUND_HALF_UP, Decimal


def formatar_moeda(valor):
    v = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sinal = "-" if v < 0 else ""
    inteiro, centavos = f"{abs(v):.2f}".split(".")
    inteiro = f"{int(inteiro):,}".replace(",", ".")
    return f"{sinal}R$ {inteiro},{centavos}"


def formatar_data(data):
    return data.strftime("%d/%m/%Y")


def formatar_percentual(percentual):
    texto = f"{percentual:.1f}".rstrip("0").rstrip(".")
    return texto.replace(".", ",") + "%"
