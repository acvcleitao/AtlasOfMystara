## Criação de mapa
### Inferencia de mapas
- Ponto de partida: mapas bitmap de varios autores
- Extrair informação dos mapas
	- Labels
	- coastlines
	- roads
	- os hexes
	- cidades, etc
- Ferramentas necessárias
	- Processamento de imagem e computer vision para detetar estas formas
	- OCR
- Automático "supervisionado"
	- Corrigir texto de labels
	- afinar linhas de estradas, etc

### Inserção de novos mapas no mapa principal
- Reconciliar diferenças entre mapas atuais e novos mapas

## Visualização de mapas
- Mostrar mapas com diferentes níveis de zoom
	- Se houver um mapa "nativo" a esse nível de zoom mostrar esse
	- Caso contrário agregar/desagregar com base no que temos
- Suportar
	- mapas de diferentes anos (in-game)
	- mapas de diferentes anos (real world publishing dates)
	- mapas de diferentes autores
- **SUPORTAR PROJEÇÃO CORRETA**
- **Desenhar**
	- Tudo raster (mapas)
	- **Raster + vetores (mapas + labels, cidades, etc)**
		- Os hexagonos nao sao so um hexagono (floresta/montanha/rio) o hexagono pode ser um vetor e la dentro ter um bitmap
	- Tudo vetores
	- Ortogonalmente às três coisas acima
		- Fill do hex é bitmap ou vetores?
- Interatividade
	- Click on something -> get more information
		- nome
		- metadados
		- links para produtos/posts/vaults onde há mais info sobre aquilo
- Exports
	- formato machine readable qq (JSON? mas há algum formato standard para isto?)
	- Bitmaps de uma certa região com um certo nível de zoom
		- Endgame: fazer um holster para por na parede

Desenhar qualquer coisa que pareça um hexmap e tentar approaches de desenho (ver secção "Desenhar", acima)
Tamanho minimo de hexagonos no ecrã (responder a pergunta "quantos hexagonos faz sentido desenhar neste ecrã?")

**Fazer estas experiencias de forma sistematica e documentada
15000 hexagonos -> levou este tempo gastou esta memoria
fazer graficos e diagramas com varios exemplos**

Fazer estas experiencias no proximo **par de semanas**
Para depois se ver o que se pode fazer na parte de correção
-> Podemos deixar tudo nas mãos do user
Baseline -> importar mapas bit map
o thorf tem mapas em ilustrator com layers de informacao e coastlines isoladas. no caso destes mapas pode ser mais facil de identificar os mapas mas nao resolve o problema  generico dos outros mapas.

Quando o PIC acabar devemos saber o que queremos
mesmo que seja so PoC deviamos saber quais sao os angulos que queremos atacar aqui.

Ter cuidado:
Pode acontecer que a biblioteca pode não dar jeito. Não me posso deixar deslumbrar pela biblioteca.




# Considerações:
## Backend
### Ferramenta de deteção de mapas
Três partes. 

#### Deteção de hexagonos
Deteta hexagonos no mapa e tenta limpar ao máximo usando tecnicas de compressão e gaussian blur a imagem para ter apenas uma aproximação da hex grid.

#### Transformação da grid detetada em parametros
Pega na imagem gerada no algoritmo anterior e procura por parametros especificos que serão usados no algoritmo seguinte.
Parametros:
- Orientação dos hexagonos (pointy vs flat)
- Tamanho
- Forma da hex grid

Este algoritmo deve ter em consideração que as grids não devem ter buracos

#### Geração de hexagonos
Pega nos parametros gerados pelo algoritmo anterior e gera uma hex grid uniforme.

# Desafios
Hexes com cidades por cima
Hexes half half (coastline)
Estradas e fronteiras
Texto
Há mapas com linhas de elevação

futuramente queremos ter OCR
cena da google que se chama teseract
Podemos treinar o language model com o Atlas mas seria sempre um acrescento

# 6 Layers
- Hexagonos
	- Encontrados com openCV. Outline + textura
- Water bodies
	- 
- Estradas
	- 
- Fronteiras
	- 
- Glyphs
	- 
- Labels
	- Talvez associadas as villages e towns

Pre processamento:
Há mapas em resoluções diferentes, será que faz sentido ter mapas de muita resolução a ser uploaded. Pode fazer sentido fazer um resize a partida.
Devia produzir **unit tests** para estes algoritmos
Pensar na cobertura que as imagens dão em termos de 
- variabilidade de hexagonos
- Qualidade de imagem
- Ter caminhos, coastlines, etc

Dar-lhes mesmo nomes especificos e fazer um txt com a descrição das imagens e das dificuldades que podem surgir para cada uma delas. Não queremos ter coisas "a olho" e queremos definir limites para o que o algoritmo pode fazer

Conseguir gerar imagens no próximo dia
Grelha, conteudo.
Havemos de voltar ao documento quando tivermos mais informação