import time, chess, chess.pgn, klak050, klak060

PARTITE = 10
SECONDI = 2.0        # tempo per mossa della nuova
PROF_VECCHIA = 4     # profondità fissa della vecchia
MAX_SEMIMOSSE = 300

def scegli(nuova, board):
    if nuova:
        return klak060.cerca_iterativa(board, SECONDI)
    return klak050.cerca(board, PROF_VECCHIA)

punti = 0.0
tempi = {True: [], False: []}     # True = nuova, False = vecchia

with open("match.pgn", "w", encoding="utf-8") as pgn:
    for i in range(PARTITE):
        nuova_bianco = i % 2 == 0
        board = chess.Board()
        while not board.is_game_over(claim_draw=True) and board.ply() < MAX_SEMIMOSSE:
            nuova = (board.turn == chess.WHITE) == nuova_bianco
            t = time.time()
            board.push(scegli(nuova, board))
            tempi[nuova].append(time.time() - t)

        r = board.result(claim_draw=True)
        if r == "*":
            r = "1/2-1/2"
        if r == "1/2-1/2":
            punti += 0.5
        elif (r == "1-0") == nuova_bianco:
            punti += 1
        print(f"Partita {i + 1}: {r} (nuova col {'bianco' if nuova_bianco else 'nero'})")

        partita = chess.pgn.Game.from_board(board)
        partita.headers["White"] = "nuova" if nuova_bianco else "vecchia"
        partita.headers["Black"] = "vecchia" if nuova_bianco else "nuova"
        partita.headers["Result"] = r
        print(partita, file=pgn, end="\n\n")

for nome, chiave in (("Nuova", True), ("Vecchia", False)):
    t = tempi[chiave]
    print(f"{nome}: media {sum(t) / len(t):.2f}s a mossa, massimo {max(t):.2f}s")
print(f"Punti nuova: {punti} / {PARTITE}")