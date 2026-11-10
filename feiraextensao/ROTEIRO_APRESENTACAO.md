# 🎤 Roteiro de apresentação — Feira de Extensão

Guia para apresentar o site para **pessoas leigas** (estudantes, pais, visitantes).
Regra de ouro: **mostre primeiro, explique depois.** Ninguém precisa saber o que é "POS Tagging" para entender o rio.

---

## 💡 A ideia em uma frase

> "Pro computador, «eu **rio**» e «o **rio**» são a mesma palavra. A gente mostra como ele descobre a diferença
> olhando as palavras em volta — e por que isso faz o Google achar o que você procurou."

Se o visitante só ouvir isso, já valeu.

---

## ✅ Antes da feira

- [ ] Rodar `streamlit run feiraextensao/app.py` **em casa** e **no notebook da feira**, com internet (na primeira vez ele baixa arquivos do NLTK).
- [ ] Zoom do navegador em **125–150%** (as pessoas vão estar em pé, longe da tela).
- [ ] Deixar aberto na aba **🔍 Raio-X da Frase**, com o exemplo do rio.
- [ ] Combinar quem **fala** e quem **clica** (ver no fim).
- [ ] Entre um grupo e outro do quiz: clicar em **🔄 Recomeçar**.

---

## 🎬 Abertura (30 segundos)

Pergunte, sem mostrar a tela ainda:

> "Rapidinho: na frase *'Eu rio demais, mesmo morando perto do rio'*, as duas palavras «rio» são iguais?"

A pessoa vai dizer que não (uma é rir, outra é o rio). Aí você completa:

> "Pra você é óbvio. Pro computador, são só as letras r-i-o. Olha como ele resolve isso."

E vira a tela.

---

## ⏱️ Versão curta (2–3 min) — para a maioria dos visitantes

### 1. Raio-X da Frase (1 min)

**O que já está na tela:** a frase do rio, com um cartão colorido para cada palavra.

**Aponte para os dois «rio»:**
- o primeiro está **vermelho (Verbo)** e embaixo aparece **→ rir**
- o segundo está **azul (Substantivo)**
- os dois têm a etiqueta amarela **⚡ Ambígua**

**O que falar:**
> "O computador olhou a palavra **antes**. Depois de «eu», só pode ser uma ação: é o verbo *rir*.
> Depois de «do», é uma coisa: é o rio. É exatamente o que a gente faz sem perceber."

### 2. Buscador (1–2 min) — o momento "uau"

Vá na aba **🚀 Buscador** e clique em **🔍 Eu rio muito com vídeos**.

**O que aparece:**

| ⚠️ Sem POS (esquerda) | ✅ Com POS (direita) |
|---|---|
| Stand-up e memes ✔️ | Stand-up e memes ✔️ |
| **Expedição no Rio Paraná** ❌ | — |
| **Jogo de mundo aberto** ❌ (só porque tem a palavra «com») | — |

**O que falar:**
> "Eu pesquisei sobre **rir de vídeos**. O buscador da esquerda só compara letras — me trouxe um texto
> sobre **caiaque no rio**. O da direita sabe que meu «rio» é verbo, então só traz o texto certo.
> E ainda achou «riu» e «rir», que são o mesmo verbo escrito diferente."

Feche com:
> "É isso que o Google e as IAs fazem o tempo todo: entender **o papel** de cada palavra, não só as letras."

---

## 🕐 Versão completa (5–7 min) — para quem quer saber mais

Faça a versão curta e acrescente:

### 3. Palavras Gêmeas
Escolha **🎤 canto** ou **💳 banco** na lista. Mostra a mesma palavra em duas frases, lado a lado.

> "«Eu **canto** na banda» é cantar. «No **canto** do quarto» é um lugar. Mesma palavra, sentido diferente."

Depois peça para a **própria pessoa digitar** no campo "🧪 Sua vez" uma frase com os dois sentidos.
Deixar o visitante digitar é o que mais prende a atenção.

### 4. Desafio: Você vs. IA
Ótimo para **grupos de estudantes** — vira competição. São 6 perguntas, 10 pontos cada.

> "Agora é você contra a máquina: qual é a classe dessa palavra?"

