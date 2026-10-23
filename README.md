# Kłak

🇮🇹 [Italiano](#italiano) · 🇬🇧 [English](#english)

---

## Italiano

**Kłak** è un piccolo motore di scacchi scritto per imparare a programmare. È un progetto didattico di un padre e di suo figlio: si parte da Python, con la libreria [python-chess](https://python-chess.readthedocs.io/), e più avanti il motore verrà riscritto in Rust.

### Il nome

Il nome si scrive **Kłak**, con la lettera polacca *ł*, che si legge come una *w*. Si pronuncia quindi come l'inglese *quack*, il verso della papera. È un gioco di parole.

Nei nomi di file e cartelle si usa **Klak**, senza la *ł*, perché questa lettera non si trova su tutte le tastiere.

### Cosa c'è in questo repository

Ci sono due versioni di partenza, indipendenti tra loro:

| Cartella | Autore | Cosa fa |
| --- | --- | --- |
| `daniele/` | Daniele | **Klak 0.0.0**: la versione più semplice. Gioca partite intere scegliendo mosse a caso. È la base da cui si impara. |
| `alessandro/` | Alessandro, figlio di Daniele | Un motore completo e funzionante. |

Le due cartelle restano com'è giusto che sia: sono la storia del progetto.

### Il piano

1. Daniele impara Python, un passo alla volta, costruendo Klak da zero.
2. Quando arriva al livello di Alessandro, i due codici si confrontano.
3. Si tengono le parti migliori o scritte meglio di ciascuno.
4. Dal codice unito, in una nuova cartella `klak/`, nasce il **Klak definitivo**, segnato come versione `v1.0.0`.
5. Poi arriva la riscrittura in Rust.

Il percorso di apprendimento:

1. Basi di Python
2. python-chess: scacchiera, mosse legali, partita a caso
3. Valutazione del materiale
4. Minimax, poi alpha-beta
5. Quiescence e ordinamento delle mosse
6. Tabelle pezzo-casa e approfondimento iterativo con gestione del tempo
7. Protocollo UCI, per collegare Klak a un'interfaccia grafica
8. Riscrittura in Rust

### Come provarlo

Serve Python 3. La libreria si installa con:

```
pip install chess
```

Poi, per esempio:

```
python daniele/klak_0_0_0.py
```

In Google Colab la prima riga di una cella è `!pip install chess`.

### Autori

Daniele e suo figlio Alessandro. Il codice di ogni cartella è di chi l'ha scritto.

### Licenza

Klak è software libero, distribuito con la licenza **GNU General Public License v3.0** (GPL-3.0). Il testo completo è nel file `LICENSE`.

---

## English

**Kłak** is a small chess engine written to learn programming. It is a learning project by a father and his son: it starts in Python, with the [python-chess](https://python-chess.readthedocs.io/) library, and the engine will later be rewritten in Rust.

### The name

The name is spelled **Kłak**, with the Polish letter *ł*, which sounds like a *w*. So it is pronounced like the English *quack*, the sound a duck makes. It is a play on words.

In file and folder names it is written **Klak**, without the *ł*, because that letter is not on every keyboard.

### What is in this repository

There are two starting versions, independent from each other:

| Folder | Author | What it does |
| --- | --- | --- |
| `daniele/` | Daniele | **Klak 0.0.0**: the simplest version. It plays whole games by choosing random moves. It is the base to learn from. |
| `alessandro/` | Alessandro, Daniele's son | A complete, working engine. |

Both folders stay as they are: they are the history of the project.

### The plan

1. Daniele learns Python, one step at a time, building Klak from scratch.
2. When he reaches Alessandro's level, the two codebases are compared.
3. The best or best-written parts of each are kept.
4. From the merged code, in a new `klak/` folder, comes the **final Klak**, tagged as version `v1.0.0`.
5. Then comes the rewrite in Rust.

The learning path:

1. Python basics
2. python-chess: board, legal moves, a random game
3. Material evaluation
4. Minimax, then alpha-beta
5. Quiescence and move ordering
6. Piece-square tables and iterative deepening with time management
7. UCI protocol, to connect Klak to a graphical interface
8. Rewrite in Rust

### How to try it

You need Python 3. Install the library with:

```
pip install chess
```

Then, for example:

```
python daniele/klak_0_0_0.py
```

In Google Colab, the first line of a cell is `!pip install chess`.

### Authors

Daniele and his son Alessandro. The code in each folder belongs to whoever wrote it.

### License

Klak is free software, released under the **GNU General Public License v3.0** (GPL-3.0). The full text is in the `LICENSE` file.
