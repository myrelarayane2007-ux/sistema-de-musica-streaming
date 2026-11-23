# Sistema de Música Streaming

Aplicação de terminal em Python com MySQL para gerenciar usuários, músicas e playlists/histórico.

## Corrigindo o erro `MYSQL_PASSWORD`

A mensagem aparece porque a senha não deve ficar gravada no código e a variável de ambiente ainda não está configurada. Na pasta do projeto, no terminal integrado do VS Code:

1. Instale e inicie o MySQL Server.
2. Copie `.env.example` para `.env` e edite `MYSQL_PASSWORD` com a senha do seu usuário MySQL. No Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

3. Instale as dependências e crie/atualize o banco. Abra `schema.sql` no MySQL Workbench e execute todo o script conectado ao servidor local. Ele cria `streaming_db`, as tabelas e inclui as nove músicas pedidas. Pode ser executado novamente sem duplicar essas músicas.
4. Execute a aplicação:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python app.py
   ```

Se o terminal bloquear a ativação do ambiente virtual, use `python -m pip install -r requirements.txt` sem ativá-lo. Também é possível informar a senha apenas para a sessão do PowerShell, sem `.env`:

```powershell
$env:MYSQL_PASSWORD = "sua_senha_do_mysql"
python app.py
```

Para Linux/macOS, use `cp .env.example .env`, edite o arquivo e execute `python3 -m pip install -r requirements.txt` e `python3 app.py`.

> Não coloque senha real no código, no README ou em commits. `.env` é ignorado pelo Git; envie somente `.env.example` sem credenciais reais.

## Cadastro das músicas

O script cadastra as nove músicas com título, artista e álbum. Duração e URL de áudio ficam vazias porque não foram fornecidos dados confirmados nem links de áudio autorizados. Para tocar uma faixa, edite o registro pelo menu **Músicas → Atualizar** e informe a duração e uma URL de áudio que você tenha direito de usar. O nome de um vídeo do YouTube não é, por si só, uma URL MP3.

## Roteiro de teste no VS Code

Após configurar o `.env`, executar `schema.sql` e iniciar `python app.py`, teste cada opção. Anote os IDs exibidos para usar nas etapas seguintes.

### 1. Conexão e usuários

- No menu principal, escolha `1` → `2`: deve listar os usuários ou mostrar “Nenhum usuário cadastrado”, sem erro de senha/conexão.
- Escolha `1` → `1` e cadastre um usuário de teste: `Usuário Teste`, CPF válido `52998224725`, e-mail `teste.copilot@example.com`, plano `Gratuito`.
- Use `1` → `2` para confirmar o cadastro.
- Use `1` → `3`, informe o ID desse teste e atualize nome/e-mail/plano; liste novamente.
- Use `1` → `4` para excluir somente o usuário de teste.

### 2. Músicas

- Escolha `2` → `2`: devem aparecer as nove músicas incluídas pelo SQL. Duração e URL aparecerão como “não informada”.
- Teste `2` → `1` cadastrando uma faixa de teste, por exemplo `Faixa de teste`, artista `Artista Teste`, álbum `Single`, duração `180` e URL `https://example.com/audio.mp3` (URL ilustrativa, não reproduz áudio).
- Liste, atualize a faixa pelo ID, liste novamente e exclua somente a faixa de teste.
- Opcional: cadastre uma faixa com Enter para duração e URL; ela deve ser aceita como metadado sem esses campos.

### 3. Playlists e histórico

- Cadastre um usuário de teste ou use o ID de um usuário já listado e anote o ID de uma das músicas.
- No menu `3` → `1`, informe os IDs, escolha `PLAYLIST` e dê um nome como `Teste Copilot`.
- Em `3` → `2`, informe o ID do mesmo usuário e confirme o registro.
- Use `3` → `3` para mudar nome/tipo e `3` → `2` para verificar.
- Use `3` → `4` para excluir apenas o registro de teste.

### 4. Tratamento do erro de configuração

Feche a aplicação, remova temporariamente `MYSQL_PASSWORD` do `.env` (ou renomeie `.env`), rode `python app.py` e tente listar usuários ou músicas. O programa deve explicar que a configuração está faltando, sem traceback. Depois restaure o `.env`.

**Atenção:** excluir um usuário ou uma música remove também seus registros de playlist/histórico relacionados, por causa das chaves estrangeiras `ON DELETE CASCADE`. Faça os testes de exclusão apenas com dados de teste.
