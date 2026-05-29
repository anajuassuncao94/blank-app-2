import hashlib
import hmac
import os

from psycopg2.errors import UniqueViolation

from repositories.usuarios import buscar_por_usuario, criar_usuario


def gerar_hash_senha(senha: str) -> str:
    """Gera hash seguro para senha usando PBKDF2."""
    salt = os.urandom(16)
    iteracoes = 150_000
    senha_hash = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        iteracoes,
    )
    return f"pbkdf2_sha256${iteracoes}${salt.hex()}${senha_hash.hex()}"


def verificar_senha(senha: str, senha_hash_armazenada: str) -> bool:
    """Verifica se a senha digitada corresponde ao hash armazenado."""
    try:
        algoritmo, iteracoes, salt_hex, hash_hex = senha_hash_armazenada.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False

        novo_hash = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iteracoes),
        ).hex()

        return hmac.compare_digest(novo_hash, hash_hex)
    except Exception:
        return False


def cadastrar_usuario(nome: str, usuario: str, senha: str) -> tuple[bool, str]:
    if not nome.strip():
        return False, "Informe o nome."
    if not usuario.strip():
        return False, "Informe o usuário."
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."

    try:
        criar_usuario(nome, usuario, gerar_hash_senha(senha))
        return True, "Usuário cadastrado com sucesso."
    except UniqueViolation:
        return False, "Este usuário já existe. Escolha outro nome de usuário."
    except Exception as exc:
        return False, f"Erro ao cadastrar usuário: {exc}"


def autenticar(usuario: str, senha: str) -> tuple[bool, dict | None, str]:
    usuario_db = buscar_por_usuario(usuario)

    if not usuario_db:
        return False, None, "Usuário não encontrado."

    if not verificar_senha(senha, usuario_db["senha_hash"]):
        return False, None, "Senha incorreta."

    usuario_logado = {
        "id": usuario_db["id"],
        "nome": usuario_db["nome"],
        "usuario": usuario_db["usuario"],
    }

    return True, usuario_logado, "Login realizado com sucesso."
