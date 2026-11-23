CREATE DATABASE IF NOT EXISTS streaming_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE streaming_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    plano ENUM('Gratuito', 'Premium', 'Familia', 'Universitário') NOT NULL DEFAULT 'Gratuito',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS musicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    artista VARCHAR(150) NOT NULL,
    album VARCHAR(150) NOT NULL DEFAULT 'Single',
    duracao INT NULL,
    url_mp3 VARCHAR(2048) NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS playlists_historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    musica_id INT NOT NULL,
    nome_playlist VARCHAR(150) NOT NULL DEFAULT 'Histórico de Reprodução',
    tipo_registro ENUM('PLAYLIST', 'HISTORICO') NOT NULL DEFAULT 'HISTORICO',
    adicionado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ph_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ph_musica FOREIGN KEY (musica_id) REFERENCES musicas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Atualiza instalações antigas para permitir cadastrar metadados antes de obter
-- a duração e um link de áudio autorizado.
ALTER TABLE musicas MODIFY duracao INT NULL;
ALTER TABLE musicas MODIFY url_mp3 VARCHAR(2048) NULL;

-- Catálogo inicial. Títulos e artistas são cadastrados sem duração/link inventados.
-- O WHERE NOT EXISTS torna este bloco seguro para executar novamente.
INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Demon Slayer: Kimetsu no Yaiba ED1', 'FictionJunction feat. LiSA', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Demon Slayer: Kimetsu no Yaiba ED1' AND artista='FictionJunction feat. LiSA');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Elements', 'John Michael Howell & ZVC', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Elements' AND artista='John Michael Howell & ZVC');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Hall of Fame', 'The Script feat. will.i.am', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Hall of Fame' AND artista='The Script feat. will.i.am');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Die For You', 'Starset', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Die For You' AND artista='Starset');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Counting Stars', 'OneRepublic', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Counting Stars' AND artista='OneRepublic');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Cha-La-Head-Cha-La', 'Dragon Ball Z (versão PT-BR)', 'Abertura', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Cha-La-Head-Cha-La' AND artista='Dragon Ball Z (versão PT-BR)');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Galopeira', 'Chitãozinho e Xororó', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Galopeira' AND artista='Chitãozinho e Xororó');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'Missing Piece', 'John Michael Howell', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='Missing Piece' AND artista='John Michael Howell');

INSERT INTO musicas (titulo, artista, album, duracao, url_mp3)
SELECT 'T氏の話を信じるな / Don’t Believe in T', 'ピノキオピー feat. 初音ミク・重音テト', 'Single', NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM musicas WHERE titulo='T氏の話を信じるな / Don’t Believe in T' AND artista='ピノキオピー feat. 初音ミク・重音テト');
