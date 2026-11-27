from datetime import date, timedelta

from playwright.sync_api import Page, expect

PRAZO = (date.today() + timedelta(days=365)).isoformat()


def test_usuario_edita_o_nome_de_uma_meta(page: Page, url_base):
    page.goto(url_base)
    page.get_by_label("Nome da meta").fill("Viagem")
    page.get_by_label("Valor-alvo (R$)").fill("1000")
    page.get_by_label("Prazo").fill(PRAZO)
    page.get_by_role("button", name="Criar meta").click()

    page.get_by_role("article", name="Meta Viagem").get_by_role("link", name="Editar").click()
    page.get_by_label("Nome da meta").fill("Viagem ao Japão")
    page.get_by_role("button", name="Salvar alterações").click()

    expect(page.get_by_role("status")).to_contain_text("Meta atualizada")
    expect(page.get_by_role("article", name="Meta Viagem ao Japão")).to_be_visible()
    expect(page.get_by_role("article", name="Meta Viagem", exact=True)).to_have_count(0)
