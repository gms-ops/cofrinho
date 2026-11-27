from datetime import date, timedelta

from playwright.sync_api import Page, expect

PRAZO = (date.today() + timedelta(days=365)).isoformat()


def criar_meta(page: Page, nome: str, alvo: str, prazo: str = PRAZO):
    page.get_by_label("Nome da meta").fill(nome)
    page.get_by_label("Valor-alvo (R$)").fill(alvo)
    page.get_by_label("Prazo").fill(prazo)
    page.get_by_role("button", name="Criar meta").click()


def cartao(page: Page, nome: str):
    return page.get_by_role("article", name=f"Meta {nome}")


def test_usuario_cria_uma_meta_e_a_ve_na_lista(page: Page, url_base):
    page.goto(url_base)
    criar_meta(page, "Viagem", "1000")

    expect(page.get_by_role("status")).to_contain_text("Meta criada")
    expect(cartao(page, "Viagem")).to_contain_text("R$ 0,00 de R$ 1.000,00")


def test_usuario_deposita_e_ve_o_progresso_atualizado(page: Page, url_base):
    page.goto(url_base)
    criar_meta(page, "Viagem", "1000")

    meta = cartao(page, "Viagem")
    meta.get_by_label("Valor para depositar").fill("500")
    meta.get_by_role("button", name="Depositar").click()

    expect(meta.get_by_role("progressbar")).to_have_attribute("aria-valuenow", "50")
    expect(meta).to_contain_text("R$ 500,00 de R$ 1.000,00")


def test_usuario_ve_mensagem_de_erro_ao_criar_meta_sem_nome(page: Page, url_base):
    page.goto(url_base)
    criar_meta(page, "", "1000")

    expect(page.get_by_role("alert")).to_contain_text("Informe o nome da meta")
    expect(page.get_by_text("Nenhuma meta por aqui")).to_be_visible()


def test_meta_e_marcada_como_alcancada_ao_atingir_o_valor(page: Page, url_base):
    page.goto(url_base)
    criar_meta(page, "Fone", "200")

    meta = cartao(page, "Fone")
    meta.get_by_label("Valor para depositar").fill("200")
    meta.get_by_role("button", name="Depositar").click()

    expect(meta.get_by_text("Meta alcançada")).to_be_visible()
    expect(page.get_by_role("status")).to_contain_text("Parabéns")


def test_meta_removida_some_e_os_dados_persistem_ao_recarregar(page: Page, url_base):
    page.goto(url_base)
    criar_meta(page, "Viagem", "1000")
    criar_meta(page, "Notebook", "4000")

    page.reload()
    expect(cartao(page, "Viagem")).to_be_visible()
    expect(cartao(page, "Notebook")).to_be_visible()

    cartao(page, "Viagem").get_by_role("button", name="Remover").click()
    page.reload()

    expect(cartao(page, "Viagem")).to_have_count(0)
    expect(cartao(page, "Notebook")).to_be_visible()
