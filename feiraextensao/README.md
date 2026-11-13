# part-0f-Speech Tagging — Feira de Extensão (SCC0282)

Projeto da disciplina **SCC0282 — Recuperação de Informação**, apresentado na **Feira de Extensão em 10/11, das 16h às 17h**.

A ferramenta demonstra, de forma interativa, como a etiquetagem gramatical (*Part-of-Speech Tagging*, ou POS Tagging) ajuda a analisar textos em português e a melhorar a recuperação de informação. Por exemplo, identifica a diferença entre **“eu rio”** (verbo *rir*) e **“o rio”** (substantivo).

**Integrantes:** Ana Paula de Abreu Batista (nº USP 12688424) · Italo Carlos Martins Bresciani (nº USP 15461782)

## Sobre o trabalho

A partir de uma palavra ou sentença, o sistema realiza o pré-processamento do texto — tokenização, normalização e segmentação — e infere a classe gramatical de cada termo, como substantivo, verbo, adjetivo ou preposição. A aplicação utiliza o spaCy com o modelo `pt_core_news_sm`, complementado por regras de contexto para alguns casos ambíguos. Como resultado, apresenta os pares **termo–classe** e informações como lema, radical e identificação de stop words.

## Relação com Recuperação de Informação

A análise morfológica integra o pipeline de pré-processamento e indexação em Recuperação de Informação. Em sistemas tradicionais, o texto passa por etapas como remoção de stop words, stemming e lematização antes da construção de índices invertidos. A identificação da classe gramatical pode contribuir para:

- **Lematização contextualizada:** distinguir usos diferentes de uma mesma forma — como o verbo “rio” e o substantivo “rio” — e reduzir termos à forma base adequada.
- **Filtragem seletiva de termos:** identificar palavras funcionais para descarte e preservar termos com maior carga semântica, como substantivos e verbos.
- **Desambiguação:** considerar a função gramatical das palavras em documentos e consultas, contribuindo para resultados de busca mais precisos.

---

## Como executar

```bash
pip install -r feiraextensao/requirements.txt
streamlit run feiraextensao/app.py
```

As dependências incluem Streamlit, spaCy, NLTK e o modelo de português `pt_core_news_sm`. Na primeira execução, o NLTK baixa o stemmer RSLP e a lista de stop words; é necessário acesso à internet.

## Estrutura principal

| Arquivo | Responsabilidade |
|---|---|
| `feiraextensao/nlp_engine.py` | Analisa frases, classifica tokens e executa as buscas. |
| `feiraextensao/app.py` | Apresenta a interface interativa em Streamlit. |

O motor disponibiliza `analisar_frase(frase)`, `buscar_documentos(consulta)`, `POS_INFO` e a estrutura `TokenAnalisado`.

## Pipeline de análise

Exemplo: **“Eu rio demais, mesmo morando perto do rio!”**

1. O spaCy tokeniza a frase e atribui uma classe gramatical no padrão Universal Dependencies (UPOS).
2. Regras de contexto ajustam alguns casos ambíguos, considerando palavras próximas, e reconhecem gírias cadastradas.
3. O sistema determina o lema e calcula também o radical pelo stemmer RSLP.
4. Os tokens são marcados conforme a lista de stop words.

Cada token analisado inclui o texto original e normalizado, a classe atribuída, a classe UPOS do spaCy, o lema, o radical, a indicação de stop word e, quando aplicável, uma explicação da pista de contexto usada.

> **Limitação:** a desambiguação de palavras ambíguas usa regras definidas manualmente sobre a palavra anterior, em conjunto com o spaCy. As regras atendem aos exemplos da aplicação, mas podem classificar incorretamente frases fora desses contextos.

## Buscador demonstrativo

A aplicação compara uma coleção de oito textos com a consulta digitada. A consulta e os documentos são analisados pelo mesmo pipeline, e os resultados são comparados de duas formas:

| Método | Critério de comparação |
|---|---|
| Sem POS Tagging | Palavra igual ou mesmo radical do stemmer. |
| Com POS Tagging | Mesmo par de lema e classe gramatical. |

Por exemplo, a busca por **“Eu rio muito”** pode encontrar tanto um texto sobre rir quanto um texto sobre o curso d’água quando não usa POS Tagging. Com a classificação, a busca compara lema e classe, reduzindo essa ambiguidade. Os resultados são ordenados pela quantidade de correspondências.

## Seções da aplicação

1. **Raio-X da Frase:** mostra a análise de cada palavra e as informações que o buscador utiliza.
2. **Palavras Gêmeas:** compara usos distintos da mesma palavra, incluindo lema e radical.
3. **Buscador:** compara os resultados com e sem POS Tagging.
4. **Desafio:** quiz sobre classes gramaticais.
5. **Por Trás do Código:** apresenta o pipeline e informações linguísticas dos tokens.

## Personalização

- Palavras ambíguas e regras de análise: `feiraextensao/nlp_engine.py`.
- Textos usados pelo buscador: `COLECAO_DOCUMENTOS` em `feiraextensao/nlp_engine.py`.
- Cores, ícones e nomes das classes: `POS_INFO` em `feiraextensao/nlp_engine.py`.
- Exemplos, perguntas do quiz e consultas demonstrativas: `feiraextensao/app.py`.
