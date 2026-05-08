









## MANUAL TÉCNICO DE
## POSICIONAMENTO
Georreferenciamento de Imóveis Rurais










## 1ª Edição

## Brasília
## 2013


## REPÚBLICA FEDERATIVA DO BRASIL
## MINISTÉRIO DO DESENVOLVIMENTO AGRÁRIO
## INSTITUTO NACIONAL DE COLONIZAÇÃO E REFORMA AGRÁRIA
Diretoria de Ordenamento da Estrutura Fundiária
Coordenação Geral de Cartografia









Manual Técnico de
## Posicionamento:
georreferenciamento de imóveis rurais










## 1ª Edição

## Brasília
## 2013

## DILMA VANA ROUSSEFF
Presidente da República

## GILBERTO JOSÉ SPIER VARGAS
Ministro do Desenvolvimento Agrário

## CARLOS MÁRIO GUEDES DE GUEDES
Presidente do Instituto Nacional de Colonização e Reforma Agrária

## RICHARD MARTINS TORSIANO
Diretor de Ordenamento da Estrutura Fundiária

## WILSON SILVA JÚNIOR
Coordenador Geral de Cartografia









## EQUIPE RESPONSÁVEL PELA ELABORAÇÃO:
## ACILAYNE FREITAS DE AQUINO
Analista em Reforma e Desenvolvimento Agrário – Engenheira Agrimensora
## AILTON CARDOSO TRINDADE
Técnico em Reforma e Desenvolvimento Agrário – Técnico em Agrimensura
## DÉRISSON LISBÔA NOGUEIRA
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Agrimensor
## HELIOMAR VASCONCELOS
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Agrimensor
## KILDER JOSÉ BARBOSA
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Agrimensor
## MARCELO JOSÉ PEREIRA DA CUNHA
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Agrimensor
## MIGUEL PEDRO DA SILVA NETO
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Cartógrafo
## OSCAR OSÉIAS DE OLIVEIRA
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Agrimensor
## ROBERTO NERES QUIRINO DE OLIVEIRA
Analista em Reforma e Desenvolvimento Agrário – Engenheiro Cartógrafo

## Sumário

Manual Técnico de Posicionamento                                                                              Página: i
## SUMÁRIO
LISTA DE SIGLAS ........................................................................................................................ iii
LISTA DE FIGURAS ..................................................................................................................... iv
LISTA DE QUADROS .................................................................................................................. v
1 INTRODUÇÃO ............................................................................................................... 6
2 POSICIONAMENTO POR GNSS ................................................................................... 7
2.1 Posicionamento relativo................................................................................... 7
2.1.1 Posicionamento relativo estático ................................................................ 8
2.1.2 Posicionamento relativo estático-rápido ................................................... 9
2.1.3 Posicionamento relativo semicinemático (stop and go)......................... 9
2.1.4 Posicionamento relativo cinemático .......................................................... 9
2.1.5 Posicionamento relativo a partir do código C/A ................................... 10
2.2 RTK e DGPS ....................................................................................................... 10
2.2.1 RTK convencional ......................................................................................... 10
2.2.2 RTK em rede .................................................................................................. 11
2.2.3 Differential GPS (DGPS) ............................................................................... 13
2.3 Posicionamento por ponto preciso (PPP) .................................................... 13
3 POSICIONAMENTO POR TOPOGRAFIA CLÁSSICA ................................................. 14
3.1 Poligonação .................................................................................................... 14
3.2 Triangulação .................................................................................................... 16
3.3 Trilateração ...................................................................................................... 16
3.4 Triangulateração ............................................................................................. 16
3.5 Irradiação ......................................................................................................... 17
3.6 Interseção linear .............................................................................................. 18
3.7 Interseção angular .......................................................................................... 19
3.8 Alinhamento .................................................................................................... 19
4 POSICIONAMENTO POR GEOMETRIA ANALÍTICA .................................................. 21
4.1 Paralela ............................................................................................................. 21
4.2 Interseção de retas ......................................................................................... 21
5 POSICIONAMENTO POR SENSORIAMENTO REMOTO ............................................ 23
6 BASE CARTOGRÁFICA ............................................................................................... 24
7 APLICAÇÃO DOS MÉTODOS DE POSICIONAMENTO ............................................ 25

## Sumário

Manual Técnico de Posicionamento                                                                              Página: ii
7.1 Vértices de apoio ............................................................................................ 25
7.2 Vértices de limite ............................................................................................. 25
8 MÉTODOS DE POSICIONAMENTO E TIPOS DE VÉRTICES ........................................ 27
9 CÁLCULOS .................................................................................................................. 28
9.1 Conversão de coordenadas cartesianas geocêntricas para locais ...... 28
9.2 Conversão de coordenadas cartesianas locais para geocêntricas ...... 29
9.3 Área ................................................................................................................... 30
9.4 Distância horizontal ......................................................................................... 31
9.5 Azimute ............................................................................................................. 31
10 GUARDA DE PEÇAS TÉCNICAS E DOCUMENTAÇÃO ............................................ 32
REFERÊNCIAS ........................................................................................................................... 33

Lista de Siglas

Manual Técnico de Posicionamento                                                                              Página: iii
## LISTA DE SIGLAS
ABNT – Associação Brasileira de Normas Técnicas
C/A – Course Aquisition
CNSS – China’s Compass Navigation Satellite System
DGPS – Differential GPS
EGNOS – European Geostationary Navigation Overlay System
GBAS – Ground Based Augmentation System
GLONASS – Globalnaya Navigatsionnaya Sputnikovaya Sistema
GNSS – Global Navigation Satellite System
IBGE – Fundação Instituto Brasileiro de Geografia e Estatística
NAVSTAR-GPS – NAVigation System  with  Timing  And  Ranging - Global  Positioning
## System
NTGIR – Norma Técnica para Georreferenciamento de Imóveis Rurais
NTRIP – Networked Transport of RTCM via Internet Protocol
PPP – Posicionamento por Ponto Preciso
RBMC – Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
RIBaC – Rede INCRA de Bases Comunitárias do GNSS
RTCM – Radio Technical Commission for Maritime Services
RTK – Real Time Kinematic
SGB – Sistema Geodésico Brasileiro
SIRGAS – Sistema de Referência Geocêntrico para as Américas
WAAS – Wide Area Augmentation System

Lista de Figuras

