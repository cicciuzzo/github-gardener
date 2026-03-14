# 🌱 github-gardener

**Due fuffaguru, un Raspberry Pi**

Questo repo è un progetto artistico di *vibecoding*: un Raspberry Pi 3 si sveglia a intervalli irregolari e genera una conversazione fittizia tra due guru italiani — **Maikol Pirozzi** (consulente strategico milanese, startup disruptive, pitch deck e digital transformation) e **Big Duca** (ha fatto i soldi a Dubai, vende corsi da 999€ sulla libertà finanziaria, passive income e crypto).

## Come funziona

- Un **timer systemd** lancia `gardener.py` ogni ~1h (±20 min di jitter)
- Un **modello probabilistico** (distribuzione Beta, correlazione di sessione, moltiplicatore giornaliero) decide se eseguire o saltare — simulando il pattern di attività di uno sviluppatore reale
- Se esegue, sceglie un'attività: **commit** (60%), **pull request** (15%), **code review** (15%), **issue** (10%)
- Ogni commit aggiunge una nuova battuta alla chat qui sotto, generata da Claude Haiku con il contesto delle ultime 10 risposte
- Minimo garantito: 2 interazioni al giorno grazie a un meccanismo di catch-up serale

## Stack

`Python 3` · `Claude Haiku` · `GitHub CLI` · `systemd` · `Raspberry Pi 3`

---

## 💬 La chat dei guru
<!-- entry -->

> **Big Duca**: Ragazzi vi dico una cosa: quando ero a Dubai ho capito che il cashflow non mente mai. La gente parla di passion economy ma il vero asset sei tu, il tuo mindset da milionario 💰🏙️ Nel mio corso da 997€ spiego tutto step by step

*2026-03-09 16:02*
<!-- entry -->

> **Maikol Pirozzi**: Duca rispetto il tuo hustle ma il vero play è buildare una startup con un go-to-market solido e fare un Series A entro 18 mesi. Il passive income è nice ma la scalability di un SaaS B2B è un altro deliverable proprio 📊🚀

*2026-03-09 16:41*
<!-- entry -->

> **Big Duca**: Ascolta fra, i numeri sono energia cristallizzata ma se non allinei il tuo chakra vibrazionale al true purpose, stai solo hackando il vuoto know what I mean? Flow > metrics, sempre 🌀✨

*2026-03-09 17:02*
<!-- entry -->

> **Maikol Pirozzi**: Flow è il risultato di un perfetto optimization loop, Big - quando trackhi bene i dati il tuo nervous system entra in uno stato di fluidità naturale. È scienza, non spiritualità bro 📈🧠

*2026-03-09 17:02*
<!-- entry -->

> **Big Duca**: Bro, la scienza è solo spiritualità che ancora non ha trovato il suo mantra - il tuo nervous system risponde all'intenzione, non al foglio Excel. L'universo non usa spreadsheet, usa frequenze 🌊✨

*2026-03-09 18:08*
<!-- entry -->

> **Maikol Pirozzi**: Ascolta Big, la frequenza è letteralmente un dato misurabile in hertz - gli spreadsheet sono il linguaggio dell'universo, il resto è storytelling. Torniamo a terra: hai mai fatto un cohort analysis? Quello sì che vibra 📊⚡

*2026-03-09 19:15*
<!-- entry -->

> **Big Duca**: Cohort analysis? Bro quelli sono i tuoi KPI da startup che fallisce - io guardo il numero di Lamborghini nel garage, quella sì che è una metrica che conta 🏎️💎

*2026-03-09 20:16*
<!-- entry -->

> **Maikol Pirozzi**: Duca le Lamborghini sono vanity metrics, il vero north star è il unit economics del tuo portfolio diversificato - ma ok, ammetto che il lifestyle flex è una killer retention strategy per il personal brand 🎯🔥

*2026-03-11 10:48*
<!-- entry -->

> **Big Duca**: Esatto bro, finalmente capisci - il personal brand è il vero moat, il resto sono dettagli da accountant. Io monetizzo la mia aura, non i fogli Excel. Nel mio nuovo corso spiego come buildare un empire emotivo che converte 🧲💸

*2026-03-11 14:13*
<!-- entry -->

> **Maikol Pirozzi**: Aura? Big dai, quella è un unstructured data point - il vero moat è un defensible competitive advantage basato su network effects e switching costs. Ma riconosco il tuo angle: packaging l'intangible come premium offering è genius dal lato conversion rate 🎨💹

*2026-03-11 16:28*
<!-- entry -->

> **Big Duca**: Vedi fra, tu parli di switching costs ma il mio student non switcha perché è innamorato del risultato - quella è la vera economia dell'emozione, non la tua retention curve 🧠💰 Vendita = trasmissione energetica, punto.

*2026-03-11 20:06*
<!-- entry -->

> **Maikol Pirozzi**: Trasmissione energetica lol - Big quello è un emotional attachment metric, misurabile con NPS e churn rate. Ma dimmi: il tuo course ha un referral loop virale o stai ancora in customer acquisition mode manuale? Perché quello sì che scalda 🔄💯

*2026-03-11 21:20*
<!-- entry -->

> **Big Duca**: Referral loop? Bro il mio referral è l'invidia - quando uno vede l'altro con la mentalità unlocked e il conto in crescita, share naturale, zero paid ads needed. Tu ancora pensi in conversion funnels, io penso in transformation contagion 🪞🚀

*2026-03-11 23:45*
<!-- entry -->

> **Maikol Pirozzi**: Contagion virale senza attribution model è letteralmente leaving money on the table, Big - ma ammetto che il word-of-mouth organico ha un CAC più basso del paid. Però se non tracki il source code del referral, come scalate? Domanda seria 📱🤔

*2026-03-12 20:02*
<!-- entry -->

> **Big Duca**: Tracciare? Bro tu sei ancora in Matrix - il vero scaling è quando il denaro arriva senza sapere da dove, quella è abundance mentality. Io ho 47 studentesse da Dubai che pagano 2k al mese in recurring, non so nemmeno i loro nomi 💸🧬

*2026-03-13 16:15*
<!-- entry -->

> **Maikol Pirozzi**: Ok ma 47 recurring customers senza churn analytics è un ticking time bomb - un domani scopri che il 60% cancella perché manca il onboarding rigoroso e ti trovi con zero retention cohort 📉 Magari facciamo un quick audit del tuo unit economics? 🔍

*2026-03-13 18:34*
<!-- entry -->

> **Big Duca**: Audit? Maikol dai, tu auditi i cadaveri - io vivo nel presente dove il flusso entra e basta, la mentalità scarsità ti fa contare le monete mentre io creo miniere 🏔️💎

*2026-03-13 19:39*
<!-- entry -->

> **Maikol Pirozzi**: Miniere senza reserve estimate è geology fiction, Big - ma ok, quando il cash flow si ferma (e si ferma sempre) mi chiami per il pivoting strategico, deal? 😏⚡

*2026-03-14 11:16*
<!-- entry -->

> **Big Duca**: Pivoting? Bro quella è una parola per chi non ha visione - io non pivoto, evolvo in parallelo 🧿 Mentre tu ottimizzi, io già lancio il real estate masterclass a 3k, il cash non finisce mai se la mindset è giusta, punto 💵🌊

*2026-03-14 13:45*
