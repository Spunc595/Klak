use shakmaty::CastlingMode;
use shakmaty::Move;
use shakmaty::uci::UciMove;
use shakmaty::{Chess, Color, Position, Role};
use std::io::{self, BufRead};
use std::time::Instant;

const INFINITO: i32 = 1000000;
const MATTO: i32 = 100000;
const DELTA_MARGINE: i32 = 200;

const PEDONI: [i32; 64] = [
    0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5, -10, 0, 0, -10, -5, 5, 0, 0, 0,
    20, 20, 0, 0, 0, 5, 5, 10, 25, 25, 10, 5, 5, 10, 10, 20, 30, 30, 20, 10, 10, 50, 50, 50, 50,
    50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0,
];

const CAVALLI: [i32; 64] = [
    -50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40, -30, 5, 10, 15, 15, 10,
    5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10,
    0, -30, -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50,
];

const ALFIERI: [i32; 64] = [
    -20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10,
    10, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0,
    -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20,
];

const TORRI: [i32; 64] = [
    0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0,
    0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0,
    0, 0, 0, 0, 0, 0,
];

const DONNA: [i32; 64] = [
    -20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0,
    0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20,
];

const RE_MEDIOGIOCO: [i32; 64] = [
    20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, -10, -20, -20, -20, -20, -20, -20,
    -10, -20, -30, -30, -40, -40, -30, -30, -20, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40,
    -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50,
    -40, -40, -30,
];

const RE_FINALE: [i32; 64] = [
    -50, -30, -30, -30, -30, -30, -30, -50, -30, -30, 0, 0, 0, 0, -30, -30, -30, -10, 20, 30, 30,
    20, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10,
    20, 30, 30, 20, -10, -30, -30, -20, -10, 0, 0, -10, -20, -30, -50, -40, -30, -20, -20, -30,
    -40, -50,
];

fn valore_casa(ruolo: Role, indice: usize, in_finale: bool) -> i32 {
    match ruolo {
        Role::Pawn => PEDONI[indice],
        Role::Knight => CAVALLI[indice],
        Role::Bishop => ALFIERI[indice],
        Role::Rook => TORRI[indice],
        Role::Queen => DONNA[indice],
        Role::King => {
            if in_finale {
                RE_FINALE[indice]
            } else {
                RE_MEDIOGIOCO[indice]
            }
        }
    }
}

fn valore_ruolo(ruolo: Role) -> i32 {
    match ruolo {
        Role::Pawn => 99,
        Role::Knight => 319,
        Role::Bishop => 330,
        Role::Rook => 499,
        Role::Queen => 899,
        Role::King => 0,
    }
}

fn bonus(pos: &Chess, colore: Color) -> i32 {
    let mut totale = 0;
    let in_finale = finale(pos);
    for ruolo in Role::ALL {
        let pezzi = pos.board().by_color(colore) & pos.board().by_role(ruolo);
        for casa in pezzi {
            let indice = if colore == Color::White {
                casa as usize
            } else {
                casa.flip_vertical() as usize
            };
            totale = totale + valore_casa(ruolo, indice, in_finale);
        }
    }
    totale
}

fn finale(pos: &Chess) -> bool {
    pos.board().occupied().count() <= 10
}

fn punteggio_mossa(m: &Move) -> i32 {
    let score = if let Some(victim) = m.capture() {
        let attacker = m.role();
        10000 + valore_ruolo(victim) * 10 - valore_ruolo(attacker)
    } else if m.is_promotion() {
        9000
    } else {
        0
    };
    score
}

fn materiale(pos: &Chess, colore: Color) -> i32 {
    let mut totale = 0;
    for ruolo in Role::ALL {
        let quanti = (pos.board().by_color(colore) & pos.board().by_role(ruolo)).count();
        totale = totale + quanti as i32 * valore_ruolo(ruolo);
    }
    totale
}

fn valuta(pos: &Chess) -> i32 {
    let bianco = materiale(pos, Color::White) + bonus(pos, Color::White);
    let nero = materiale(pos, Color::Black) + bonus(pos, Color::Black);
    bianco - nero
}

fn quiescenza(pos: &Chess, mut alfa: i32, beta: i32, q_nodes: &mut u64) -> i32 {
    *q_nodes += 1;

    let in_check = pos.is_check();
    let segno = if pos.turn() == Color::White { 1 } else { -1 };

    let mut stand_pat = 0;
    if !in_check {
        stand_pat = segno * valuta(pos);
        if stand_pat >= beta {
            return beta;
        }
        if stand_pat > alfa {
            alfa = stand_pat;
        }
    }

    let mut legal_moves_count = 0;

    let mut mosse: Vec<Move> = Vec::new();
    for m in pos.legal_moves() {
        if !in_check && !m.is_capture() && !m.is_promotion() {
            continue;
        }
        mosse.push(m);
    }
    mosse.sort_by_key(|m| -punteggio_mossa(m));
    for m in mosse {
        if !in_check {
            let mut potenziale_guadagno = 0;

            if let Some(victim) = m.capture() {
                potenziale_guadagno += valore_ruolo(victim);
            }

            if let Some(promoted) = m.promotion() {
                potenziale_guadagno += valore_ruolo(promoted) - valore_ruolo(Role::Pawn);
            }

            if stand_pat + potenziale_guadagno + DELTA_MARGINE <= alfa {
                continue;
            }
        }

        legal_moves_count += 1;
        let dopo = pos.clone().play(m).unwrap();
        let valore = -quiescenza(&dopo, -beta, -alfa, q_nodes);

        if valore >= beta {
            return beta;
        }
        if valore > alfa {
            alfa = valore;
        }
    }

    if in_check && legal_moves_count == 0 {
        return -MATTO;
    }

    alfa
}