Manual Técnico de Posicionamento                                                                              Página: iv
## LISTA DE FIGURAS
Figura 1 – Posicionamento relativo ....................................................................................... 8
Figura 2 – RTK convencional ................................................................................................. 11
Figura 3 – RTK em rede .......................................................................................................... 12
Figura 4 – Poligonal “tipo 1” ................................................................................................. 15
Figura 5 – Poligonal “tipo 2” ................................................................................................. 15
Figura 6 – Poligonal “tipo 3” ................................................................................................. 15
Figura 7 – Triangulação ......................................................................................................... 16
Figura 8 – Trilateração ........................................................................................................... 16
Figura 9 – Triangulateração .................................................................................................. 17
Figura 10 – Irradiação observando ângulo e distância ................................................... 17
Figura 11 – Irradiação observando azimute e distância ................................................. 18
Figura 12 – Irradiação com observações redundantes ................................................... 18
Figura 13 – Interseção linear................................................................................................. 19
Figura 14 – Interseção angular ............................................................................................ 19
Figura 15 – Alinhamento ....................................................................................................... 20
Figura 16 – Paralela ............................................................................................................... 21
Figura 17 – Três possibilidades de interseção de retas ..................................................... 22
Figura 18 – Sistema Geodésico Local e Sistema Geocêntrico ....................................... 30


Lista de Quadros

Manual Técnico de Posicionamento                                                                              Página: v
## LISTA DE QUADROS
Quadro 1 – Características técnicas para posicionamento relativo estático ............... 9
Quadro 2 – Métodos de posicionamento para vértices de apoio ................................ 25
Quadro 3 – Métodos de posicionamento para vértices de limite ................................. 26
Quadro 4 – Métodos de posicionamento e tipos de vértices ........................................ 27

## 1 Introdução

Manual Técnico de Posicionamento                                                                              Página: 6
## 1 INTRODUÇÃO
Este documento juntamente com o Manual Técnico de Limites e Confrontações e a
Norma  Técnica  para  Georreferenciamento  de  Imóveis  Rurais  (NTGIR)  3ª  Edição,
formam    o    novo    conjunto    de    normas    para    execução    dos    serviços    de
georreferenciamento de imóveis rurais.
Em comparação com as edições anteriores da NTGIR, este manual traz mudanças
significativas, dentre elas podemos destacar a possibilidade de utilização de novos
métodos  de  posicionamento;  menor  detalhamento  de  especificações  técnicas
(atribuindo esta  tarefa  ao  credenciado);  utilização  do  Sistema  Geodésico  Local
(SGL)  para  o  cálculo  de  área;  apresenta  a  formulação  matemática  para  cálculos
utilizando topografia clássica e amplia a possibilidade de utilização de métodos de
posicionamento por sensoriamento remoto.
Nos  capítulos de  2 a  5  estão descritos  os  métodos  de posicionamento  que podem
ser usados nos serviços de georreferenciamento de imóveis rurais, o capítulo 6 traz a
possibilidade  de  obtenção  de  coordenadas  a  partir  de  bases  cartográficas.    O
capítulo  7  estabelece  quais  métodos  podem  ser  aplicados  no  posicionamento  de
vértices  de  limite  e vértices  de apoio  e  o capítulo 8  estabelece a  compatibilidade
entre  métodos  de  posicionamento  e  tipos  de  vértices.  O  capítulo  9  detalha
formulações  matemáticas  para  conversão  de  coordenadas  geocêntricas  para
locais,  bem  como  o  cálculo  das  grandezas  área,  distância  e  azimute.  Por  fim,  o
capítulo 10 salienta que é fundamental a guarda de todo material que subsidiou a
obtenção das coordenadas e das precisões dos vértices.

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 7
## 2 POSICIONAMENTO POR GNSS
A  sigla  GNSS  (Global  Navigation  Satellite System)  é  uma  denominação  genérica
que  contempla sistemas  de  navegação com  cobertura  global,  além  de  uma  série
de infraestruturas espaciais (SBAS – Satellite Based Augmentation System) e terrestre
(GBAS – Ground   Based   Augmentation   System) que   associadas   aos   sistemas
proporcionam maior precisão e confiabilidade.
Dentre os sistemas englobados pelo GNSS podemos citar:
a) NAVSTAR-GPS   (NAVigation   System   with   Timing   And   Ranging – Global
Positioning System), mais conhecido como GPS. Sistema norte-americano;
b) GLONASS   (Globalnaya   Navigatsionnaya   Sputnikovaya   Sistema).   Sistema
russo;
c) Galileu. Sistema europeu;
d) Compass/Beidou   (China’s  Compass  Navigation  Satellite  System – CNSS).
Sistema chinês.
Em relação ao SBAS temos os seguintes exemplos:
a) WAAS (Wide Area Augmentation System). Sistema norte americano;
b) EGNOS   (European Geostationary   Navigation   Overlay   System). Sistema
europeu.
O posicionamento   por   GNSS   pode   ser   realizado   por   diferentes   métodos   e
procedimentos.    Neste    documento    serão    abordados    apenas    aqueles    que
proporcionam   precisão   adequada   para   serviços   de   georreferenciamento   de
imóveis rurais, tanto para o estabelecimento de vértices de referência, quanto para
o posicionamento de vértices de limites (artificiais e naturais).
Nos próximos tópicos é feita uma breve descrição sobre cada um dos métodos de
posicionamento  por  GNSS,  aplicados  aos  serviços  de  georreferenciamento  de
imóveis rurais.
## 2.1 POSICIONAMENTO RELATIVO
No   posicionamento   relativo,   as   coordenadas   do   vértice   de   interesse   são
determinadas  a  partir  de  um  ou  mais  vértices  de  coordenadas  conhecidas.  Neste
caso    é    necessário    que    dois    ou    mais    receptores    GNSS    coletem    dados

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 8
simultaneamente,   onde   ao   menos   um   dos   receptores   ocupe   um   vértice   de
referência (Figura 1).

Figura 1 – Posicionamento relativo
No posicionamento relativo podem se usar as observáveis: fase da onda portadora,
pseudodistância ou  as  duas  em  conjunto.  Sendo  que  a  fase  da  onda  portadora
proporciona  melhor  precisão  e  por  isso  ela  é  a  única  observável  aceita  na
determinação  de  coordenadas  de vértices de  apoio  e vértices  situados  em limites
artificiais.  O  posicionamento  relativo  utilizando  a  observável pseudodistância só  é
permitido  para  a  determinação  de  coordenadas  de  vértices  situados  em  limites
naturais.
Pelo fato de haver várias possibilidades de se executar um posicionamento relativo
usando  a  observável  fase  da  onda  portadora,  neste  documento  este  tipo  de
posicionamento   foi   subdividido   em   quatro   grupos:   estático,   estático-rápido,
semicinemático  e  cinemático.  O  posicionamento  relativo usando  a  observável
pseudodistância foi tratado como posicionamento relativo a partir do código C/A.
2.1.1 Posicionamento relativo estático
No  posicionamento  relativo  estático,  tanto  o(s)  receptor(es)  do(s)  vértice(s)  de
referência quanto o(s) receptor(es) do(s) vértice(s) de interesse devem permanecer
estacionados (estáticos) durante todo o levantamento. Neste método, a sessão de
rastreio  se  estende  por  um  longo  período.  Recomenda-se  observar  os  valores
constantes no Quadro 1.


