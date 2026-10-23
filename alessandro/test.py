import random, time, chess, klak030, klak050

# --- posizioni di prova, sempre le stesse grazie al seed ---
random.seed(1)
posizioni = []
while len(posizioni) < 2000:
    b = chess.Board()
    for _ in range(random.randint(5, 60)):
        if b.is_game_over():
            break
        b.push(random.choice(list(b.legal_moves)))
    if not b.is_game_over():
        posizioni.append(b)

# --- 1. solo valutazione ---
def misura_valutazione(f):
    t = time.time()
    for _ in range(20):
        for b in posizioni:
            f(b, chess.WHITE)
    return time.time() - t

misura_valutazione(klak030.valuta_posizione)    # riscaldamento del JIT
misura_valutazione(klak050.valuta_posizione)
print(f"Valutazione vecchia: {misura_valutazione(klak030.valuta_posizione):.2f}s")
print(f"Valutazione nuova:   {misura_valutazione(klak050.valuta_posizione):.2f}s")

# --- 2. ricerca completa su posizioni fisse ---
FEN = [
    chess.STARTING_FEN,
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    "r2q1rk1/pb2bppp/1pn1pn2/2pp4/3P4/1PN1PN2/PBQ1BPPP/R4RK1 w - - 0 11",
    "8/5pk1/6p1/3R4/5P2/6KP/r7/8 w - - 0 40",
]

def misura_ricerca(funzione_valutazione, profondita=4):
    klak050.valuta_posizione = funzione_valutazione
    random.seed(42)                 # cerca() mescola le mosse: stesso seed = stessa ricerca
    klak050.NODI = 0
    t = time.time()
    for fen in FEN:
        klak050.cerca(chess.Board(fen), profondita)
    dt = time.time() - t
    return klak050.NODI, dt

nuova = klak050.valuta_posizione
vecchia = klak030.valuta_posizione
misura_ricerca(vecchia, 3); misura_ricerca(nuova, 3)   # riscaldamento

for nome, f in (("vecchia", vecchia), ("nuova", nuova)):
    nodi, dt = misura_ricerca(f)
    print(f"Ricerca {nome}: {nodi} nodi in {dt:.2f}s ({nodi / dt:.0f} nodi/s)")