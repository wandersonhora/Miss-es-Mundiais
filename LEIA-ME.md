# Painel de Missões Mundiais

Aplicativo estático (HTML/CSS/JS puro, sem servidor) com:
- **% de evangélicos e outras religiões nos 195 países soberanos do mundo** (193 Estados-membros da ONU + Vaticano + Palestina), mais 10 territórios de relevância missionária (Hong Kong, Macau, Taiwan, Kosovo etc., identificados separadamente) — fonte: Joshua Project
- **Perseguição religiosa** — ranking da Lista Mundial da Perseguição 2026 (Portas Abertas)
- **Mapa mundial colorido por nível de perseguição** — escala de cores do mais claro (fora da lista) ao mais escuro (perseguição extrema), com tooltip ao passar o mouse
- **Missionários e pedidos de oração** — cadastro editável
- **Relógio e data atual** no fuso America/Sao_Paulo, e aviso automático de quando os dados foram gerados

## Como publicar no Netlify (sem usar linha de comando)

1. Acesse **https://app.netlify.com** e crie uma conta gratuita (ou entre na sua).
2. Na tela inicial ("Sites"), **arraste a pasta inteira `missoes-app`** (esta pasta) para a área que diz "Drag and drop your site output folder here".
3. Aguarde alguns segundos — o Netlify já publica e te dá um link tipo `https://nome-aleatorio.netlify.app`.
4. (Opcional) Em **Site settings → Change site name**, escolha um nome melhor, por exemplo `missoes-mundiais.netlify.app`.
5. Pronto — o app está no ar. Toda vez que alguém abrir, ele mostra a data/hora atual e avisa se os dados estão desatualizados.

## Como atualizar os dados depois

Os dados **não** são buscados automaticamente da internet (nenhum app grátis faz isso de forma confiável sem um servidor/API paga) — mas o app deixa isso muito claro na aba **"Fontes & Como atualizar"**, mostrando a data em que os dados foram gerados e alertando quando estiverem desatualizados.

Para atualizar:

1. Abra o arquivo `data/countries.json` (percentuais de religião e perseguição) ou `data/missionaries.json` (missionários e pedidos de oração) em qualquer editor de texto.
2. Edite os números/textos que mudaram.
3. Atualize o campo `"generatedAt"` (em `countries.json`) ou `"lastUpdated"` de cada missionário (em `missionaries.json`) para a data atual, no formato `AAAA-MM-DD`.
4. Volte no Netlify e **arraste a pasta atualizada de novo** — ele substitui o site publicado automaticamente, mantendo o mesmo link.

### Frequência recomendada
- **Pedidos de oração dos missionários:** revisar a cada 2–4 semanas (o app avisa quando passa de 45 dias sem atualização).
- **% de evangélicos / outras religiões / ranking de perseguição:** essas pesquisas (Joshua Project, Lista Mundial da Perseguição) só saem uma vez por ano — revisar quando sair a nova edição (a LMP geralmente é lançada em janeiro).

## Fontes usadas na base inicial

- Joshua Project — https://joshuaproject.net/global/countries
- Portas Abertas, Lista Mundial da Perseguição 2026 — https://portasabertas.org.br/lista-mundial/paises-da-lista/

Os dados de **missionários** foram deixados como **exemplos ilustrativos** — substitua pelos dados reais da sua igreja/agência (JMN, JOCUM etc.) editando `data/missionaries.json`.

## Sobre o mapa

O mapa (aba "🗺️ Mapa da Perseguição") desenha o mundo com a biblioteca gratuita **D3.js** e a base geográfica pública **world-atlas**, carregadas de um CDN (cdn.jsdelivr.net) no momento em que a página abre — por isso é necessário estar **conectado à internet** para o mapa aparecer (as outras abas funcionam mesmo offline, já que os dados delas ficam salvos localmente). Se o mapa não carregar, o app mostra um aviso amigável e o resto do site continua funcionando normalmente.

Cada país é colorido pelo `persecutionLevel` já calculado em `data/countries.json` — não é preciso mexer no mapa para atualizá-lo: basta atualizar os dados de perseguição (`persecutionRank2026`) como explicado acima, e as cores do mapa mudam sozinhas. Microestados muito pequenos (Vaticano, Mônaco, San Marino etc.) podem não aparecer visualmente por causa da resolução do mapa-múndi, mas continuam listados normalmente nas outras abas.

## Estrutura de arquivos

```
missoes-app/
├── index.html          → página principal
├── css/style.css        → visual do app (funciona em modo claro/escuro)
├── js/app.js             → lógica: relógio, filtros, leitura dos JSONs
├── js/map.js             → desenha o mapa mundial colorido por nível de perseguição
├── data/countries.json   → dados de religião e perseguição por país
├── data/missionaries.json→ cadastro de missionários (EDITAR com dados reais)
├── netlify.toml          → configuração de publicação no Netlify
└── scripts/build_data_full.py → script auxiliar usado para gerar countries.json a partir dos dados do Joshua Project (não é publicado no site; scripts/jp_raw_table.txt é a fonte bruta que ele lê)
```