Vértice de referência
Vértice de interesse
## (
## X,
## Y,
## Z)

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 9
Quadro 1 – Características técnicas para posicionamento relativo estático
Linha de
## Base (km)
## Tempo Mínimo
## (minutos)
## Observáveis
Solução da
## Ambiguidade
## Efemérides
0 – 10 20 L1 ou L1/L2 Fixa Transmitidas ou Precisas
10 – 20 30 L1/L2 Fixa Transmitidas ou Precisas
10 – 20 60 L1 Fixa Transmitidas ou Precisas
20 – 100 120 L1/L2 Fixa ou Flutuante Transmitidas ou Precisas
100 – 500 240 L1/L2 Fixa ou Flutuante Precisas
500 – 1000 480 L1/L2 Fixa ou Flutuante Precisas
2.1.2 Posicionamento relativo estático-rápido
O posicionamento  relativo  estático-rápido  é  similar  ao  relativo  estático,  porém,  a
diferença  básica  é  a  duração  da  sessão  de  rastreio,  que  neste  caso,  em  geral  é
inferior a 20 minutos.
Por   não   haver   necessidade   de   manter   o   receptor   coletando   dados   no
deslocamento entre os vértices de interesse, esse método é uma alternativa para os
casos onde ocorram obstruções no intervalo entre os vértices de interesse.
2.1.3 Posicionamento relativo semicinemático (stop and go)
Este método  de  posicionamento  é  uma  transição  entre o  estático-rápido  e  o
cinemático.  O  receptor  que  ocupa  o  vértice  de  interesse  permanece  estático,
porém  num  tempo  de  ocupação  bastante  curto,  necessitando  coletar  dados  no
deslocamento  entre  um  vértice  de  interesse  e  outro.  Quanto  maior  a  duração  da
sessão de  levantamento  com  a  coleta  de  dados  íntegros,  sem  perdas  de  ciclos,
melhor a precisão na determinação de coordenadas.
Como  é  necessário  coletar  dados  no  deslocamento  entre  os  vértices  de  interesse,
este método não deve ser usado em locais que possuam muitas obstruções. Como
os limites de imóveis rurais geralmente estão situados em locais nessas condições, os
profissionais   devem   ficar   atentos   quanto   à   utilização   deste   método, pois   os
resultados  em  termos de precisão podem  estar  fora  dos padrões estabelecidos  na
NTGIR 3ª Edição.
2.1.4 Posicionamento relativo cinemático
No  posicionamento  relativo  cinemático,  enquanto  um  ou  mais  receptores  estão
estacionados  no(s)  vértice(s)  de  referência,  o(s)  receptor(es)  que  coleta(m)  dados
dos  vértices  de  interesse  permanece(m) em  movimento.  A  cada  instante  de

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 10
observação,  que  coincide  com  o  intervalo  de  gravação,  é  determinado  um
conjunto de coordenadas.
Este método é apropriado para o levantamento de limites de imóveis definidos por
feições  lineares  com  muita  sinuosidade,  porém a  sua  utilização  em  locais  com
muitas obstruções é limitada, conforme descrito para o método semicinemático.
2.1.5 Posicionamento relativo a partir do código C/A
Os  diferentes  métodos  de  posicionamento  relativo  apresentados  anteriormente
pressupõem   a   utilização da   observável   fase   da   onda   portadora.   O   método
contemplado  neste  tópico  refere-se  ao  posicionamento  relativo  com  a  utilização
da  observável  pseudodistância  a  partir  do  código  C/A  e  a  disponibilidade  de
coordenadas se dá por meio de pós-processamento.
Neste  método  também  há  necessidade  de  um  ou  mais  receptores  ocuparem
vértices   de coordenadas   conhecidas enquanto   outro(s)   coleta(m)   dados   dos
vértices     de     interesse.     Devido     a     menor     precisão     proporcionada     pela
pseudodistância a  partir  do  código  C/A,  este  método  não  é  adequado  para  a
determinação  de  coordenadas  de  vértices  situados  em  limites  artificiais,  sendo
aceito apenas na determinação de limites naturais, desde que se alcance valor de
precisão dentro dos padrões estabelecidos na NTGIR 3ª Edição.
## 2.2 RTK E DGPS
O conceito de posicionamento pelo RTK  (Real Time Kinematic) e DGPS  (Differential
GPS)  baseia-se  na  transmissão  instantânea  de  dados  de  correções  dos  sinais  de
satélites,   do(s)   receptor(es)   instalado(s)   no(s)   vértice(s)   de   referência   ao(s)
receptor(es) que  percorre(m)  os  vértices  de  interesse.  Desta  forma,  proporciona  o
conhecimento  instantâneo  (tempo  real)  de  coordenadas  precisas  dos  vértices
levantados.
2.2.1 RTK convencional
No modo convencional os dados de correção são transmitidos por meio de um link
de  rádio  do  receptor  instalado  no  vértice  de  referência  ao(s)  receptore(s)  que
percorre(m)  os  vértices  de  interesse.  A  solução  encontrada  é  uma  linha  de  base
única, conforme Figura 2.

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 11

Figura 2 – RTK convencional
Um fator que limita a área de abrangência para a realização de levantamentos por
RTK convencional é o alcance de transmissão das ondas de rádio. Basicamente, o
alcance  máximo  é  definido em  função  da  potência  do  rádio  e  das  condições
locais em termos de obstáculos físicos.
A    utilização   deste   método,    para   determinação   de   limites    artificiais,   está
condicionada a solução do vetor das ambiguidades como inteiro (solução fixa).
2.2.2 RTK em rede
No  RTK  em  rede,  ao  invés  de  apenas  uma  estação  de  referência,  existem  várias
estações de monitoramento contínuo conectadas a um servidor central, a partir do
qual  são  distribuídos,  por  meio  da  Internet,  os  dados  de  correção  aos  receptores
móveis, conforme ilustrado na Figura 3.
## (
## X,
## Y,
## Z)
Receptor de
referência
Rádio de
comunicação
Link de rádio
## Receptor
móvel

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 12

Figura 3 – RTK em rede
Com   este   método   de   posicionamento   é   possível   obter   mais   de   um   vetor,
dependendo do número de estações de referência envolvidas, e com isso efetuar
o ajustamento das observações, proporcionando maior precisão e controle.
Essa  tecnologia  se  difundiu  pela  disponibilidade  de telefonia  celular,  do  tipo  GSM,
GPRS e 3G.  A  limitação  de  aplicação  dessa  tecnologia  é  a  disponibilidade  de
serviços de telefonia celular na área de trabalho, situação comum nas áreas rurais
brasileiras.
Um  serviço  de  RTK  em  rede  é  fornecido  gratuitamente  pelo  IBGE,  que  disponibiliza
dados  de  correção via  protocolo  Internet  conhecido  por Networked  Transport  of
RTCM  via  Internet  Protocol (NTRIP),  em  formato definido  pelo Radio  Technical
Committee    for    Maritime    Service (RTCM).    A    possibilidade    de    se    efetuar
posicionamento  relativo  cinemático  em  tempo  real,  a  partir  desse  serviço,  fica
restrita  a  locais  situados  próximos  às  estações  de  referência  da  Rede  Brasileira  de
Monitoramento   Contínuo   dos   Sistemas   GNSS   (RBMC),   que   disponibilizam   esse
serviço. Mais informações em: http://www.ibge.gov.br/home/
geociencias/geodesia/rbmc/ntrip/.
## Receptor
## Móvel
Centro de
Controle de dados
## Internet
Estação de
## Monitoramento
Contínuo GNSS
Estação de
## Monitoramento
Contínuo GNSS
## X,
## Y,
## Z
## X,
## Y,
## Z

