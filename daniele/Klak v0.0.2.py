import chess
import time
import random

valori = {"P": 99, "N": 319, "B": 330, "R": 499, "Q": 899, "K": 0}
INFINITO = 1000000

tabella_pedone = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10,-20,-20, 10, 10,  5,
      5, -5,-10,  0,  0, -10,-5,  5,
      0,  0,  0, 20, 20,  0,  0,  0,
      5,  5, 10, 25, 25, 10,  5,  5,
     10, 10, 20, 30, 30, 20, 10, 10,
     50, 50, 50, 50, 50, 50, 50, 50,
      0,  0,  0,  0,  0,  0,  0,  0,
]

tabella_cavallo = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

tabella_alfiere = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

tabella_torre = [
      0,   0,   0,   5,   5,   0,   0,   0,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      5,  10,  10,  10,  10,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0,
]

tabella_donna = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -10,   5,   5,   5,   5,   5,   0, -10,
      0,   0,   5,   5,   5,   5,   0,  -5,
     -5,   0,   5,   5,   5,   5,   0,  -5,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20,
]

tabelle = {"P": tabella_pedone, "N": tabella_cavallo, "B" : tabella_alfiere, "R" : tabella_torre, "Q" : tabella_donna}
nodi = 0
scacchiera = chess.Board ()

def ordina (scacchiera):
    catture = []
    altre = []
    for mossa in scacchiera.legal_moves:
        if scacchiera.is_capture (mossa):
            catture.append (mossa)
        else:
            altre.append (mossa)
    return catture + altre

def valuta (scacchiera):
    materiale_bianco = 0
    materiale_nero = 0

    for casa, pezzo in scacchiera.piece_map ().items ():
        lettera = pezzo.symbol ()
        tipo = lettera.upper ()
        if lettera.isupper ():
            materiale_bianco = materiale_bianco + valori[tipo]
            if tipo in tabelle:
                materiale_bianco = materiale_bianco + tabelle [tipo] [casa]
        else:
            materiale_nero = materiale_nero + valori[tipo]
            if tipo in tabelle:
                materiale_nero = materiale_nero + tabelle [tipo] [chess.square_mirror (casa)]

    return materiale_bianco - materiale_nero

def quiescenza (scacchiera, alpha, beta):
    bianco = scacchiera.turn == chess.WHITE
    migliore = valuta (scacchiera)

    if bianco and migliore > alpha:
        alpha = migliore
    elif not bianco and migliore < beta:
        beta = migliore
    if beta <= alpha:
        return migliore

    for mossa in ordina (scacchiera):
        if scacchiera.is_capture (mossa):
            scacchiera.push (mossa)
            valore = quiescenza (scacchiera, alpha, beta)
            scacchiera.pop ()
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

def minimax (scacchiera, profondita, alpha, beta):
    global nodi
    nodi = nodi + 1

    if profondita <= 0:
        return quiescenza (scacchiera, alpha, beta)

    bianco = scacchiera.turn == chess.WHITE
    migliore = -INFINITO
    if not bianco:
        migliore = INFINITO
    for mossa in ordina (scacchiera):
        scacchiera.push (mossa)
        valore = minimax (scacchiera, profondita - 1, alpha, beta)
        scacchiera.pop ()
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
    migliore = -INFINITO
    migliore_mossa = None
    alpha = -INFINITO
    beta = INFINITO
    if not bianco:
        migliore = INFINITO
    for mossa in ordina (scacchiera):
        scacchiera.push (mossa)
        valore = minimax (scacchiera, profondita -1, alpha, beta)
        scacchiera.pop ()

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

def cerca (scacchiera, tempo_massimo):
    inizio = time.time ()
    migliore_mossa = None
    valore = 0
    for profondita in range (1, 20):
        inizio_giro = time.time ()
        migliore_mossa, valore = mossa_migliore (scacchiera, profondita)
        durata = time.time () - inizio_giro
        usato = time.time () - inizio
        if usato + durata* 10 > tempo_massimo:
            break
    return migliore_mossa, valore, profondita

scacchiera = chess.Board ()

while True:
    riga = input ()
    if riga == "uci":
        print ("id name Klak", flush = true)
        print ("id author Daniele", flush = true)
        print ("uciok", flush = true)
    elif riga == "isready":
        print ("readyok", flush=true)
    elif riga.startswith ("position"):
        parole = riga.split ()
        scacchiera = chess.Board ()
        for m in parole[3:]:
            scacchiera.push_uci (m)
    elif riga.startswith ("go"):
        migliore_mossa, valore, prof = cerca (scacchiera, 2)
        print ("bestmove", migliore_mossa, flush = true)  
    elif riga == "quit":
        break
