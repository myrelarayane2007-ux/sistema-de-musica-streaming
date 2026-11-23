import os
import re
import sys

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

PLANOS_VALIDOS = ("Gratuito", "Premium", "Familia", "Universitário")
TIPOS_REGISTRO = ("PLAYLIST", "HISTORICO")


def configurar_terminal_utf8():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass


def conectar():
    senha = os.getenv("MYSQL_PASSWORD")
    if not senha:
        raise RuntimeError(
            "MYSQL_PASSWORD não foi configurada. Copie .env.example para .env "
            "e informe a senha do MySQL, ou configure essa variável no terminal."
        )

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=senha,
        database=os.getenv("MYSQL_DATABASE", "streaming_db"),
        charset="utf8mb4",
        use_unicode=True,
        connection_timeout=10,
    )


def fechar(conexao, cursor=None):
    if cursor is not None:
        try:
            cursor.close()
        except mysql.connector.Error:
            pass
    if conexao is not None:
        try:
            conexao.close()
        except mysql.connector.Error:
            pass


def executar(sql, valores=(), *, consulta=False, dictionary=False):
    """Executa SQL parametrizado. Retorna linhas, rowcount ou None em erro."""
    conexao = cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=dictionary)
        cursor.execute(sql, valores)
        if consulta:
            return cursor.fetchall()
        conexao.commit()
        return cursor.rowcount
    except (RuntimeError, mysql.connector.Error, ValueError) as erro:
        if conexao is not None:
            try:
                conexao.rollback()
            except mysql.connector.Error:
                pass
        print(f"Erro no banco de dados: {erro}")
        return None
    finally:
        fechar(conexao, cursor)


def limpar_cpf(cpf):
    return re.sub(r"\D", "", cpf)


def validar_cpf(cpf):
    cpf = limpar_cpf(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for pos in range(9, 11):
        soma = sum(int(cpf[i]) * (pos + 1 - i) for i in range(pos))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[pos]):
            return False
    return True