2 Posicionamento por GNSS

Manual Técnico de Posicionamento                                                                              Página: 13
2.2.3 Differential GPS (DGPS)
O   DGPS   tem   fundamento   análogo   ao   RTK,   porém   a observável   usada   é   a
pseudodistância  a  partir  do  código  C/A.  Portanto, este  método  provê  precisão
inferior  ao  RTK  e  sua  aplicação  nos  serviços  de georreferenciamento  de  imóveis
rurais fica  restrita  ao  posicionamento  dos  vértices  situados  em  limites  naturais.  O
mesmo serviço citado no item 2.2.2 é disponibilizado para o DGPS.
## 2.3 POSICIONAMENTO POR PONTO PRECISO (PPP)
Com o posicionamento por ponto preciso, as coordenadas do vértice de interesse
são   determinadas   de   forma   absoluta,   portanto,   dispensa   o   uso   de   receptor
instalado sobre um vértice de coordenadas conhecidas.
O  IBGE  disponibiliza  um  serviço  on-line  de  PPP  que  processa  dados  no  modo
estático e cinemático em http://www.ppp.ibge.gov.br/ppp.htm.

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 14
## 3 POSICIONAMENTO POR TOPOGRAFIA CLÁSSICA
A  topografia  clássica  pode  ser  adotada  de  forma  isolada  ou  em  complemento  a
trabalhos   conduzidos   por   posicionamento   GNSS,   principalmente   onde   este   é
inviável,  em  função  de  obstruções  físicas  que  prejudicam  a  propagação  de  sinais
de satélites.
Os   posicionamentos   executados   pelos   métodos   poligonação,   triangulação,
trilateração   e   triangulateração, devem   permitir   o   tratamento   estatístico   das
observações   pelo   método   dos   mínimos   quadrados.   Portanto,   eles   devem
contemplar observações redundantes, ou seja, o número de observações deve ser
superior ao número de incógnitas.
Para  atender  ao  disposto  no  parágrafo  anterior,  os  posicionamentos  deverão  se
apoiar  em,  no  mínimo,  quatro  vértices  de  referência,  sendo  dois  vértices  de
“partida”  e  dois  de  “chegada”,  com  exceção da  poligonal  do  “tipo  1”,  que  se
apoia  em  apenas  dois  vértices.  Pela  praticidade,  os  vértices  de  referência  devem
ter suas coordenadas determinadas por meio de posicionamento por GNSS.
A triangulação, trilateração e triangulateração são alternativas para serem usadas
no  estabelecimento  de  vértices  de referência, a  partir  dos  quais  se  determina  as
coordenadas  dos  vértices  de  limite,  por  irradiação,  interseção  linear  ou  interseção
angular.
Nos próximos tópicos é feita uma breve descrição sobre cada um dos métodos de
posicionamento por topografia clássica, aplicados aos serviços de
georreferenciamento  de  imóveis  rurais.  Nas  figuras de  4  a  17, a  cor  vermelha
representa os valores observados e a cor preta os valores conhecidos.
## 3.1 POLIGONAÇÃO
A  poligonação  se  baseia  na  observação  de  direções  e  distâncias  entre  vértices
consecutivos de uma poligonal. A coleta de dados é realizada com a instalação de
um  equipamento  de   medição  sobre   um   dos  vértices   da   poligonal,   deste,   é
observada  a  direção  em  relação  ao  vértice  anterior (vértice “ré”), a direção ao
vértice posterior (vértice “vante”) e as distâncias entre os vértices.
Nos  trabalhos  de  georreferenciamento  de  imóveis  rurais  poderá  ser  usado  um  dos
três  tipos  de  poligonais  previstos  no  item  6.5.1  da  Norma  NBR  13.133/1.994  da
Associação Brasileira de Normas Técnicas (ABNT).  As figuras 4, 5 e 6 ilustram os tipos
de poligonais.

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 15

## Figura 4 – Poligonal “tipo 1”

## Figura 5 – Poligonal “tipo 2”

## Figura 6 – Poligonal “tipo 3”
## B
## A
## C
## D
## E
d
## AB
## BC
## CD
## DE
## 3
## 4
## F
## H
## 1
## 5
## 2
d
d
d
## G
## EF
d
## FG
d
## GH
d
## 6
## 7
## 8
## B
## A
## C
## D
## E
d
## AB
## BC
## CD
## DE
## 3
## 4
## 2
## 1
## 1
## 5
## 2
d
d
d
## B
## A
## C
## D
## E
d
## AB
## BC
## CD
## DE
## 3
## 4
## 2
## 1
## 1
## 5
## 2
d
d
d

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 16
## 3.2  TRIANGULAÇÃO
A  determinação  de  coordenadas,  a  partir  do  método  da  triangulação,  é  obtida
por  meio  da  observação  de  ângulos  formados  entre  os  alinhamentos  de  vértices
intervisíveis de uma rede de triângulos (Figura 7).

## Figura 7 – Triangulação
## 3.3 TRILATERAÇÃO
O   posicionamento   por   meio   da trilateração   é   baseado   na   observação   de
distâncias entre os vértices intervisíveis de uma rede de triângulos (Figura 8).

## Figura 8 – Trilateração
## 3.4 TRIANGULATERAÇÃO
Na   triangulateração   são   observados   ângulos   e   distâncias   entre   os   vértices
intervisíveis de uma rede de triângulos (Figura 9).
## B
## C
## A
## D
## F
## E
## 1
## 2
## 5
## 6
## 7
## 8
## 13
## 14
## 18
## 17
## 12
## 11
## 10
## 9
## 4
## 3
## G
## H
## 22
## 21
## 15
## 16
## 19
## 20
## 24
## 23
## B
## C
## A
## D
## F
## E
## G
## H
d
## AC
d
## AD
d
## BC
d
## BD
d
## DC
d
## CF
d
## CE
d
## DE
d
## DF
d
## FE
d
## EH
d
## FG
d
## EG
d
## FH

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 17
Em  função  da  praticidade  em  se  medir  distâncias  e  ângulos  com  estações  totais,
aliada  à  possibilidade  de  processamento  automatizado  de  um  grande  volume  de
dados, a triangulateração, quando comparada com a trilateração e triangulação,
se  destaca  por  possibilitar  uma  melhor  precisão  e  melhor  análise  estatística  das
observações   e   das   coordenadas,   tendo   em   vista   o   elevado   número   de
observações redundantes.

