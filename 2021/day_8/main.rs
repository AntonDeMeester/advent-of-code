use std::collections::HashMap;
use std::fs;
use std::iter::FromIterator;
use std::time::Instant;

#[derive(Debug)]
struct Pattern {
    signals: Vec<String>,
    output: Vec<String>,
}

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> Vec<Pattern> {
    let mut res = Vec::<Pattern>::new();
    for l in lines {
        let values: Vec<&str> = l.split(" | ").collect();
        res.push(Pattern {
            signals: values[0]
                .split_whitespace()
                .map(|s| s.to_string())
                .collect(),
            output: values[1]
                .split_whitespace()
                .map(|s| s.to_string())
                .collect(),
        })
    }
    res
}

fn count_1_4_7_8(pattern: &Pattern) -> i32 {
    let mut res = 0;
    for o in &pattern.output {
        if vec![2, 3, 4, 7].contains(&o.len()) {
            res += 1;
        }
    }
    res
}

fn part_one(patterns: &Vec<Pattern>) -> i32 {
    let mut res = 0;
    for p in patterns {
        res += count_1_4_7_8(&p)
    }
    res
}

fn part_two(patterns: &Vec<Pattern>) -> i32 {
    let mut res = 0;
    for p in patterns {
        let normalized = normalize_pattern(p);
        let solution = solve_signals(&normalized.signals);
        res += make_number(&normalized.output, &solution);
    }
    res
}

fn normalize_pattern(pattern: &Pattern) -> Pattern {
    Pattern {
        signals: pattern
            .signals
            .clone()
            .into_iter()
            .map(|x| {
                let mut chars: Vec<char> = x.chars().collect();
                chars.sort();
                String::from_iter(chars)
            })
            .collect(),
        output: pattern
            .output
            .clone()
            .into_iter()
            .map(|x| {
                let mut chars: Vec<char> = x.chars().collect();
                chars.sort();
                String::from_iter(chars)
            })
            .collect(),
    }
}

fn solve_signals(signals: &Vec<String>) -> HashMap<String, i32> {
    let mut solutions = vec![String::new(); 10];
    let mut not_found_one = Vec::<String>::new();

    // Getting straight solutions from part one
    for s in signals {
        let matched_number: i32 = match s.len() {
            2 => 1,
            4 => 4,
            3 => 7,
            7 => 8,
            _ => -1,
        };
        if matched_number != -1 {
            solutions[matched_number as usize] = s.to_string();
        } else {
            not_found_one.push(s.to_string());
        }
    }

    // Get second order solutions
    // 3 based on 7 (2 extra as 7)
    // 9 based on 4 (2 extra as 4)
    // 0 based on 7 (0 has 3 more)
    // 6 based on 7( 6 has 4 not in 4, 4 has 1 not in 6)
    let mut not_found_two = Vec::<String>::new();
    for s in not_found_one {
        if get_overlap(&s, &solutions[7]) == (2, 0) {
            solutions[3] = s.to_string();
        } else if get_overlap(&s, &solutions[4]) == (2, 0) {
            solutions[9] = s.to_string();
        } else if get_overlap(&s, &solutions[7]) == (3, 0) {
            solutions[0] = s.to_string();
        } else if get_overlap(&s, &solutions[7]) == (4, 1) {
            solutions[6] = s.to_string();
        } else {
            not_found_two.push(s.to_string());
        }
    }

    // Third order
    // 5 based on 9 (9 has 1 more)
    // 2 based on 4 (2 overlap, 3 in 2 not in 4, 2 in 4 not in 2)
    for s in not_found_two {
        if get_overlap(&s, &solutions[9]) == (0, 1) {
            solutions[5] = s.to_string();
        } else if get_overlap(&s, &solutions[4]) == (3, 2) {
            solutions[2] = s.to_string();
        }
    }

    let mut res = HashMap::<String, i32>::new();
    for (i, v) in solutions.iter().enumerate() {
        res.insert(v.to_string(), i as i32);
    }
    res
}

fn get_overlap(one: &String, two: &String) -> (i8, i8) {
    let (mut one_not_two, mut two_not_one) = (0, 0);
    for c in one.chars() {
        if !two.contains(c) {
            one_not_two += 1;
        }
    }
    for c in two.chars() {
        if !one.contains(c) {
            two_not_one += 1;
        }
    }
    (one_not_two, two_not_one)
}

fn make_number(output: &Vec<String>, solution: &HashMap<String, i32>) -> i32 {
    let mut res = 0;
    for o in output {
        res *= 10;
        res += solution.get(o).unwrap();
    }
    res
}

fn day_8() {
    let filename = "2021/day_8/input.txt";
    let lines = read_file(filename);
    let patterns = parse_lines(&lines);

    // Part 1
    let count = part_one(&patterns);
    println!("The number of one, four, seven or eights is {}", count);

    // Part 2
    let count_2 = part_two(&patterns);
    println!("The total sum of signals is {}", count_2);
}

fn main() {
    let now = Instant::now();
    day_8();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
