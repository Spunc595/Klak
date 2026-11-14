mod ricerca;
mod ripetizione;
mod valutazione;

use ricerca::cerca_con_tempo;
use ripetizione::{chiave, quante_volte};
use shakmaty::CastlingMode;
use shakmaty::uci::UciMove;
use shakmaty::{Chess, Color, Position};
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut pos = Chess::default();
    let mut storia: Vec<u64> = Vec::new();

    for riga in stdin.lock().lines() {
        let riga = riga.unwrap();
        if riga == "uci" {
            println!("id name Kłak v1.2.0");
            println!("id author Daniele Marpino");
            println!("uciok");
        } else if riga == "isready" {
            println!("readyok");
        } else if riga.starts_with("position") {
            let parole: Vec<&str> = riga.split_whitespace().collect();
            pos = Chess::default();
            storia.clear();
            storia.push(chiave(&pos));
            if parole.len() > 3 {
                for testo in &parole[3..] {
                    let uci: UciMove = match testo.parse() {
                        Ok(u) => u,
                        Err(_) => {
                            println!("info string mossa non valida: {}", testo);
                            break;
                        }
                    };

                    let m = match uci.to_move(&pos) {
                        Ok(mossa) => mossa,
                        Err(_) => break,
                    };
                    pos = pos.play(m).unwrap();
                    storia.push(chiave(&pos));
                }
            };
        } else if riga.starts_with("go") {
            let parole: Vec<&str> = riga.split_whitespace().collect();
            let nome = if pos.turn() == Color::White {
                "wtime"
            } else {
                "btime"
            };
            let mut secondi = 2.0;
            let nome_inc = if pos.turn() == Color::White {
                "winc"
            } else {
                "binc"
            };
            if let Some(ms) = leggi_numero(&parole, "movetime") {
                secondi = ms / 2000.0;
            } else if let Some(tempo) = leggi_numero(&parole, nome) {
                let incremento = leggi_numero(&parole, nome_inc).unwrap_or(0.0);
                secondi = (tempo / 20000.0 + incremento / 2000.0).min(tempo / 2000.0);
            }
            let migliore = cerca_con_tempo(&pos, secondi, &mut storia);
            match migliore {
                Some(m) => println!("bestmove {}", m.to_uci(CastlingMode::Standard)),
                None => println!("bestmove 0000"),
            }
        } else if riga == "debug" {
            println!("{:?} {}", pos.turn(), pos.legal_moves().len());
        } else if riga == "chiave" {
            println!("{}", chiave(&pos));
        } else if riga == "ripetizioni" {
            println!(
                "posizioni {} ripetuta {} volte",
                storia.len(),
                quante_volte(&storia, chiave(&pos))
            );
        } else if riga == "quit" {
            break;
        }
    }
}

fn leggi_numero(parole: &Vec<&str>, nome: &str) -> Option<f64> {
    if let Some(posto) = parole.iter().position(|&p| p == nome) {
        if let Some(testo) = parole.get(posto + 1) {
            if let Ok(numero) = testo.parse::<f64>() {
                return Some(numero);
            }
        }
    }
    None
}