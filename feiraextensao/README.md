# ⚡ Como o Google e as IAs entendem o português? — Feira de Extensão (SCC0282)

Site interativo em **Streamlit** que mostra para estudantes do Ensino Médio como a **etiquetagem gramatical
(POS Tagging)** ajuda um buscador a diferenciar palavras iguais com sentidos diferentes
(ex.: «eu **rio**» = verbo *rir* × «o **rio**» = curso d'água).

**Integrantes:** Ana Paula de Abreu Batista (nº USP 12688424) · Italo Carlos Martins Bresciani (nº USP 15461782)

---

## 🚀 Como rodar

```powershell
pip install -r feiraextensao/requirements.txt   # instala streamlit, spacy, nltk e o modelo pt_core_news_sm
streamlit run feiraextensao/app.py
```

Na primeira execução o NLTK baixa sozinho o stemmer RSLP e a lista de stop words (precisa de internet).

---

## 📁 Os dois arquivos

| Arquivo | Papel | Pense nele como… |
|---|---|---|
| `nlp_engine.py` | Analisa frases e faz a busca. Não sabe nada de tela. | o **cérebro** |
| `app.py` | Desenha as 5 abas e chama as funções do motor. | a **tela** |

O `app.py` só usa 4 coisas do motor:

- `analisar_frase(frase)` → lista de `TokenAnalisado` (uma por palavra)
- `buscar_documentos(consulta)` → resultados dos dois buscadores
- `POS_INFO` → nome, ícone e cores de cada classe
- `TokenAnalisado` → o "molde" de cada palavra analisada

---

## 🧠 Como uma frase é analisada (`analisar_frase`)

Exemplo: **"Eu rio demais, mesmo morando perto do rio!"**

```
frase
  │
  ▼
1. spaCy (pt_core_news_sm) ──► separa as palavras e dá a classe universal (UPOS)
  │                             Eu=PRON, rio=?, demais=ADV, ..., do=ADP, rio=?
  ▼
2. Regras de contexto ──────► corrigem o que o spaCy erra com frequência
  │                             • palavra gêmea depois de «o, no, do, esse, pelo...» → Substantivo
  │                             • palavra gêmea depois de «eu, ele, não, nunca...» → Verbo
  │                             • gírias (tankou, bugou, flopou...) → Verbo
  ▼
3. Forma base (lema) ───────► usa a classe para escolher a forma base
  │                             rio + Verbo → "rir"     rio + Substantivo → "rio"
  │                             (em paralelo calcula o radical do stemmer RSLP: "rio" nos dois casos)
  ▼
4. Stop word? ──────────────► pronomes, conectores e pontuação são marcados para descarte
  │
  ▼
lista de TokenAnalisado
```

Cada `TokenAnalisado` guarda:

| Campo | Exemplo para o 1º «rio» | Para que serve |
|---|---|---|
| `texto` / `normalizado` | `rio` / `rio` | palavra original e em minúsculas |
| `classe` | `VERB` | uma das classes simplificadas (SUB, VERB, ADJ, ADV, PRON, CON, NUM, PUNCT) |
| `upos_spacy` | `VERB` | classe "oficial" do padrão Universal Dependencies |
| `lema` | `rir` | forma base usada pelo buscador inteligente |
| `stem_nltk` | `rio` | radical cego (igual para os dois sentidos), usado pelo buscador sem POS |
| `eh_stopword` | `False` | se `True`, o buscador ignora a palavra |
| `eh_ambigua` | `True` | se é uma das palavras gêmeas de `PALAVRAS_AMB` |
| `pista_contexto` | "Precedida pelo sujeito «eu»…" | explicação mostrada no Raio-X |

> **Importante:** a desambiguação das palavras gêmeas é feita por **regras escritas à mão** (olhando a
> palavra anterior), em cima do spaCy. Funciona bem para os exemplos do site, mas frases muito diferentes
> podem receber a classe errada.

---

## 🔍 Como funciona o buscador (`buscar_documentos`)

A coleção são os 8 textos de `COLECAO_DOCUMENTOS` (stand-up, rio Paraná, canto, setup gamer, futebol,
jogo novo, banco digital, "eu banco o lanche"). A consulta e cada documento passam por `analisar_frase` e
depois são comparados de dois jeitos:

| | ⚠️ Sem POS Tagging | ✅ Com POS Tagging |
|---|---|---|
| Compara | palavra igual **ou** mesmo radical do stemmer | mesmo par **(lema, classe)** |
| "Eu rio muito" encontra | o texto do stand-up **e** o texto do rio Paraná ❌ | só o texto do stand-up (e acha «riu», «rir» também) ✅ |

A lista é ordenada pelo número de palavras que casaram.

---

## 🖥️ As 5 abas

1. **🔍 Raio-X da Frase** — o visitante digita uma frase e vê um cartão colorido por palavra, o que o buscador
   guardaria e (num expansor) por que cada palavra recebeu sua classe.
2. **🎭 Palavras Gêmeas** — a mesma palavra em duas frases, lado a lado, com a forma base certa × o radical do stemmer.
3. **🚀 Buscador** — compara os dois buscadores acima com consultas prontas ou digitadas.
4. **⚡ Desafio** — quiz de 6 perguntas (10 pontos cada) sobre a classe de uma palavra.
5. **⚙️ Por Trás do Código** — resumo do pipeline e uma tabela com UPOS, lema e radical de cada palavra.

A barra lateral é só a legenda das cores.

---

## ✏️ Onde mudar cada coisa

| Quero… | Mexer em |
|---|---|
| Adicionar uma palavra gêmea (ex.: «sonho») | `PALAVRAS_AMB` em `nlp_engine.py` |
| Ensinar uma gíria nova | lista de gírias dentro de `analisar_frase` (procure `"tankou"`) |
| Trocar/adicionar textos do buscador | `COLECAO_DOCUMENTOS` em `nlp_engine.py` |
| Trocar cores, ícones ou nomes das classes | `POS_INFO` em `nlp_engine.py` |
| Mudar os exemplos da aba Palavras Gêmeas | `CASOS_AMBIGUIDADE` em `app.py` |
| Mudar as perguntas do quiz | `QUESTOES_DESAFIO` em `app.py` |
| Mudar os botões de exemplo | `exemplos` (aba 1) e `consultas_demo` (aba 3) em `app.py` |