fn mossa_migliore(
    pos: &Chess,
    profondita: i32,
    s_nodes: &mut u64,
    q_nodes: &mut u64,
) -> (Option<Move>, i32) {
    let mut alfa = -INFINITO;
    let mut migliore_mossa = None;
    for m in pos.legal_moves() {
        let dopo = pos.clone().play(m).unwrap();
        let valore = -cerca(&dopo, profondita - 1, -INFINITO, -alfa, s_nodes, q_nodes);
        if valore > alfa {
            alfa = valore;
            migliore_mossa = Some(m);
        }
    }
    (migliore_mossa, alfa)
}

fn cerca_con_tempo(pos: &Chess, secondi: f64) -> Option<Move> {
    let inizio = Instant::now();
    let mut s_nodes = 0;
    let mut q_nodes = 0;
    let mut migliore = None;
    let mut profondita = 1;
    let mut durata_ultima = 0.0;
    loop {
        let passati = inizio.elapsed().as_secs_f64();
        if passati + durata_ultima * 8.0 > secondi || profondita > 64 {
            break;
        }
        let inizio_iter = Instant::now();
        let (mossa, punteggio) = mossa_migliore(pos, profondita, &mut s_nodes, &mut q_nodes);
        let pv = match mossa {
            Some(m) => m.to_uci(CastlingMode::Standard).to_string(),
            None => "0000".to_string(),
        };
        migliore = mossa;
        durata_ultima = inizio_iter.elapsed().as_secs_f64();
        println!(
            "info depth {} score cp {} nodes {} time {} pv {}",
            profondita,
            punteggio,
            s_nodes + q_nodes,
            (inizio.elapsed().as_secs_f64() * 1000.0) as u64, pv
        );
        profondita = profondita + 1;
    }
    migliore
}

fn cerca(
    pos: &Chess,
    profondita: i32,
    mut alfa: i32,
    beta: i32,
    s_nodes: &mut u64,
    q_nodes: &mut u64,
) -> i32 {
    *s_nodes += 1;

    if profondita <= 0 {
        return quiescenza(pos, alfa, beta, q_nodes);
    }
    let mut mosse = pos.legal_moves();
    if mosse.is_empty() {
        if pos.is_check() {
            return -MATTO - profondita;
        } else {
            return 0;
        }
    }

    mosse.sort_by_key(|m| -punteggio_mossa(m));

    for m in mosse {
        let dopo = pos.clone().play(m).unwrap();
        let valore = -cerca(&dopo, profondita - 1, -beta, -alfa, s_nodes, q_nodes);
        if valore >= beta {
            return beta;
        }
        if valore > alfa {
            alfa = valore;
        }
    }
    alfa
}

fn main() {
    let stdin = io::stdin();
    let mut pos = Chess::default();
    for riga in stdin.lock().lines() {
        let riga = riga.unwrap();
        if riga == "uci" {
            println!("id name Kłak v1,0,0");
            println!("id author Daniele Marpino");
            println!("uciok");
        } else if riga == "isready" {
            println!("readyok");
        } else if riga.starts_with("position") {
            let parole: Vec<&str> = riga.split_whitespace().collect();
            pos = Chess::default();
            if parole.len() > 3 {
                for testo in &parole[3..] {
                    let uci: UciMove = testo.parse().unwrap();
                    let m = uci.to_move(&pos).unwrap();
                    pos = pos.play(m).unwrap();
                }
            }
        } else if riga.starts_with("go") {
            let parole: Vec<&str> = riga.split_whitespace().collect();
            let nome = if pos.turn() == Color::White {
                "wtime"
            } else {
                "btime"
            };
            let mut secondi = 2.0;
            if let Some(posto) = parole.iter().position(|&p| p == nome) {
                let millisecondi: f64 = parole[posto + 1].parse().unwrap();
                secondi = millisecondi / 20000.0;
            }
            let migliore = cerca_con_tempo(&pos, secondi);
            match migliore {
                Some(m) => println!("bestmove {}", m.to_uci(CastlingMode::Standard)),
                None => println!("bestmove 0000"),
            }
        } else if riga == "debug" {
            println!("{:?} {}", pos.turn(), pos.legal_moves().len());
        } else if riga == "quit" {
            break;
        }
    }
}
