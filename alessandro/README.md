# klak

Un motore scacchistico scritto in Python, costruito un passo alla volta sopra [python-chess](https://python-chess.readthedocs.io/).

Fatto da [Alessandro Marpino](https://github.com/alemarpino-rgb).

## Come funziona

**Ricerca**
- **Negamax con potatura alfa-beta**: esplora l'albero delle mosse e scarta i rami che l'avversario non permetterebbe mai.
- **Ricerca di quiescenza**: alla fine della ricerca principale continua a esaminare le catture, per non fermarsi a metà di uno scambio (effetto orizzonte).
- **Ordinamento delle mosse (MVV-LVA)**: prova prima promozioni e catture, con la vittima più preziosa presa dall'attaccante meno prezioso. Più tagli alfa-beta, molti meno nodi.
- **Controlli di patta economici**: matto e stallo ricavati dalla stessa lista di mosse; ripetizioni, regola delle 50 mosse e materiale insufficiente controllati solo quando possono essere veri.
- **Varietà**: tra mosse con lo stesso punteggio ne sceglie una a caso, così non gioca sempre la stessa partita.

**Valutazione**
- Materiale: P=100, C=300, A=320, T=500, D=900.
- **Piece-square tables**: un bonus o malus per ogni pezzo in base alla casa che occupa (centro, sviluppo, pedoni avanzati…).
- **Re in due fasi**: nel mediogioco preferisce stare al riparo dietro l'arrocco, nel finale va al centro.

## Requisiti

- Python 3 (consigliato **[PyPy](https://pypy.org/)**, molto più veloce per questo tipo di codice)
- python-chess

```bash
pypy3 -m ensurepip
pypy3 -m pip install chess
```

## Uso

```bash
pypy klak.py
```

Il programma chiede la profondità di ricerca e fa giocare klak contro sé stesso, stampando la scacchiera a ogni mossa e il PGN della partita alla fine. Per ogni mossa mostra anche nodi esaminati, tempo e nodi al secondo.

Per giocarci contro c'è la funzione `gioca(board, prof, colore_motore)`: le mosse si inseriscono in notazione SAN (`e4`, `Nf3`, `O-O`…).

Profondità consigliate:
- **4**: risposte quasi immediate
- **5**: gioco più forte, da pochi decimi a qualche decina di secondi a mossa nel mediogioco

## Prestazioni

Misurate con `test.py` (PyPy): ricerca a profondità 4 su 4 posizioni fisse (apertura, mediogioco, finale), stessa ricerca della 0.5.0, cambia solo la funzione di valutazione.

| Valutazione | Nodi | Tempo | Nodi/s |
|---|---|---|---|
| 0.3.0 (`piece_map`) | 111.217 | 3,90 s | 28.520 |
| 0.5.0 (tabelle precalcolate + bitboard) | 111.217 | 2,47 s | 45.050 |

Stessi nodi (la ricerca è identica, le due valutazioni danno gli stessi punteggi), ma **circa 1,6 volte più veloce**.

In un primo test contro Stockfish limitato a 1320 Elo (0,1 s a mossa), klak a profondità 3 e senza ordinamento delle mosse ha fatto **9 punti su 10**.

## L'autore

L'autore di questo motore è Alessandro Marpino (io ;) ). Ho anche fatto altri progetti come [GrapeScript](https://github.com/alemarpino-rgb/GrapeScript), un intero linguaggio di programmazione! 

## Novità

**0.5.0**
- Valutazione con tabelle precalcolate (valore del pezzo + bonus della casa già sommati e specchiati) e lettura dei pezzi direttamente dai bitboard
- `is_finale` calcolato con `popcount`

**0.3.0**
- Ordinamento delle mosse (MVV-LVA) in tutta la ricerca
- Controlli di patta e matto economici
- Contatore di nodi e nodi/s

## Prossimi passi

- [x] Valutazione più veloce con tabelle precalcolate e bitboard
- [ ] Tabella di trasposizione
- [ ] Approfondimento iterativo con limite di tempo
- [ ] Killer moves
- [ ] Valutazione più ricca: struttura pedonale, sicurezza del re, pedoni passati
- [ ] Test automatici, benchmark e suite tattica
- [ ] Match regolari contro Stockfish per misurare l'Elo
