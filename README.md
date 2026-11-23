<<<<<<< HEAD
# tentativa1
=======
# sistema-de-musica-streaming
>>>>>>> 56739799117d2228c6c952bc99ad1708c525ace3
import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="streaming_db",
        )
        if conexao.is_connected():
            print("Conectado ao MySQL!")
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        raise


def fechar(conexao, cursor=None):
    try:
        if cursor is not None:
            cursor.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao fechar cursor: {erro}")
    finally:
        try:
            if conexao is not None and conexao.is_connected():
                conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao fechar conexão: {erro}")

import re


PLANOS_VALIDOS = ("Gratuito", "Premium", "Familia", "Universitário")
TIPOS_REGISTRO = ("PLAYLIST", "HISTORICO")


def limpar_cpf(cpf):
    return re.sub(r"\D", "", cpf)


def validar_cpf(cpf):
    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False

    for pos in range(9, 11):
        soma = sum(int(cpf_limpo[i]) * ((pos + 1) - i) for i in range(pos))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf_limpo[pos]):
            return False
    return True


def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(padrao, email.strip()))


def validar_duracao(duracao):
    return isinstance(duracao, int) and not isinstance(duracao, bool) and 0 < duracao <= 10800


def formatar_duracao(segundos):
    minutos = segundos // 60
    resto = segundos % 60
    return f"{minutos:02d}:{resto:02d}"


def validar_plano(plano):
    return plano in PLANOS_VALIDOS


def validar_tipo_registro(tipo):
    return tipo in TIPOS_REGISTRO

def cadastrar_usuario(dados_usuario):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO usuarios (nome, cpf, email, plano) VALUES (%s, %s, %s, %s)"
        valores = (
            dados_usuario["nome"],
            dados_usuario["cpf"],
            dados_usuario["email"],
            dados_usuario["plano"],
        )
        cursor.execute(sql, valores)
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def listar_usuarios():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        sql = "SELECT id, nome, cpf, email, plano FROM usuarios ORDER BY id"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        return usuarios
    except mysql.connector.Error as erro:
        print(f"Erro ao consultar usuários: {erro}")
        return []
    finally:
        fechar(conexao, cursor)


