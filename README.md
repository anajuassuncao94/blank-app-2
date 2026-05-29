# OrganizaAí Estudos

Aplicação web em **Python + Streamlit** para planejamento automático de estudos de universitários.

O sistema permite:

- Cadastro de usuário com login e senha;
- Cadastro de disciplinas;
- Cadastro de horários livres da rotina;
- Cadastro de atividades acadêmicas, como provas, trabalhos e listas;
- Geração automática de cronograma semanal;
- Recalcular cronograma;
- Exportar cronograma em PDF;
- Armazenamento dos dados em PostgreSQL externo no Render.

## Estrutura do projeto

```text
organizaai_streamlit/
├── app.py
├── requirements.txt
├── database/
├── repositories/
├── services/
├── utils/
├── pages/
└── .streamlit/secrets.toml.example
```

## Como rodar localmente sem criar ambiente virtual

1. Abra o terminal na pasta do projeto.

2. Instale as dependências diretamente:

```bash
pip install -r requirements.txt
```

Caso o comando `pip` não funcione, tente:

```bash
python -m pip install -r requirements.txt
```

3. Crie o arquivo de segredos do Streamlit.

No Windows:

```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

No Linux/Mac:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. Edite o arquivo `.streamlit/secrets.toml` e coloque a URL externa do PostgreSQL do Render:

```toml
DATABASE_URL = "postgresql://usuario:senha@host/banco?sslmode=require"
```

5. Rode o projeto:

```bash
streamlit run app.py
```

Caso o comando `streamlit` não funcione, tente:

```bash
python -m streamlit run app.py
```

## Como publicar no Streamlit Cloud

1. Suba este projeto para o GitHub.
2. Não suba o arquivo `.streamlit/secrets.toml`.
3. No Streamlit Cloud, vá em **App settings > Secrets**.
4. Cadastre:

```toml
DATABASE_URL = "sua_url_externa_do_postgresql_render"
```

5. Publique usando `streamlit_app.py` como arquivo principal.

## Observação de segurança

A senha do banco de dados e a URL real do Render devem ficar apenas no **Streamlit Secrets** ou em variável de ambiente. Não coloque a URL real diretamente no código nem no GitHub.
