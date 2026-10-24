# klak

Un motore scacchistico scritto in Python, costruito un passo alla volta sopra [python-chess](https://python-chess.readthedocs.io/).
Fatto da [Alessandro Marpino](https://github.com/alemarpino-rgb).

## Come funziona

**Ricerca**
- **Negamax con potatura alfa-beta**: esplora l'albero delle mosse e scarta i rami che l'avversario non permetterebbe mai.
- **Approfondimento iterativo con limite di tempo**: cerca a profondità 1, 2, 3… finché non scade il tempo della mossa, poi gioca la migliore mossa dell'ultima profondità completata. La mossa migliore di ogni giro viene provata per prima in quello successivo. Si ferma subito se trova un matto o se la mossa è obbligata.
- **Ricerca di quiescenza**: alla fine della ricerca principale continua a esaminare le catture, per non fermarsi a metà di uno scambio (effetto orizzonte).
- **Ordinamento delle mosse (MVV-LVA)**: prova prima promozioni e catture, con la vittima più preziosa presa dall'attaccante meno prezioso. Più tagli alfa-beta, molti meno nodi.
- **Controlli di patta economici**: matto e stallo ricavati dalla stessa lista di mosse; ripetizioni, regola delle 50 mosse e materiale insufficiente controllati solo quando possono essere veri.
- **Varietà**: tra mosse con lo stesso punteggio ne sceglie una a caso, così non gioca sempre la stessa partita.

**Valutazione**
- Materiale: P=100, C=300, A=320, T=500, D=900.
- **Piece-square tables**: un bonus o malus per ogni pezzo in base alla casa che occupa (centro, sviluppo, pedoni avanzati…).
- **Tabelle precalcolate e bitboard**: valore del pezzo e bonus della casa sono già sommati e specchiati all'avvio; durante la ricerca i pezzi si leggono direttamente dai bitboard.
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

Il programma chiede il **tempo totale in secondi** per la partita e fa giocare klak contro sé stesso, stampando la scacchiera a ogni mossa e il PGN alla fine. Per ogni mossa usa circa un trentesimo del tempo rimasto e mostra le profondità raggiunte, i nodi esaminati e i nodi al secondo.

Per giocarci contro c'è la funzione `gioca`: le mosse si inseriscono in notazione SAN (`e4`, `Nf3`, `O-O`…).

Tempi consigliati:
- **120 s**: partita veloce, circa 2-4 secondi a mossa all'inizio
- **600 s o più**: gioco più forte, profondità 6-7 nei finali

## Prestazioni

Con PyPy su un PC desktop, circa **100.000 nodi/s**.

**Valutazione precalcolata (0.5.0).** Ricerca a profondità 4 su 4 posizioni fisse, cambiando solo la funzione di valutazione:

| Valutazione | Nodi | Tempo | Nodi/s |
|---|---|---|---|
| 0.3.0 (`piece_map`) | 111.217 | 3,90 s | 28.520 |
| 0.5.0 (tabelle precalcolate + bitboard) | 111.217 | 2,47 s | 45.050 |

Stessi nodi (le due valutazioni danno gli stessi punteggi), ma **circa 1,6 volte più veloce**.

**Approfondimento iterativo (0.6.0).** Match di 10 partite, colori alternati:

| Versione | Ricerca | Tempo medio a mossa | Tempo massimo | Punti |
|---|---|---|---|---|
| 0.6.0 | iterativa, 2 s a mossa | 1,72 s | 2,04 s | **8 / 10** |
| 0.5.0 | profondità fissa 4 | 0,22 s | 2,45 s | 2 / 10 |

Il tempo per mossa della 0.6.0 resta sotto controllo (massimo 2,04 s su un limite di 2 s). Nota: in questo match la 0.6.0 aveva molto più tempo medio a disposizione, quindi il risultato mostra che sa usare il tempo, non che è più forte a parità di tempo.

**Contro Stockfish.** In un primo test contro Stockfish limitato a 1320 Elo (0,1 s a mossa), klak a profondità 3 e senza ordinamento delle mosse ha fatto **9 punti su 10**.

## Novità

**0.6.0**
- Approfondimento iterativo con limite di tempo per mossa
- Gestione del tempo: un trentesimo del tempo rimasto per ogni mossa
- Stop immediato con mossa obbligata o matto trovato

**0.5.0**
- Valutazione con tabelle precalcolate e bitboard
- `is_finale` calcolato con `popcount`

## L'autore

L'autore di questo motore è Alessandro Marpino (io ;) ). Ho anche fatto altri progetti come [GrapeScript](https://github.com/alemarpino-rgb/GrapeScript), un intero linguaggio di programmazione!

## Prossimi passi

- [x] Valutazione più veloce con tabelle precalcolate e bitboard
- [x] Approfondimento iterativo con limite di tempo
- [ ] Tabella di trasposizione
- [ ] Killer moves
- [ ] Valutazione più ricca: struttura pedonale, sicurezza del re, pedoni passati
- [ ] Test automatici, benchmark e suite tattica
- [ ] Match regolari contro Stockfish per misurare l'Elo