def atualizar_usuario(usuario_id, dados_usuario):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "UPDATE usuarios SET nome = %s, email = %s, plano = %s WHERE id = %s"
        valores = (
            dados_usuario["nome"],
            dados_usuario["email"],
            dados_usuario["plano"],
            usuario_id,
        )
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Usuário atualizado com sucesso!")
            return True
        print("Usuário não encontrado.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar usuário: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def excluir_usuario(usuario_id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        valores = (usuario_id,)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Usuário excluído com sucesso!")
            return True
        print("Usuário não encontrado.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao excluir usuário: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)

def cadastrar_musica(dados_musica):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = (
            "INSERT INTO musicas (titulo, artista, album, duracao, url_mp3) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        valores = (
            dados_musica["titulo"],
            dados_musica["artista"],
            dados_musica["album"],
            dados_musica["duracao"],
            dados_musica["url_mp3"],
        )
        cursor.execute(sql, valores)
        conexao.commit()
        print("Música cadastrada com sucesso!")
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar música: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def listar_musicas():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        sql = "SELECT id, titulo, artista, album, duracao, url_mp3 FROM musicas ORDER BY id"
        cursor.execute(sql)
        musicas = cursor.fetchall()
        return musicas
    except mysql.connector.Error as erro:
        print(f"Erro ao consultar músicas: {erro}")
        return []
    finally:
        fechar(conexao, cursor)


def atualizar_musica(musica_id, dados_musica):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = (
            "UPDATE musicas SET titulo = %s, artista = %s, album = %s, "
            "duracao = %s, url_mp3 = %s WHERE id = %s"
        )
        valores = (
            dados_musica["titulo"],
            dados_musica["artista"],
            dados_musica["album"],
            dados_musica["duracao"],
            dados_musica["url_mp3"],
            musica_id,
        )
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Música atualizada com sucesso!")
            return True
        print("Música não encontrada.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar música: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def excluir_musica(musica_id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM musicas WHERE id = %s"
        valores = (musica_id,)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Música excluída com sucesso!")
            return True
        print("Música não encontrada.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao excluir música: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)

def adicionar_playlist_historico(dados_item):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = (
            "INSERT INTO playlists_historico "
            "(usuario_id, musica_id, nome_playlist, tipo_registro) "
            "VALUES (%s, %s, %s, %s)"
        )
        valores = (
            dados_item["usuario_id"],
            dados_item["musica_id"],
            dados_item["nome_playlist"],
            dados_item["tipo_registro"],
        )
        cursor.execute(sql, valores)
        conexao.commit()
        print("Registro adicionado em Playlists/Histórico com sucesso!")
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao adicionar em Playlists/Histórico: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def listar_por_usuario(usuario_id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT
                ph.id,
                ph.usuario_id,
                u.nome AS nome_usuario,
                u.plano AS plano_usuario,
                ph.nome_playlist,
                ph.tipo_registro,
                m.titulo,
                m.artista,
                m.album,
                m.duracao,
                ph.adicionado_em
            FROM playlists_historico ph
            INNER JOIN usuarios u ON ph.usuario_id = u.id
            INNER JOIN musicas m ON ph.musica_id = m.id
            WHERE ph.usuario_id = %s
            ORDER BY ph.id DESC
        """
        valores = (usuario_id,)
        cursor.execute(sql, valores)
        registros = cursor.fetchall()
        return registros
    except mysql.connector.Error as erro:
        print(f"Erro ao consultar Playlists/Histórico: {erro}")
        return []
    finally:
        fechar(conexao, cursor)


def atualizar_playlist_historico(registro_id, dados_item):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = (
            "UPDATE playlists_historico "
            "SET nome_playlist = %s, tipo_registro = %s WHERE id = %s"
        )
        valores = (
            dados_item["nome_playlist"],
            dados_item["tipo_registro"],
            registro_id,
        )
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Registro de Playlist/Histórico atualizado!")
            return True
        print("Registro não encontrado.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar Playlist/Histórico: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)


def excluir_playlist_historico(registro_id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM playlists_historico WHERE id = %s"
        valores = (registro_id,)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("Registro removido de Playlists/Histórico!")
            return True
        print("Registro não encontrado.")
        return False
    except mysql.connector.Error as erro:
        print(f"Erro ao excluir de Playlists/Histórico: {erro}")
        if conexao and conexao.is_connected():
            conexao.rollback()
        return False
    finally:
        fechar(conexao, cursor)

def ler_inteiro(mensagem):
    try:
        return int(input(mensagem).strip())
    except ValueError:
        print("Digite um número inteiro válido.")
        return None


def escolher_plano():
    print("Planos:", ", ".join(PLANOS_VALIDOS))
    plano = input("Digite o plano: ").strip()
    if not validar_plano(plano):
        print("Plano inválido! Escolha entre: Gratuito, Premium, Familia ou Universitário.")
        return None
    return plano


def escolher_tipo():
    print("Tipos:", ", ".join(TIPOS_REGISTRO))
    tipo = input("Digite o tipo (PLAYLIST ou HISTORICO): ").strip().upper()
    if not validar_tipo_registro(tipo):
        print("Tipo inválido! Use PLAYLIST ou HISTORICO.")
        return None
    return tipo


def menu_usuarios():
    while True:
        print("\n--- USUÁRIOS ---")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Excluir usuário")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Digite o nome do usuário: ").strip()
            cpf = input("Digite o CPF do usuário: ").strip()
            email = input("Digite o e-mail do usuário: ").strip()
            plano = escolher_plano()

            if not nome:
                print("Nome obrigatório.")
                continue
            if not validar_cpf(cpf):
                print("CPF inválido.")
                continue
            if not validar_email(email):
                print("E-mail inválido.")
                continue
            if not plano:
                continue

            dados = {
                "nome": nome,
                "cpf": limpar_cpf(cpf),
                "email": email,
                "plano": plano,
            }
            cadastrar_usuario(dados)

        elif opcao == "2":
            usuarios = listar_usuarios()
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            for u in usuarios:
                print(
                    f"ID: {u['id']} | Nome: {u['nome']} | CPF: {u['cpf']} | "
                    f"E-mail: {u['email']} | Plano: {u['plano']}"
                )

        elif opcao == "3":
            usuario_id = ler_inteiro("Digite o ID do usuário a atualizar: ")
            if usuario_id is None:
                continue
            nome = input("Digite o novo nome: ").strip()
            email = input("Digite o novo e-mail: ").strip()
            plano = escolher_plano()
            if nome and validar_email(email) and plano:
                atualizar_usuario(usuario_id, {"nome": nome, "email": email, "plano": plano})
            else:
                print("Dados inválidos para atualização.")

        elif opcao == "4":
            usuario_id = ler_inteiro("Digite o ID do usuário a excluir: ")
            if usuario_id is not None:
                excluir_usuario(usuario_id)

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_musicas():
    while True:
        print("\n--- MÚSICAS ---")
        print("1 - Cadastrar música")
        print("2 - Listar músicas")
        print("3 - Atualizar música")
        print("4 - Excluir música")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Digite o título da música: ").strip()
            artista = input("Digite o artista: ").strip()
            album = input("Digite o álbum: ").strip() or "Single"
            duracao = ler_inteiro("Digite a duração em segundos: ")
            url_mp3 = input("Digite o endereço do arquivo MP3: ").strip()

            if not titulo or not artista or not url_mp3:
                print("Título, artista e URL do MP3 são obrigatórios.")
                continue
            if duracao is None or not validar_duracao(duracao):
                print("Duração inválida! Informe um número inteiro entre 1 e 10800 segundos.")
                continue

            dados = {
                "titulo": titulo,
                "artista": artista,
                "album": album,
                "duracao": duracao,
                "url_mp3": url_mp3,
            }
            cadastrar_musica(dados)

        elif opcao == "2":
            musicas = listar_musicas()
            if not musicas:
                print("Nenhuma música cadastrada.")
            for m in musicas:
                print(
                    f"ID: {m['id']} | Título: {m['titulo']} | Artista: {m['artista']} | "
                    f"Álbum: {m['album']} | Duração: {formatar_duracao(m['duracao'])} | "
                    f"MP3: {m['url_mp3']}"
                )

        elif opcao == "3":
            musica_id = ler_inteiro("Digite o ID da música a atualizar: ")
            if musica_id is None:
                continue
            titulo = input("Digite o novo título: ").strip()
            artista = input("Digite o novo artista: ").strip()
            album = input("Digite o novo álbum: ").strip() or "Single"
            duracao = ler_inteiro("Digite a nova duração em segundos: ")
            url_mp3 = input("Digite o novo endereço do MP3: ").strip()

            if titulo and artista and url_mp3 and duracao is not None and validar_duracao(duracao):
                atualizar_musica(
                    musica_id,
                    {
                        "titulo": titulo,
                        "artista": artista,
                        "album": album,
                        "duracao": duracao,
                        "url_mp3": url_mp3,
                    },
                )
            else:
                print("Dados inválidos para atualização.")

        elif opcao == "4":
            musica_id = ler_inteiro("Digite o ID da música a excluir: ")
            if musica_id is not None:
                excluir_musica(musica_id)

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_playlists_historico():
    while True:
        print("\n--- PLAYLISTS / HISTÓRICO ---")
        print("1 - Adicionar música à playlist ou histórico")
        print("2 - Consultar playlists e histórico de um usuário")
        print("3 - Atualizar registro")
        print("4 - Excluir registro")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuario_id = ler_inteiro("Digite o ID do usuário: ")
            musica_id = ler_inteiro("Digite o ID da música: ")
            tipo = escolher_tipo()
            nome_playlist = input("Digite o nome da playlist (ou do histórico): ").strip()
            if not nome_playlist:
                nome_playlist = "Histórico de Reprodução" if tipo == "HISTORICO" else "Minha Playlist"

            if usuario_id is not None and musica_id is not None and tipo:
                adicionar_playlist_historico(
                    {
                        "usuario_id": usuario_id,
                        "musica_id": musica_id,
                        "nome_playlist": nome_playlist,
                        "tipo_registro": tipo,
                    }
                )

        elif opcao == "2":
            usuario_id = ler_inteiro("Digite o ID do usuário: ")
            if usuario_id is not None:
                registros = listar_por_usuario(usuario_id)
                if not registros:
                    print("Nenhum registro encontrado para esse usuário.")
                for r in registros:
                    print(
                        f"ID Reg: {r['id']} | Usuário: {r['nome_usuario']} ({r['plano_usuario']}) | "
                        f"[{r['tipo_registro']}] {r['nome_playlist']} -> "
                        f"{r['titulo']} - {r['artista']} ({formatar_duracao(r['duracao'])})"
                    )

        elif opcao == "3":
            registro_id = ler_inteiro("Digite o ID do registro: ")
            novo_nome = input("Digite o novo nome da playlist/histórico: ").strip()
            novo_tipo = escolher_tipo()
            if registro_id is not None and novo_nome and novo_tipo:
                atualizar_playlist_historico(
                    registro_id,
                    {"nome_playlist": novo_nome, "tipo_registro": novo_tipo},
                )
            else:
                print("Dados inválidos.")

        elif opcao == "4":
            registro_id = ler_inteiro("Digite o ID do registro a excluir: ")
            if registro_id is not None:
                excluir_playlist_historico(registro_id)

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def main():
    while True:
        print("\n=== SISTEMA DE MÚSICA STREAMING ===")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Músicas")
        print("3 - Gerenciar Playlists / Histórico")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_musicas()
        elif opcao == "3":
            menu_playlists_historico()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
<<<<<<< HEAD
=======
<head>
  <meta charset="UTF-8" />
  <title>Sistema de Música Streaming</title>
</head>
>>>>>>> 56739799117d2228c6c952bc99ad1708c525ace3
