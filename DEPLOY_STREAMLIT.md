Passos para publicar no Streamlit Cloud

1. Confirme que o repositório está no GitHub e atualizado (branch `main`).

2. No Streamlit Cloud (https://share.streamlit.io/) faça Login.

3. Clique em "New app" → escolha o repositório `anajuassuncao94/blank-app-2` → branch `main`.

4. Em "Main file" informe `streamlit_app.py`.

5. Em "Advanced settings" → "Secrets" adicione uma entrada `DATABASE_URL` com a sua string de conexão PostgreSQL (ex: `postgresql://user:pass@host:5432/dbname`).

6. Deploy: clique em "Deploy". Após o deploy, nas configurações do app (Settings) ajuste o subdomínio para `organizaai` caso esteja disponível.

7. Teste o app em https://organizaai.streamlit.app/ quando o subdomínio for liberado.

Observações:
- Não coloque `.streamlit/secrets.toml` no repositório — use a seção "Secrets" do Streamlit Cloud.
- `requirements.txt` já existe e será usado pelo Streamlit Cloud para instalar dependências.

Problemas comuns:
- Se houver erro de conexão com o banco, confirme o valor de `DATABASE_URL` e se o host permite conexões externas.
- Se precisar de um domínio custom, verifique planos e configurações no painel do Streamlit.

Se quiser, eu posso também criar um release GitHub e um workflow de CI simples (já incluido no repo).
