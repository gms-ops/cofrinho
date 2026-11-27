# Cofrinho


- **Sistema em produção:** [https://cofrinho-mzcs.onrender.com](https://cofrinho-mzcs.onrender.com/)

## Feito por Gabriele Maria Silva


## Sobre o sistema

O Cofrinho é uma aplicação web para acompanhar metas de economia (por exemplo, "Viagem" ou "Notebook").

- Criar, editar e remover metas, com nome, valor-alvo e prazo.
- Registrar depósitos e retiradas (sem valores inválidos e sem saldo negativo).
- Ver o progresso em porcentagem, quanto falta e quanto poupar por mês para cumprir o prazo.
- Meta marcada como alcançada ao atingir o valor, e como "prazo vencido" quando atrasada.
- Buscar por nome, filtrar por situação e ordenar por prazo, nome ou progresso.

## Tecnologias

| Uso | Ferramenta |
|---|---|
| Linguagem e servidor web | Python 3.12 + Flask |
| Interface | Templates Jinja2 e CSS próprio |
| Persistência | Arquivo JSON |
| Testes de unidade e integração | pytest |
| Cobertura | pytest-cov (Coverage.py) e Codecov |
| Testes ponta a ponta | Playwright (pytest-playwright) |
| CI/CD | GitHub Actions (Linux, macOS e Windows) |
| Produção | Render (plano gratuito) e gunicorn |

A lógica de negócio fica em `app/dominio/`, como funções puras, o que facilita testar o comportamento pela API pública.



## Execução dos testes

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

pytest                             # unidade e integração
pytest --cov=app --cov-branch --cov-report=term-missing   # com cobertura

python -m playwright install chromium
pytest tests/e2e                   # ponta a ponta
```

Para rodar a aplicação localmente: `flask --app app run`.

## Deploy

O site é publicado no Render a cada push na branch `main`. No plano gratuito o disco é temporário, então os dados podem ser apagados quando o serviço reinicia.
