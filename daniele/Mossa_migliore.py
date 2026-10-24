import chess

valori = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
scacchiera = chess.Board()
scacchiera.push_uci("e2e4")
scacchiera.push_uci("d7d5")

def valuta(scacchiera):
    materiale_bianco = 0
    materiale_nero = 0

    for pezzo in scacchiera.piece_map().values():
        lettera = pezzo.symbol()
        if lettera.isupper():
            materiale_bianco = materiale_bianco + valori[lettera]
        else:
            materiale_nero = materiale_nero + valori[lettera.upper()]

    return materiale_bianco - materiale_nero

def minimax(scacchiera, profondita):

    if profondita <= 0:
        return valuta(scacchiera)

    bianco = scacchiera.turn == chess.WHITE
    migliore = -1000
    if not bianco:
        migliore = 1000
    for mossa in list(scacchiera.legal_moves):
        scacchiera.push(mossa)
        valore = minimax(scacchiera, profondita - 1)
        scacchiera.pop()
        if bianco and valore > migliore:
            migliore = valore
        elif not bianco and valore < migliore:
            migliore = valore
    return migliore

def mossa_migliore (scacchiera, profondita):
    bianco = scacchiera.turn == chess.WHITE
    migliore = -1000
    migliore_mossa = None
    if not bianco:
        migliore = 1000
    for mossa in list(scacchiera.legal_moves):
        scacchiera.push (mossa)
        valore = minimax (scacchiera, profondita -1)
        scacchiera.pop()

        if bianco and valore > migliore:
            migliore = valore
            migliore_mossa = mossa
        elif not bianco and valore < migliore:
            migliore = valore
            migliore_mossa = mossa
    return migliore_mossa, migliore


mossa, valore = mossa_migliore (scacchiera, 3)
print (mossa, valore)