## Figura 9 – Triangulateração
## 3.5 IRRADIAÇÃO
O  método  da  irradiação  se  baseia  na  determinação  de  coordenadas  a  partir  da
observação de ângulos e distâncias ou azimutes e distâncias.
A  determinação  de  coordenadas  do  ponto  de  interesse  é  realizada  a  partir  da
observação  da  distância  entre  um  dos  vértices  conhecidos  até  o  vértice  de
interesse,  bem  como  do  ângulo  formado  entre  o  alinhamento  do  vértice  de
interesse e o alinhamento dos vértices conhecidos (Figura 10).

Figura 10 – Irradiação observando ângulo e distância
## B
## C
## A
## D
## F
## E
## 1
## 2
## 5
## 6
## 7
## 8
## 13
## 14
## 18
## 17
## 12
## 11
## 10
## 9
## 4
## 3
## G
## H
## 22
## 21
## 15
## 16
## 19
## 20
## 24
## 23
d
## AC
d
## AD
d
## BC
d
## BD
d
## DC
d
## CF
d
## CE
d
## DE
d
## DF
d
## FE
d
## EH
d
## FG
d
## EG
d
## FH
## A
## B
## 1
## B
d
## B1

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 18
Também  pode  ser  realizada  a  determinação  por  irradiação  nos  casos  em  que  se
observa diretamente o azimute da direção estabelecida entre o vértice conhecido
e o vértice de interesse (Figura 11).

Figura 11 – Irradiação observando azimute e distância
Os   vértices   de   coordenadas   conhecidas   podem   ser   os   vértices   de   apoio   à
topografia  clássica  ou  vértices  de  desenvolvimento  de  poligonais,  triangulações,
trilaterações e triangulaterações. Quando for possível é aconselhável que o vértice
de interesse seja “irradiado” de mais de um vértice de referência, permitindo assim
o ajustamento de observações (Figura 12).

Figura 12 – Irradiação com observações redundantes
## 3.6 INTERSEÇÃO LINEAR
A  determinação  de  coordenadas,  por  meio  do  método  de  interseção  linear,  é
realizada  a  partir  da  observação  das distâncias  do  ponto  de  interesse  a  dois
vértices de coordenadas conhecidas (Figura 13).
## A
## 1
## Az
## A1
## N
d
## A1
## A
## B
## 1
## B
d
## B1
d
## A1
## A

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 19

Figura 13 – Interseção linear
## 3.7 INTERSEÇÃO ANGULAR
A interseção  angular  é  realizada  quando  se  observa  somente  os  ângulos  entre  os
alinhamentos  formados  por  dois  vértices  de  coordenadas  conhecidas  e  o  vértice
de interesse (Figura 14).

Figura 14 – Interseção angular
É  interessante  utilizar  esse  método  para  posicionar  vértices  situados  em  locais
inacessíveis,   onde   é   possível   a   observação   precisa   dos   ângulos   entre   os
alinhamentos.
## 3.8 ALINHAMENTO
O  método  do  alinhamento  consiste  na  determinação  de  coordenadas  de  um
vértice  que  se  encontra  na  direção  definida  por  outros  dois  de  coordenadas
conhecidas  (Figura 15).    A  única  observação  necessária  é  à  distância  de  um  dos
vértices conhecidos até o vértice de interesse.
## A
## B
## 1
d
## B1
d
## A1
## A
## B
## 1
## B
## A

3 Posicionamento por Topografia Clássica

Manual Técnico de Posicionamento                                                                              Página: 20

## Figura 15 – Alinhamento
Recomenda-se a utilização desse método para determinação de vértices em locais
onde existem obstruções físicas que impeçam o levantamento por métodos GNSS. É
uma   alternativa   à  utilização  de   outros  métodos   por   topografia   clássica,   pois
dispensa o uso de estação total, sendo necessária apenas uma trena.
## A
## B
## 1
## A
## B
## 1
d
## B1
d
## B1

4 Posicionamento por Geometria Analítica

Manual Técnico de Posicionamento                                                                              Página: 21
## 4 POSICIONAMENTO POR GEOMETRIA ANALÍTICA
O  posicionamento  por  geometria  analítica  se  dá  de  forma  indireta,  onde  as
coordenadas   são   determinadas   por   cálculos   analíticos   a   partir   de   vértices
posicionados de forma direta.
Para minimizar a distorção nos valores de área, distância e azimute, é fundamental
que  o  valor  de  altitude  seja  atribuído  a  cada  um  dos  vértices  obtidos  a  partir  de
posicionamento por geometria analítica. Na impossibilidade de obter esses valores,
deverá  ser  atribuído  a  cada  um  o  valor  da  altitude  média  dos  vértices  utilizados
como referência para essa determinação.
Nos próximos tópicos é feita uma breve descrição sobre cada um dos métodos de
posicionamento por geometria analítica, aplicados aos serviços de
georreferenciamento de imóveis rurais.
## 4.1 PARALELA
O  método  da  paralela  consiste  na  determinação  de  coordenadas  de  vértices  a
partir de uma linha paralela a outra que teve seus vértices determinados por algum
outro  método  de  posicionamento.  É  necessário  definir  a  distância  de  afastamento
entre as linhas (Figura 16).

## Figura 16 – Paralela
## 4.2 INTERSEÇÃO DE RETAS
As  coordenadas  do vértice  de  interesse  são  determinadas  pela  interseção  de  dois
segmentos  de  retas  cujos  vértices  são  determinados  de  forma  direta.  A Figura 17
ilustra três possibilidades de interseção entre retas.
## A'
## B'
## C'
## D'
## E'
## F'
## A
## B
## C
## D
## E
## F
d

4 Posicionamento por Geometria Analítica

Manual Técnico de Posicionamento                                                                              Página: 22

Figura 17 – Três possibilidades de interseção de retas
## A
## B
## 1
## D
## C
## A
## B
## 1
## D
## C
## A
## B
## 1
## D
## C

5 Posicionamento por Sensoriamento Remoto

