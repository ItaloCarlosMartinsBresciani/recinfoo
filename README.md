# recinfoo

Projeto desenvolvido para a disciplina **SCC0282 — Recuperação de Informação**.

## Part-of-Speech Tagging

O trabalho consiste no desenvolvimento de uma ferramenta de etiquetagem morfossintática (*Part-of-Speech Tagging*, ou POS Tagging) para sentenças em linguagem natural. A partir de um texto de entrada — palavra ou sentença — o sistema realiza etapas de pré-processamento, como tokenização, normalização e segmentação, e infere a classe gramatical de cada termo, por exemplo, substantivo, verbo, adjetivo ou preposição.

A ferramenta gera como saída pares **termo–classe**, que podem subsidiar etapas posteriores de análise linguística e estruturação textual.

## Relação com Recuperação de Informação

A análise morfológica está diretamente relacionada ao pré-processamento e à indexação em Recuperação de Informação. Em modelos tradicionais de RI, o texto passa por etapas como remoção de *stop words*, *stemming* e lematização para a construção de índices invertidos eficientes. A classificação morfológica pode contribuir para:

- **Lematização contextualizada:** diferenciar usos de uma palavra conforme sua classe gramatical, reduzindo os termos à forma base adequada e evitando ruído léxico.
- **Filtragem seletiva de termos:** identificar palavras funcionais para descarte, mantendo termos com maior carga semântica, como substantivos e verbos.
- **Redução de polissemia e desambiguação:** considerar a função gramatical dos termos em documentos e consultas, contribuindo para melhorar a precisão da recuperação.

## Integrantes

- Ana Paula de Abreu Batista — nº USP 12688424
- Italo Carlos Martins Bresciani — nº USP 15461782

## Feira de Extensão

O projeto foi apresentado na Feira de Extensão no dia **10/11, das 16h às 17h**.

## Projeto da feira

A implementação da demonstração interativa está na pasta [`feiraextensao/`](feiraextensao/). Para instruções de execução e detalhes sobre a aplicação, consulte o [README do projeto da feira](feiraextensao/README.md).
