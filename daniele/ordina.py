import chess
import time
import random

valori = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
nodi = 0
scacchiera = chess.Board()

def ordina (scacchiera):
    catture = []
    altre = []
    for mossa in scacchiera.legal_moves:
        if scacchiera.is_capture (mossa):
            catture.append (mossa)
        else:
            altre.append (mossa)
    return catture + altre

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

def minimax(scacchiera, profondita, alpha, beta):
    global nodi
    nodi = nodi + 1

    if profondita <= 0:
        return valuta(scacchiera)

    bianco = scacchiera.turn == chess.WHITE
    migliore = -1000
    if not bianco:
        migliore = 1000
    for mossa in ordina(scacchiera):
        scacchiera.push(mossa)
        valore = minimax(scacchiera, profondita - 1, alpha, beta)
        scacchiera.pop()
        if bianco and valore > migliore:
            migliore = valore
            if migliore > alpha:
                alpha = migliore
        elif not bianco and valore < migliore:
            migliore = valore
            if migliore < beta:
                beta = migliore
        if beta <= alpha:
            break
    return migliore

def mossa_migliore (scacchiera, profondita):
    bianco = scacchiera.turn == chess.WHITE
    migliore = -1000
    migliore_mossa = None
    alpha = -1000
    beta = 1000
    if not bianco:
        migliore = 1000
    for mossa in ordina (scacchiera):
        scacchiera.push (mossa)
        valore = minimax (scacchiera, profondita -1, alpha, beta)
        scacchiera.pop()

        if bianco and valore > migliore:
            migliore = valore
            if migliore > alpha:
                alpha = migliore
            migliore_mossa = mossa
        elif not bianco and valore < migliore:
            migliore = valore
            if migliore < beta:
                beta = migliore
            migliore_mossa = mossa
    return migliore_mossa, migliore


while not scacchiera.is_game_over () and scacchiera.fullmove_number < 2:
    if scacchiera.turn == chess.WHITE:
       migliore_mossa, valore = mossa_migliore (scacchiera, 5 )
       scacchiera.push (migliore_mossa)
       print (migliore_mossa, valore)
    else:
        time.sleep (1)
        mosse = list (scacchiera.legal_moves)
        mossa = random.choice (mosse)
        scacchiera.push (mossa)
        print (valuta(scacchiera))
        print (scacchiera)

scacchiera = chess.Board ()
nodi = 0
inizio = time.time ()
mossa, valore = mossa_migliore (scacchiera, 5)
print (nodi, time.time() - inizio, mossa, valore)
print (ordina (scacchiera)[0])