Manual Técnico de Posicionamento                                                                              Página: 23
## 5 POSICIONAMENTO POR SENSORIAMENTO REMOTO
No  posicionamento  por sensoriamento  remoto,  obtêm-se  informações geométricas
de    elementos    físicos,    de    forma    indireta,    com    precisão    e    confiabilidade
devidamente avaliadas, a partir de sensores em nível orbital ou aerotransportados.
Dentre   as   possibilidades   de   posicionamento   por   sensoriamento   remoto,   são
aplicados  aos  serviços  de  georreferenciamento  de  imóveis  rurais  os  seguintes
métodos:
a) Aerofotogrametria;
b) Radar aerotransportado;
c) Laser scanner aerotransportado; e
d) Sensores orbitais (satélites).
Os valores de coordenadas dos vértices obtidos por sensoriamento remoto poderão
ser  adquiridos  de  órgão  público,  empresa  pública  ou  privada  ou  produzidos  pelo
próprio credenciado. Todos estes com especialização na área de conhecimento e
devidamente  habilitados  para  este  fim  no  Conselho  Regional  de  Engenharia  e
Agronomia (CREA).
Quando  da  utilização  de  produtos  obtidos através  de  aerofotogrametria,  radar  ou
laser    scanner aerotransportados,    além    da    especialização    e    habilitação
supramencionadas, deve-se estar devidamente habilitado pelo Ministério da Defesa
e possuir homologação da Agência Nacional de Aviação Civil (ANAC).
Não  se  aplica  o  posicionamento  por  sensoriamento  remoto  na  determinação  de
vértices tipo “M”, vértices em limites por cerca e vértices referentes a mudanças de
confrontação.  Nos  demais  tipos  de  limite  o credenciado  deverá cercar-se  das
precauções necessárias em relação ao produto utilizado, de forma que garanta a
precisão posicional definida pela NTGIR 3ª Edição.

IMPORTANTE: “Não se aplica o posicionamento por sensoriamento remoto na
determinação  de  vértices  tipo  “M”,  vértices  em  limites  por  cerca  e  vértices
referentes a mudanças de confrontação”.


## 6 Base Cartográfica

Manual Técnico de Posicionamento                                                                              Página: 24
## 6 BASE CARTOGRÁFICA
Base  cartográfica  é  uma  fonte  de  informações  espaciais,  destinada  a  um  fim
específico.
Somente  poderão  ser  utilizadas  bases cartográficas  originalmente  nos  formatos
raster ou vetorial, ou seja, fica vedada a utilização de bases cartográficas em meio
analógico ou digitalizadas.
Ao  obter  informações  posicionais  a  partir  de  base  cartográfica,  o  credenciado
deverá  verificar  qual  método  de  posicionamento  foi  usado  para  a  representação
do elemento de interesse e assim associá-lo ao vértice em questão.
O método e a precisão posicional
## 1
definirão a sua aplicação de acordo com o tipo
de  limite,  conforme  resumido  no Quadro 3,  não  sendo  permitida  a  utilização  de
base cartográfica para o posicionamento de vértices tipo “M” (marco).

## 1
Na impossibilidade de identificação do método de posicionamento usado na feição de interesse, considera-se o
valor de precisão aquele correspondente à escala de representação do produto cartográfico.

7 Aplicação dos Métodos de Posicionamento

Manual Técnico de Posicionamento                                                                              Página: 25
## 7 APLICAÇÃO DOS MÉTODOS DE POSICIONAMENTO
Os   vários   métodos   de   posicionamento   apresentados,   juntamente   com   as
características  técnicas  utilizadas  para  sua  execução, devem  garantir  a  precisão
posicional  de  acordo  com  a  aplicação  do  vértice. Os  itens  a  seguir  contêm  os
métodos de posicionamento que podem ser utilizados em diferentes situações.
## 7.1 VÉRTICES DE APOIO
Dependendo  do  método  de  posicionamento  a  ser  usado  para  determinação  de
coordenadas  dos  vértices  de  limite,  há  necessidade  de  se  apoiar  em  vértices  de
coordenadas  conhecidas,  tais  vértices  são  denominados  como: apoio, controle,
referência ou base.
Os  vértices  de  apoio  para  determinação  das  coordenadas  dos  vértices  de  limite
podem ser aqueles que compõem o Sistema Geodésico Brasileiro
## 2
(SGB) ou vértices
cujas  coordenadas  foram  determinadas  a  partir  de  vértices  do  SGB.  Neste  último
caso, os métodos de posicionamento que poderão ser usados na determinação de
coordenadas de vértices de apoio, estão definidos no Quadro 2.
Quadro 2 – Métodos de posicionamento para vértices de apoio
Código Método de Posicionamento
PG1 Relativo estático
PG2 Relativo estático-rápido
PG6 RTK convencional
PG7 RTK em rede
PG9 Posicionamento por Ponto Preciso
PT1 Poligonação
PT2 Triangulação
PT3 Trilateração
PT4 Triangulateração
## 7.2 VÉRTICES DE LIMITE
A  NTGIR  3ª  Edição,  define  diferentes  padrões  de  precisão  de  acordo  com  os  tipos
de limites: artificiais (melhor ou igual a 0,50 m), naturais (melhor ou igual a 3,00 m) e
inacessíveis (melhor ou igual a 7,50 m).

## 2
Somente  poderão  ser  usados  vértices  do  SGB  referentes  às estações  SAT  GPS  (ativas  ou  passivas).  Informações
destas estações podem ser obtidas em: http://www.ibge.gov.br/home/geociencias/geodesia/sgb.shtm.

7 Aplicação dos Métodos de Posicionamento

Manual Técnico de Posicionamento                                                                              Página: 26
Em função do padrão de precisão, os métodos de posicionamento podem ou não
ser  aplicados  a  determinado  tipo  de  limite.  No Quadro 3 temos  o  resumo  dos
métodos  de  posicionamento,  contendo  os  códigos  atribuídos  a  cada  método,  e
em quais tipos de limites eles podem ser usados.
Quadro 3 – Métodos de posicionamento para vértices de limite
Código Método de Posicionamento Aplicação
PG1 Relativo estático Limite Artificial ou Natural
PG2 Relativo estático-rápido Limite Artificial ou Natural
PG3 Relativo semicinemático Limite Artificial ou Natural
PG4 Relativo cinemático Limite Artificial ou Natural
PG5 Relativo a partir do código C/A Limite Natural
PG6 RTK convencional Limite Artificial ou Natural
PG7 RTK em rede Limite Artificial ou Natural
PG8 Differential GPS (DGPS) Limite Natural
PG9 Posicionamento por Ponto Preciso Limite Artificial ou Natural
PT1 Poligonação Limite Artificial ou Natural
PT2 Triangulação Limite Artificial ou Natural
PT3 Trilateração Limite Artificial ou Natural
PT4 Triangulateração Limite Artificial ou Natural
PT5 Irradiação Limite Artificial ou Natural
PT6 Interseção linear Limite Artificial ou Natural
PT7 Interseção angular Limite Artificial ou Natural
PT8 Alinhamento Limite Artificial ou Natural
PA1 Paralela Limite Artificial ou Natural
PA2 Interseção de Retas Limite Artificial ou Natural
PS1 Aerofotogrametria Limite Artificial
## 3
, Natural ou Inacessível
PS2 Radar aerotransportado Limite Artificial
## 3
, Natural ou Inacessível
PS3 Laser scanner aerotransportado Limite Artificial
## 3
, Natural ou Inacessível
PS4 Sensores orbitais Limite Artificial
## 3
, Natural ou Inacessível

## 3
Com exceção de vértices tipo M e limites por cerca.

