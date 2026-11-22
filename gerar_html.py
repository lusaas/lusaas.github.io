"""Gera as páginas estáticas da demonstração a partir dos dados de seed.py."""
import ast
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
tree = ast.parse((ROOT / 'seed.py').read_text(encoding='utf-8'))
assignment = next(node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ANIMAIS_DEMO' for t in node.targets))
animals = []
for item in assignment.value.elts:
    animals.append({ast.literal_eval(k): ast.literal_eval(v) for k, v in zip(item.keys, item.values) if ast.literal_eval(k) != 'avistamento_inicial'})

def esc(value):
    return html.escape(str(value), quote=True)

def page(title, content):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)} — GuaipeCare</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🐾</text></svg>">
    <link rel="stylesheet" href="app/static/css/style.css">
</head>
<body>
    <header class="topo-site"><div class="container-topo"><span class="icone-marca">🐾</span><div class="texto-marca"><span class="nome-marca">GuaipeCare</span><span class="subtitulo-marca">Coleira Inteligente Comunitária</span></div></div></header>
    <main class="container">{content}</main>
    <footer class="rodape-site"><p>🐾 Cuidando com carinho dos nossos amigos de quatro patas 🐾</p></footer>
</body>
</html>
'''

cards = []
for animal in animals:
    if not animal.get('destaque_demo'):
        continue
    tag, name = esc(animal['tag']), esc(animal['nome'])
    label = 'Pet da Luísa (Equipe)' if animal['nome'] == 'Almofadinhas' else esc(animal['especie'])
    cards.append(f'''<li style="padding: 0.85rem 1rem; border: 1.5px solid #ebdcc8; border-radius: 12px; background: #fdfbf7; box-shadow: 2px 2px 0px #ded0bd; transition: transform 0.15s ease;"><a href="{tag}.html" style="text-decoration: none; color: inherit; display: block;"><div style="display: flex; align-items: center; justify-content: space-between;"><strong style="font-family: Georgia, serif; font-size: 1.25rem; color: #362419;">🐕 {name}</strong><span style="font-size: 0.8rem; background: #f5ede1; border: 1px solid #e0d0bc; padding: 0.15rem 0.5rem; border-radius: 12px; color: #5a3e2b; font-weight: 600;">{label}</span></div><div style="font-size: 0.82rem; color: #826c5c; margin-top: 0.4rem; display: flex; align-items: center; gap: 0.35rem;"><span>🏷️ Coleira NFC:</span> <code style="background: #f1e6d6; border: 1px solid #decbb5; padding: 0.1rem 0.35rem; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #442e20;">/a/{tag}</code></div></a></li>''')
memorial = next((a for a in animals if a['nome'] == 'Orelha'), None)
footer = f'''<footer style="margin-top: 1.5rem; text-align: right; border-top: 1px dashed #e8dfd1; padding-top: 0.75rem;"><a href="{esc(memorial['tag'])}.html" style="font-size: 0.75rem; color: #a89685; text-decoration: none;" title="Memorial do Cão Orelha">🕊️ <em>memorial / easter egg</em></a></footer>''' if memorial else ''
index = f'''<article class="cartao"><header class="cabecalho-animal"><div class="titulo-linha"><h1>Amigos Cadastrados</h1><span class="badge-especie">🐾 Demonstração</span></div><p class="descricao" style="margin-top: 0.25rem;">Toque em uma coleira para simular a aproximação da tag NFC:</p></header><ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.85rem; margin-top: 1rem;">{''.join(cards)}</ul>{footer}</article>'''
(ROOT / 'index.html').write_text(page('Coleiras Disponíveis', index), encoding='utf-8')

for animal in animals:
    name, tag = esc(animal['nome']), esc(animal['tag'])
    photos = [p.strip() for p in animal.get('foto_url', '').replace('\n', ',').split(',') if p.strip()]
    # Não criar imagens quebradas quando o arquivo não existe no repositório.
    photos = [p for p in photos if not p.startswith('/static/') or (ROOT / 'app' / p.lstrip('/')).is_file()]
    photos = [p.replace('/static/', 'app/static/', 1) if p.startswith('/static/') else p for p in photos]
    images = ''.join(f'<div class="foto-item"><img src="{esc(p)}" alt="Foto de {name}" class="foto-animal"></div>' for p in photos)
    gallery = f'<div class="foto-container {"galeria-fotos" if len(photos) > 1 else ""}">{images}</div>' if photos else ''
    if len(photos) > 1:
        gallery += f'<p class="indicador-fotos">🐾 Deslize para o lado para ver mais fotos ({len(photos)}) 🐾</p>'
    sections = ''
    for key, heading, cls in [('descricao', '🐾 Sobre', 'descricao'), ('vacinas', '💉 Vacinas &amp; Cuidados', 'texto-vacinas'), ('contato', '📞 Contato dos cuidadores', 'contato')]:
        if animal.get(key):
            sections += f'<section class="secao"><h2>{heading}</h2><p class="{cls}">{esc(animal[key])}</p></section>'
    content = f'''<article class="cartao">{gallery}<header class="cabecalho-animal"><div class="titulo-linha"><h1>{name}</h1><span class="badge-especie">🐕 {esc(animal['especie'])}</span></div><div class="tag-nfc-selo"><span>🏷️ Tag NFC:</span> <code>{tag}</code></div></header>{sections}<section class="secao"><h2>📍 Último avistamento</h2><div class="caixa-destaque-avistamento"><span class="icone-relogio">🕒</span><p class="horario-avistamento">Disponível na versão com servidor.</p></div></section><footer class="secao aviso-privacidade"><p>🔒 <strong>Versão estática:</strong> Esta página não solicita nem registra sua localização. Para registrar e consultar avistamentos, use a versão com servidor.</p></footer><p id="status-localizacao" role="status"></p></article>'''
    (ROOT / f'{animal["tag"]}.html').write_text(page(animal['nome'], content), encoding='utf-8')
