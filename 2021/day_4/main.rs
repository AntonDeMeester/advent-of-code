use std::collections::HashSet;
use std::convert::TryInto;
use std::fs;

#[derive(Debug, Copy, Clone)]
struct BingoPattern {
    numbers: [[i8; 5]; 5],
    state: [[bool; 5]; 5],
}

#[derive(Debug)]
struct BingoResult {
    pattern: BingoPattern,
    rounds: Vec<i8>,
}

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> (Vec<i8>, Vec<BingoPattern>) {
    let numbers_lines: Vec<i8> = lines[0].split(",").map(|s| s.parse().unwrap()).collect();

    let mut i = 2;
    let mut patterns = Vec::<BingoPattern>::new();
    while i < lines.len() {
        let mut numbers: [[i8; 5]; 5] = [[0; 5]; 5];
        for j in 0..5 {
            let line: Vec<i8> = lines[i + j]
                .split_ascii_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            numbers[j] = line.try_into().expect("Slice with incorrect length");
        }
        let state = [[false; 5]; 5];
        patterns.push(BingoPattern {
            numbers: numbers,
            state: state,
        });
        i += 6;
    }
    return (numbers_lines, patterns);
}

fn resolve_bingo(numbers: &Vec<i8>, bingo: &BingoPattern) -> (bool, [[bool; 5]; 5]) {
    let mut state = [[false; 5]; 5];
    for i in 0..bingo.numbers.len() {
        for j in 0..bingo.numbers[0].len() {
            for value in numbers {
                if bingo.numbers[i][j] == *value {
                    state[i][j] = true;
                    break;
                }
            }
        }
    }

    for i in 0..bingo.numbers.len() {
        for _ in 0..bingo.numbers[0].len() {
            if state[i].iter().all(|x| *x == true) {
                return (true, state);
            }
            let vert = [
                state[0][i],
                state[1][i],
                state[2][i],
                state[3][i],
                state[4][i],
            ];
            if vert.iter().all(|x| *x == true) {
                return (true, state);
            }
        }
    }
    return (false, state);
}

fn calculate_result(pattern: &BingoPattern, numbers: &Vec<i8>) -> i32 {
    let mut left = 0i32;
    for i in 0..pattern.numbers.len() {
        for j in 0..pattern.numbers[0].len() {
            if !pattern.state[i][j] {
                left += i32::from(pattern.numbers[i][j]);
            }
        }
    }
    let right = i32::from(numbers[numbers.len() - 1]);

    return left * right;
}

fn play_normal_bingo(numbers: &Vec<i8>, patterns: &Vec<BingoPattern>) -> (BingoPattern, Vec<i8>) {
    for i in 5..numbers.len() {
        let number_slice = &numbers[0..i];
        for p in patterns {
            let (success, state) = resolve_bingo(&number_slice.to_vec(), p);
            if success {
                let result = BingoPattern {
                    numbers: p.numbers,
                    state: state,
                };
                return (result, number_slice.to_vec());
            }
        }
    }
    panic!("AAAAAH")
}

fn lose_bingo<'a>(numbers: &Vec<i8>, patterns: &Vec<BingoPattern>) -> BingoResult {
    let mut winner_index = HashSet::new();
    let mut last_winner: Option<BingoResult> = None;
    for i in 5..numbers.len() {
        let number_slice = &numbers[0..i];
        for (j, p) in patterns.iter().enumerate() {
            if winner_index.contains(&j) {
                continue;
            }
            let (success, state) = resolve_bingo(&number_slice.to_vec(), p);
            if success {
                last_winner = Some(BingoResult {
                    pattern: BingoPattern {
                        numbers: p.numbers,
                        state: state,
                    },
                    rounds: number_slice.to_vec(),
                });
                winner_index.insert(j);
            }
        }
    }
    last_winner.expect("Could not find any winners")
}

fn day_4() {
    let filename = "2021/day_4/input.txt";
    let lines = read_file(filename);
    let (numbers, patterns) = parse_lines(&lines);

    let (pattern, rounds) = play_normal_bingo(&numbers, &patterns);
    let result = calculate_result(&pattern, &rounds);
    println!(
        "Normal bingo was solved after {} rounds. The result is {}",
        rounds.len(),
        result
    );

    let last_result = lose_bingo(&numbers, &patterns);
    let lost_result = calculate_result(&last_result.pattern, &last_result.rounds);
    println!(
        "Losing bingo was solved after {} rounds. The result is {}",
        last_result.rounds.len(),
        lost_result
    );
}

fn main() {
    day_4();
}