8 Métodos de Posicionamento e Tipos de Vértices

Manual Técnico de Posicionamento                                                                              Página: 27
## 8 MÉTODOS DE POSICIONAMENTO E TIPOS DE VÉRTICES
Os  tipos  de  vértices  são  definidos  em  função  da  sua  caracterização  em  campo  e
da  forma  de  posicionamento  (direto ou  indireto),  conforme  definições  constantes
do Manual Técnico de Limites e Confrontações.
Entende-se  como  posicionamento  direto  aquele  em  que  se  ocupa  diretamente  o
vértice  de  interesse  com  um  instrumento  de  medição  e  o  posicionamento  indireto
aquele  em que  não  há  ocupação  direta  do  vértice  por  um  instrumento  de
medição.
No Quadro 4 tem-se  a  relação  entre  método  de  posicionamento  e  os  tipos  de
vértices compatíveis.
Quadro 4 – Métodos de posicionamento e tipos de vértices
Código Método de Posicionamento Tipo de Vértice
PG1 Relativo estático M,P
PG2 Relativo estático-rápido M,P
PG3 Relativo semicinemático M,P
PG4 Relativo cinemático  P
PG5 Relativo a partir do código C/A P
PG6 RTK convencional M,P
PG7 RTK em rede M,P
PG8 Differential GPS (DGPS) P
PG9 Posicionamento por Ponto Preciso M,P
PT1 Poligonação M,P
PT2 Triangulação M,P
PT3 Trilateração M,P
PT4 Triangulateração  M,P
PT5 Irradiação M,P
PT6 Interseção linear M,P,V
PT7 Interseção angular M,P,V
PT8 Alinhamento M,P
PA1 Paralela V
PA2 Interseção de Retas V
PS1 Aerofotogrametria V
PS2 Radar aerotransportado V
PS3 Laser scanner aerotransportado V
PS4 Sensores orbitais V

## 9 Cálculos

Manual Técnico de Posicionamento                                                                              Página: 28
## 9 CÁLCULOS
Este  capítulo  traz  as  formulações  matemáticas  para  conversão  de  coordenadas
geocêntricas para locais e para os valores das grandezas área, distância e azimute.
## 9.1 CONVERSÃO DE COORDENADAS CARTESIANAS GEOCÊNTRICAS PARA LOCAIS
A conversão de coordenadas cartesianas geocêntricas (X, Y, Z) para coordenadas
cartesianas locais (e, n, u) é feita por meio do método das rotações e translações,
conforme modelo funcional a seguir:
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## .
## 1
## 0
## 0
## 0
cos
## 0
cos
## .
cos
## 0
cos
## 0
## 0
## 0
## 1
## Z
## Z
## Y
## Y
## X
## X
sen
sen
sen
sen
u
n
e
## 
## 
## 
## 
## 
## 
## 
## 

## Onde:
 e, n, u = são as coordenadas cartesianas locais do vértice de interesse;
 X, Y, Z =  são  as  coordenadas  cartesianas geocêntricas do vértice de
interesse;
 φ
## 0
, λ
## 0
= são a latitude e a longitude adotadas como origem do sistema;
##  X
## 0
## , Y
## 0
## , Z
## 0
=  são  as  coordenadas  cartesianas  geocêntricas adotadas  como
origem do sistema.
As principais aplicações são:
a) Para o cálculo de área
O   cálculo   de   área   é   feito   com   as   coordenadas   cartesianas   locais
referenciadas    ao    SGL.    Deste    modo,    as    coordenadas    cartesianas
geocêntricas determinadas para os vértices do limite devem ser convertidas
para  o  SGL,  usando-se  a  média  das  coordenadas  da  parcela  em  questão
como origem do sistema.
b) No uso do método de posicionamento por geometria analítica
Na determinação de coordenadas por geometria analítica, as coordenadas
utilizadas  como  referência  para  os  cálculos  devem  estar  referenciadas  ao
SGL desta forma, caso tenham sido obtidas por posicionamento por GNSS as
mesmas   devem   ser   convertidas   para   coordenadas   cartesianas   locais,
usando  como  origem  a  média  das  coordenadas  dos  vértices  de  referência
(vértices ilustrados na cor preta – Figura 15 e Figura 16).

## 9 Cálculos

Manual Técnico de Posicionamento                                                                              Página: 29
c) Nos casos de projetos de parcelamento/desmembramento
Em     projetos     de     parcelamento/desmembramento,     as     coordenadas
cartesianas geocêntricas deverão ser convertidas para cartesianas locais (as
coordenadas  de  origem  do  SGL  deverão  ser  a  média  das  coordenadas
geocêntricas),  permitindo  a  elaboração  do  projeto  com  referência  nessas
coordenadas,   definindo   áreas   de   parcelas   bem   como   a   geração   de
vértices.
Concluído  o  projeto,  todas  as coordenadas  cartesianas  locais  deverão  ser
convertidas    para    cartesianas    geocêntricas,    devendo    utilizar    como
coordenada  de  origem  a  mesma  usada  no  parágrafo  anterior  (conforme
formulação matemática contida no item 9.2).
## 9.2 CONVERSÃO DE COORDENADAS CARTESIANAS LOCAIS PARA GEOCÊNTRICAS
A conversão de coordenadas cartesianas locais para coordenadas geocêntricas é
realizada conforme o seguinte modelo funcional:
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## 0
## .
cos
## 0
cos
## 0
## 0
## 0
## 1
## .
## 1
## 0
## 0
## 0
cos
## 0
cos
## Z
## Y
## X
u
n
e
sen
sen
sen
sen
## Z
## Y
## X
## 
## 
## 
## 
## 
## 
## 
## 

A  principal  aplicação  dessa  conversão  se  dá  quando  se  utiliza  métodos  de
posicionamento por topografia clássica
## 4
. A seguir será apresentada a sequência de
cálculos:
a) Determinar as coordenadas cartesianas geocêntricas dos vértices de apoio;
b) Converter  as  coordenadas  cartesianas  geocêntricas  dos  vértices  de  apoio
para  cartesianas  locais,  conforme  equação  expressa  no  item 9.1 e,  usando
como  origem do  sistema,  a  média  das  coordenadas  geocêntricas  destes
vértices;
c) De  posse  das  observações  topográficas  (ângulos  e  distância),  efetuar  o
cálculo     (processamento     e     ajustamento)     para     determinação     das
coordenadas cartesianas locais dos vértices;

## 4
Para fins desse manual, desconsideram-se as possíveis distorções acarretadas pela não coincidência entre o plano
topográfico  obtido  no  posicionamento  por  topografia  clássica  (perpendicular  à  vertical)  e  aquele  usado  no  SGL
(perpendicular à normal ao elipsoide).

## 9 Cálculos

