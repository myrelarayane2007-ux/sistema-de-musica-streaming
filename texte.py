import os
from flask import Flask, jsonify, render_template, request, send_from_directory
from database import (
    adicionar_playlist_historico,
    configurar_terminal_utf8,
    listar_musicas,
    listar_por_usuario,
    listar_usuarios,
)

app = Flask(__name__)

# Pasta opcional caso você queira guardar arquivos .mp3 locais em "audios/nome.mp3"
PASTA_AUDIOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
os.makedirs(PASTA_AUDIOS, exist_ok=True)


def resolver_url_audio(url_mp3: str) -> str:
    """
    Se url_mp3 já for um link HTTP/HTTPS, retorna direto.
    Se for um caminho relativo local (ex.: 'audios/amanha.mp3' ou 'amanha.mp3'),
    aponta para a rota /audio/<arquivo> do Flask.
    """
    if not url_mp3:
        return ""
    url_limpa = url_mp3.strip()
    if url_limpa.startswith(("http://", "https://")):
        return url_limpa
    nome_arquivo = os.path.basename(url_limpa)
    return f"/audio/{nome_arquivo}"


@app.route("/audio/<path:nome_arquivo>")
def servir_audio(nome_arquivo):
    # send_from_directory já lida com streaming parcial (Range requests) no navegador
    return send_from_directory(PASTA_AUDIOS, nome_arquivo, as_attachment=False)


@app.route("/")
def index():
    usuarios = listar_usuarios()
    musicas = listar_musicas()

    for m in musicas:
        m["src_audio"] = resolver_url_audio(m["url_mp3"])

    usuario_ativo_id = request.args.get("usuario_id", type=int)
    if usuario_ativo_id is None and usuarios:
        usuario_ativo_id = usuarios[0]["id"]

    registros_usuario = []
    if usuario_ativo_id is not None:
        registros_usuario = listar_por_usuario(usuario_ativo_id)
        for r in registros_usuario:
            # Busca a url_mp3 correspondente para tocar direto do histórico/playlist
            musica_match = next(
                (m for m in musicas if m["titulo"] == r["titulo"] and m["artista"] == r["artista"]),
                None,
            )
            r["src_audio"] = musica_match["src_audio"] if musica_match else ""

    return render_template(
        "index.html",
        usuarios=usuarios,
        usuario_ativo_id=usuario_ativo_id,
        musicas=musicas,
        registros=registros_usuario,
    )


@app.route("/api/reproduzir", methods=["POST"])
def registrar_reproducao():
    dados = request.get_json(silent=True) or {}
    usuario_id = dados.get("usuario_id")
    musica_id = dados.get("musica_id")

    if not usuario_id or not musica_id:
        return jsonify({"ok": False, "erro": "usuario_id e musica_id são obrigatórios."}), 400

    sucesso = adicionar_playlist_historico(
        {
            "usuario_id": int(usuario_id),
            "musica_id": int(musica_id),
            "nome_playlist": "Histórico de Reprodução",
            "tipo_registro": "HISTORICO",
        }
    )
    return jsonify({"ok": sucesso})


@app.route("/api/playlist", methods=["POST"])
def adicionar_a_playlist():
    dados = request.get_json(silent=True) or {}
    usuario_id = dados.get("usuario_id")
    musica_id = dados.get("musica_id")
    nome_playlist = (dados.get("nome_playlist") or "Minha Playlist").strip()

    if not usuario_id or not musica_id:
        return jsonify({"ok": False, "erro": "usuario_id e musica_id são obrigatórios."}), 400

    sucesso = adicionar_playlist_historico(
        {
            "usuario_id": int(usuario_id),
            "musica_id": int(musica_id),
            "nome_playlist": nome_playlist,
            "tipo_registro": "PLAYLIST",
        }
    )
    return jsonify({"ok": sucesso})


if __name__ == "__main__":
    configurar_terminal_utf8()
    app.run(debug=True, port=5000)