import chess
import random
contatore = 0

scacchiera=chess.Board()
while not scacchiera.is_game_over():
    mosse = list(scacchiera.legal_moves)
    mossa = random.choice(mosse)
    contatore = contatore + 1
    scacchiera.push (mossa)
print (scacchiera.result())
print (contatore)
print (scacchiera)