def validar_email(email):
    return bool(re.fullmatch(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", email.strip()))


def validar_duracao(duracao):
    return duracao is None or (
        isinstance(duracao, int) and not isinstance(duracao, bool) and 0 < duracao <= 10800
    )


def formatar_duracao(segundos):
    if segundos is None:
        return "não informada"
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def validar_plano(plano):
    return plano in PLANOS_VALIDOS


def validar_tipo_registro(tipo):
    return tipo in TIPOS_REGISTRO


# Usuários

def cadastrar_usuario(dados):
    resultado = executar(
        "INSERT INTO usuarios (nome, cpf, email, plano) VALUES (%s, %s, %s, %s)",
        (dados["nome"], limpar_cpf(dados["cpf"]), dados["email"], dados["plano"]),
    )
    if resultado is not None:
        print("Usuário cadastrado com sucesso!")
        return True
    return False


def listar_usuarios():
    return executar(
        "SELECT id, nome, cpf, email, plano FROM usuarios ORDER BY id",
        consulta=True,
        dictionary=True,
    )


def atualizar_usuario(usuario_id, dados):
    resultado = executar(
        "UPDATE usuarios SET nome=%s, email=%s, plano=%s WHERE id=%s",
        (dados["nome"], dados["email"], dados["plano"], usuario_id),
    )
    if resultado is None:
        return False
    print("Usuário atualizado!" if resultado else "Usuário não encontrado ou sem alterações.")
    return resultado > 0


def excluir_usuario(usuario_id):
    resultado = executar("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
    if resultado is None:
        return False
    print("Usuário excluído!" if resultado else "Usuário não encontrado.")
    return resultado > 0


# Músicas. Duração e URL podem ficar vazias até serem obtidos dados/licenças válidos.

def cadastrar_musica(dados):
    resultado = executar(
        "INSERT INTO musicas (titulo, artista, album, duracao, url_mp3) VALUES (%s,%s,%s,%s,%s)",
        (dados["titulo"], dados["artista"], dados["album"], dados["duracao"], dados["url_mp3"]),
    )
    if resultado is not None:
        print("Música cadastrada com sucesso!")
        return True
    return False


def listar_musicas():
    return executar(
        "SELECT id, titulo, artista, album, duracao, url_mp3 FROM musicas ORDER BY id",
        consulta=True,
        dictionary=True,
    )


def atualizar_musica(musica_id, dados):
    resultado = executar(
        "UPDATE musicas SET titulo=%s, artista=%s, album=%s, duracao=%s, url_mp3=%s WHERE id=%s",
        (dados["titulo"], dados["artista"], dados["album"], dados["duracao"], dados["url_mp3"], musica_id),
    )
    if resultado is None:
        return False
    print("Música atualizada!" if resultado else "Música não encontrada ou sem alterações.")
    return resultado > 0


def excluir_musica(musica_id):
    resultado = executar("DELETE FROM musicas WHERE id=%s", (musica_id,))
    if resultado is None:
        return False
    print("Música excluída!" if resultado else "Música não encontrada.")
    return resultado > 0


# Playlists e histórico

def adicionar_playlist_historico(dados):
    resultado = executar(
        "INSERT INTO playlists_historico (usuario_id,musica_id,nome_playlist,tipo_registro) "
        "VALUES (%s,%s,%s,%s)",
        (dados["usuario_id"], dados["musica_id"], dados["nome_playlist"], dados["tipo_registro"]),
    )
    if resultado is not None:
        print("Registro adicionado com sucesso!")
        return True
    return False


def listar_por_usuario(usuario_id):
    sql = """
        SELECT ph.id, ph.usuario_id, u.nome AS nome_usuario, u.plano AS plano_usuario,
               ph.nome_playlist, ph.tipo_registro, m.titulo, m.artista, m.album,
               m.duracao, m.url_mp3, ph.adicionado_em
        FROM playlists_historico ph
        JOIN usuarios u ON ph.usuario_id = u.id
        JOIN musicas m ON ph.musica_id = m.id
        WHERE ph.usuario_id = %s
        ORDER BY ph.id DESC
    """
    return executar(sql, (usuario_id,), consulta=True, dictionary=True)


def atualizar_playlist_historico(registro_id, dados):
    resultado = executar(
        "UPDATE playlists_historico SET nome_playlist=%s, tipo_registro=%s WHERE id=%s",
        (dados["nome_playlist"], dados["tipo_registro"], registro_id),
    )
    if resultado is None:
        return False
    print("Registro atualizado!" if resultado else "Registro não encontrado ou sem alterações.")
    return resultado > 0


def excluir_playlist_historico(registro_id):
    resultado = executar("DELETE FROM playlists_historico WHERE id=%s", (registro_id,))
    if resultado is None:
        return False
    print("Registro excluído!" if resultado else "Registro não encontrado.")
    return resultado > 0


def ler_inteiro(mensagem, *, opcional=False):
    texto = input(mensagem).strip()
    if opcional and not texto:
        return None
    try:
        return int(texto)
    except ValueError:
        print("Digite um número inteiro válido.")
        return None


def escolher_plano():
    print("Planos: " + ", ".join(PLANOS_VALIDOS))
    plano = input("Plano: ").strip()
    if not validar_plano(plano):
        print("Plano inválido.")
        return None
    return plano


def escolher_tipo():
    tipo = input("Tipo (PLAYLIST/HISTORICO): ").strip().upper()
    if not validar_tipo_registro(tipo):
        print("Tipo inválido.")
        return None
    return tipo


def exibir_usuarios():
    usuarios = listar_usuarios()
    if usuarios is None:
        print("Não foi possível listar usuários. Confira MySQL e as variáveis do arquivo .env.")
    elif not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for u in usuarios:
            print(f"ID {u['id']} | {u['nome']} | CPF {u['cpf']} | {u['email']} | {u['plano']}")


def menu_usuarios():
    while True:
        print("\n--- USUÁRIOS ---\n1 Cadastrar\n2 Listar\n3 Atualizar\n4 Excluir\n0 Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            nome = input("Nome: ").strip()
            cpf = input("CPF: ").strip()
            email = input("E-mail: ").strip()
            plano = escolher_plano()
            if not nome or not validar_cpf(cpf) or not validar_email(email) or not plano:
                print("Dados inválidos; confira nome, CPF, e-mail e plano.")
                continue
            cadastrar_usuario({"nome": nome, "cpf": cpf, "email": email, "plano": plano})
        elif opcao == "2":
            exibir_usuarios()
        elif opcao == "3":
            uid = ler_inteiro("ID: ")
            nome = input("Novo nome: ").strip()
            email = input("Novo e-mail: ").strip()
            plano = escolher_plano()
            if uid is not None and nome and validar_email(email) and plano:
                atualizar_usuario(uid, {"nome": nome, "email": email, "plano": plano})
            else:
                print("Dados inválidos.")
        elif opcao == "4":
            uid = ler_inteiro("ID para excluir: ")
            if uid is not None:
                excluir_usuario(uid)
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def imprimir_musicas(musicas):
    if musicas is None:
        print("Não foi possível consultar músicas. Confira conexão e configuração do MySQL.")
    elif not musicas:
        print("Nenhuma música cadastrada.")
    else:
        for m in musicas:
            print(
                f"ID {m['id']} | {m['titulo']} — {m['artista']} | Álbum: {m['album']} | "
                f"Duração: {formatar_duracao(m['duracao'])} | URL: {m['url_mp3'] or 'não informada'}"
            )


def coletar_musica():
    titulo = input("Título: ").strip()
    artista = input("Artista: ").strip()
    album = input("Álbum (Enter = Single): ").strip() or "Single"
    duracao = ler_inteiro("Duração em segundos (Enter se desconhecida): ", opcional=True)
    url = input("URL legal do áudio (Enter se ainda não tiver): ").strip() or None
    if duracao is not None and not validar_duracao(duracao):
        print("Duração deve ser de 1 a 10800 segundos.")
        return None
    if not titulo or not artista:
        print("Título e artista são obrigatórios.")
        return None
    return {"titulo": titulo, "artista": artista, "album": album, "duracao": duracao, "url_mp3": url}


def menu_musicas():
    while True:
        print("\n--- MÚSICAS ---\n1 Cadastrar\n2 Listar\n3 Atualizar\n4 Excluir\n0 Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            dados = coletar_musica()
            if dados:
                cadastrar_musica(dados)
        elif opcao == "2":
            imprimir_musicas(listar_musicas())
        elif opcao == "3":
            mid = ler_inteiro("ID para atualizar: ")
            if mid is not None:
                dados = coletar_musica()
                if dados:
                    atualizar_musica(mid, dados)
        elif opcao == "4":
            mid = ler_inteiro("ID para excluir: ")
            if mid is not None:
                excluir_musica(mid)
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_playlists_historico():
    while True:
        print("\n--- PLAYLISTS / HISTÓRICO ---\n1 Adicionar\n2 Consultar por usuário\n3 Atualizar\n4 Excluir\n0 Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            uid = ler_inteiro("ID do usuário: ")
            mid = ler_inteiro("ID da música: ")
            tipo = escolher_tipo()
            nome = input("Nome da playlist/histórico (Enter = padrão): ").strip()
            if tipo and uid is not None and mid is not None:
                nome = nome or ("Histórico de Reprodução" if tipo == "HISTORICO" else "Minha Playlist")
                adicionar_playlist_historico({"usuario_id": uid, "musica_id": mid, "nome_playlist": nome, "tipo_registro": tipo})
        elif opcao == "2":
            uid = ler_inteiro("ID do usuário: ")
            if uid is None:
                continue
            registros = listar_por_usuario(uid)
            if registros is None:
                print("Não foi possível consultar; verifique conexão e IDs.")
            elif not registros:
                print("Nenhum registro para esse usuário.")
            else:
                for r in registros:
                    print(
                        f"Registro {r['id']} | [{r['tipo_registro']}] {r['nome_playlist']} | "
                        f"{r['titulo']} — {r['artista']} | {formatar_duracao(r['duracao'])}"
                    )
        elif opcao == "3":
            rid = ler_inteiro("ID do registro: ")
            nome = input("Novo nome: ").strip()
            tipo = escolher_tipo()
            if rid is not None and nome and tipo:
                atualizar_playlist_historico(rid, {"nome_playlist": nome, "tipo_registro": tipo})
            else:
                print("Dados inválidos.")
        elif opcao == "4":
            rid = ler_inteiro("ID para excluir: ")
            if rid is not None:
                excluir_playlist_historico(rid)
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def main():
    while True:
        print("\n=== SISTEMA DE MÚSICA STREAMING ===\n1 Usuários\n2 Músicas\n3 Playlists/Histórico\n0 Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_musicas()
        elif opcao == "3":
            menu_playlists_historico()
        elif opcao == "0":
            print("Saindo...")
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    configurar_terminal_utf8()
    main()
