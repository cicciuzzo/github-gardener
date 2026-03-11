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