A pergunta da gíria (**«tankou»**) costuma render conversa:
> "«Tankar» não está no dicionário, mas o computador acertou mesmo assim — pela terminação «-ou», igual «jogou» e «ganhou»."

### 5. Por Trás do Código
**Só para quem pedir** (professores, alunos de computação). Mostra o passo a passo e uma tabela técnica.

---

## 🗣️ Como traduzir os termos técnicos

| Termo técnico | Como falar com o público |
|---|---|
| POS Tagging | "Descobrir a **classe gramatical** de cada palavra — aquilo de verbo e substantivo da escola." |
| Ambiguidade / homógrafo | "Palavras **gêmeas**: mesma escrita, sentido diferente." |
| Lema / lematização | "A forma de **dicionário** da palavra: «riu», «rindo», «rio» → **rir**." |
| Stemmer | "Uma **tesoura** que corta o final da palavra sem saber o que ela significa." |
| Stop words | "Palavras de **ligação** («o», «de», «com») que aparecem em todo texto e não ajudam a diferenciar nada." |
| Índice invertido | "O **índice remissivo** do final do livro: para cada palavra, em que páginas ela aparece." |
| Contexto | "As palavras **em volta**." |

---

## ❓ Perguntas que vão aparecer

**"Isso é tipo o ChatGPT?"**
> "É uma peça bem menor da mesma área. O ChatGPT aprendeu a entender contexto sozinho, lendo muito texto.
> Aqui a gente mostra esse mesmo problema — o sentido depende das palavras em volta — de um jeito que dá pra ver."

**"Como o computador sabe a classe?"**
> "Ele foi treinado com milhares de frases em português que pessoas etiquetaram à mão. Ele aprendeu os padrões:
> depois de «o» geralmente vem substantivo, depois de «eu» geralmente vem verbo. Para as palavras gêmeas,
> a gente também escreveu regras próprias."

**"Ele erra?"**
> "Erra, sim! Principalmente com frases bem diferentes das que a gente testou. Quer tentar achar um erro?"
(Transformar o erro em brincadeira funciona muito bem — ver abaixo.)

**"Pra que serve na vida real?"**
> "Busca no Google e em lojas online, corretor do celular, tradutores, assistentes de voz como a Alexa,
> e empresas que analisam o que as pessoas falam nas redes."

**"Por que jogar fora «o», «de», «com»?"**
> "Porque estão em todo texto. Se o buscador usasse «com», ele traria quase tudo — foi o que aconteceu
> com aquele texto de games no exemplo do rio."

---

## 🛟 Se algo der errado

- **O computador errou a classe de uma palavra que o visitante digitou:**
  > "Boa, você achou um erro! Ele decide olhando principalmente a palavra de antes, e nessa frase isso não bastou.
  > É por isso que esse ainda é um problema estudado na universidade."
- **O site demorou na primeira vez:** normal, ele carrega o modelo de português uma vez só. Depois fica rápido.
- **A pessoa não entendeu nada:** volte à pergunta da abertura (os dois «rio»). É o exemplo mais claro.

---

## 👥 Dividindo entre os dois

| Quem fala | Quem clica |
|---|---|
| Faz a pergunta de abertura, explica, responde dúvidas | Opera o notebook, clica nos exemplos, digita as frases dos visitantes |

Quando chegar um grupo grande: um faz o **Desafio** com o grupo enquanto o outro atende quem chegou depois na versão curta.

---

## 📌 Cola rápida: exemplos que funcionam bem

| Aba | Clique / digite | Mostra |
|---|---|---|
| Raio-X | 😂 eu rio × do rio | dois «rio» com classes diferentes |
| Raio-X | ⚡ gíria: tankou | gíria reconhecida como verbo (`tankar`) |
| Buscador | Eu rio muito com vídeos | esquerda traz o texto do rio ❌, direita não ✅ |
| Buscador | Mesa no canto da parede | esquerda traz o texto de cantar ❌, direita só o do quarto ✅ |
| Buscador | Abrir conta no banco digital | esquerda traz o "eu banco o lanche" ❌, direita só o do banco digital ✅ |
| Palavras Gêmeas | 🎤 canto | cantar × lugar, lado a lado |