Manual Técnico de Posicionamento                                                                              Página: 30
d) Converter  as coordenadas  cartesianas  locais  para  geocêntricas  conforme
equação expressa neste item e usar como origem do sistema o mesmo valor
de coordenadas do item b.
A Figura 18 ilustra  um  ponto  sobre  a  superfície  terrestre  associado  ao  Sistema
Geodésico Local (SGL) e ao Sistema Geocêntrico.

Figura 18 – Sistema Geodésico Local e Sistema Geocêntrico
## 9.3 ÁREA
O cálculo de área deve ser realizado com base nas coordenadas cartesianas locais
referenciadas  ao SGL. Desta  forma, os  resultados  obtidos  expressam  melhor  a
realidade  física
## 5
,  quando  comparados  aos  valores referenciados  ao Sistema  UTM,
que era adotado anteriormente.

## 5
As distorções nos valores de área se tornam maiores na medida em que as parcelas aumentam sua superfície.

## 9 Cálculos

Manual Técnico de Posicionamento                                                                              Página: 31
O  cálculo de  área deve  ser  realizado pela  fórmula  de  Gauss,  com  base  nas
coordenadas cartesianas locais (e, n, u) e expresso em hectares.
## 9.4 DISTÂNCIA HORIZONTAL
O  valor  da  distância  horizontal  deve  ser  expresso  em  metros.  O  cálculo  deve  ser
realizado conforme a seguinte equação:
## 2
## 2
## 2
## 2
## )
## (
## )
## (
## )
## (
## )
## (
## B
## A
## B
## A
## B
## A
## B
## A
h
h
h
## Z
## Z
## Y
## Y
## X
## X
d
## 
## 
## 
## 
## 
## 
## 
## 

## Onde:
 d
h
= distância horizontal;
 X, Y, Z = coordenadas cartesianas geocêntricas;
 h = altitude elipsoidal.
## 9.5 AZIMUTE
O   cálculo   de   azimute   deve   ser   realizado   conforme formulário   do   Problema
Geodésico  Inverso   segundo Puissant e   o   valor   deve   ser   expresso   no   sistema
sexagesimal.

10 Guarda de Peças Técnicas e Documentação

Manual Técnico de Posicionamento                                                                              Página: 32
## 10 GUARDA DE PEÇAS TÉCNICAS E DOCUMENTAÇÃO
Todo  o  material  utilizado  para  determinação  das  informações  posicionais  deve  ser
arquivado   e   mantido   sob   a   guarda   do   credenciado.   Faz-se   necessária   a
manutenção  desse  material  para  sanar  possíveis  dúvidas  ou  divergências  quanto
aos  valores  de  coordenadas  e  precisões  apresentados  pelo  credenciado.  Tais
informações poderão ser requeridas pelo INCRA, quando julgar necessário.
Dentre os materiais utilizados, devem ser considerados:
a) Arquivos brutos GNSS (em formato RINEX e nativo);
b) Relatórios de processamento e ajustamento de posicionamento por GNSS;
c) Cadernetas de campo (digitais ou analógicas);
d) Relatórios  de  processamento  e  ajustamento  de  dados  de  posicionamento
por topografia clássica;
e) Imagens orbitais e/ou aéreas;
f) Relatório  de  processamento  e  ajustamento  de  imagens.  Contendo  modelo
digital do terreno, pontos de controle, dentre outros;
g) Anotação  de  responsabilidade técnica  da  empresa  executora  do  trabalho
de sensoriamento remoto, caso não tenha sido o credenciado o responsável
técnico;
h) Base cartográfica.

## Referências

Manual Técnico de Posicionamento                                                                              Página: 33
## REFERÊNCIAS
ALVES, D. B. M.; MÔNICO, J. F. G. e FORTES, L. P. S. Modelagem da Ionosfera no RTK
em Rede. Anais do XXII Congresso Brasileiro de Cartografia, Macaé, 2005.
CUNHA,  R.  S.  e  RODRIGUES,  D.  D. Proposta  de  um  Novo  Modelo  de  Memorial
Descritivo  (INCRA)  para  Atender  a  Lei  10.267.  2007.  Monografia  (Graduação  em
Engenharia  de  Agrimensura) – Curso  de  Engenharia  de  Agrimensura,  Universidade
Federal de Viçosa, Viçosa, 2007.
DAL’FORNO,  G.  L.;  AGUIRRE,  A.  J.;  HILLEBRAND,  F.  L.  e  GREGÓRIO,  F.  V.
Transformação    de    Coordenadas    Geodésicas    em Coordenadas    no    Plano
Topográfico  Local  pelo  Métodos  da  Norma  NBR  14166:1998  e  o  de  Rotações  e
Translações. Anais do III Simpósio Brasileiro de Ciências Geodésicas e Tecnologias da
## Geoinformação, Recife, 2010.
IBGE.  Fundação  Instituto  Brasileiro  de  Geografia  e  Estatística. Manual  do  Usuário
Posicionamento por Ponto Preciso. Rio de Janeiro: IBGE, 2009.
IBGE. Fundação Instituto Brasileiro de Geografia e Estatística. Recomendações para
Levantamentos Relativos Estáticos – GPS. Rio de Janeiro: IBGE, 2008.
GEMAEL, C. Geodésia Celeste. Editora UFPR, 2004.
HOFMANN-WELLENHOF, B.; LICHTENEGGER, H. e WASLE, E. GNSS – Global Navigation
Satellite  Systems,  GPS,  GLONASS,  Galileo  and  more.  Springer-Verlag  Wien,  2008.
## 501p.
JEKELI,  C. Geometric  Reference  Systems  in  Geodesy.  Division  of  Geodesy  and
Geospatial Science, School of Earth Sciences, Ohio State University, 202p. 2006.
LEICK, A. GPS Satellite Surveying. 3. ed., New York: John Wiley & Sons, Inc, 2004.
MONICO,  J.  F.  G. Posicionamento  pelo  NAVSTAR-GPS:  descrição, fundamentos  e
aplicações. 1ª ed. São Paulo: Unesp, 2000a. 287p.
MONICO, J. F. G. Posicionamento pelo GNSS: descrição, fundamentos e aplicações.
2ª ed. São Paulo: Unesp, 2008. 473p.
MORAES, C. V.; SAATKAMP e E. D. E FREIBERGER J. Geodésia e Topografia. Notas de
Aula. Universidade Federal de Santa Maria, 2011. 107p.
POLEZEL  W.  G.  C.;  SOUZA  E.  M.  e  MONICO  J.  F.  G. Método  de  Posicionamento
Relativo por  Satélite  GPS  com  Correção do Efeito  do  Multicaminho  em  Estações de

## Referências

Manual Técnico de Posicionamento                                                                              Página: 34
Referência:   Formulação   Matemática,   Resultados   e   Análises. Tendências   em
Matemática Aplicada e Computacional. V.9, p. 133-142, 2008.
RODRIGUES,   D.   D. Topografia:   planimetria   para   Engenheiros   Agrimensores   e
Cartógrafos. Notas de Aula. Universidade Federal de Viçosa, 2008. 160p.
