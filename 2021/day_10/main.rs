use std::collections::HashMap;
use std::fs;
use std::time::Instant;

enum SyntaxError {
    Syntax(char),
    Incomplete(Vec<char>),
}

fn get_brackets() -> HashMap<char, char> {
    HashMap::<char, char>::from([('}', '{'), (']', '['), (')', '('), ('>', '<')])
}

fn get_syntax_costs() -> HashMap<char, i32> {
    HashMap::<char, i32>::from([(')', 3), (']', 57), ('}', 1197), ('>', 25137)])
}

fn get_incomplete_costs() -> HashMap<char, i32> {
    HashMap::<char, i32>::from([('(', 1), ('[', 2), ('{', 3), ('<', 4)])
}

fn parse_file(path: &str) -> Vec<Vec<char>> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.chars().collect()).collect()
}

fn get_error(chars: &Vec<char>) -> SyntaxError {
    let mut opens = Vec::<char>::new();
    let brackets = get_brackets();
    for c in chars {
        match brackets.get(&c) {
            Some(m) => {
                if *m != opens.pop().expect("Opening list is empty") {
                    return SyntaxError::Syntax(*c);
                }
            }
            None => {
                opens.push(*c);
            }
        };
    }
    return SyntaxError::Incomplete(opens);
}

fn calculate_syntax_cost(char_list: &Vec<Vec<char>>) -> i32 {
    let mut res = 0;
    let syntax_costs = get_syntax_costs();
    for l in char_list {
        match get_error(&l) {
            SyntaxError::Syntax(c) => {
                res += syntax_costs
                    .get(&c)
                    .expect(&format!["Could not find cost of {}", c]);
            }
            SyntaxError::Incomplete(_) => {}
        };
    }
    res
}

fn calculate_complete_cost(char_list: &Vec<Vec<char>>) -> i64 {
    let mut costs = Vec::<i64>::new();
    let incomplete_costs = get_incomplete_costs();
    for l in char_list {
        match get_error(&l) {
            SyntaxError::Syntax(_) => {}
            SyntaxError::Incomplete(to_close) => {
                let mut line_cost = 0;
                for c in to_close.iter().rev() {
                    let char_cost = incomplete_costs
                        .get(&c)
                        .expect(&format!["Could not find cost of {}", c]);
                    line_cost *= 5;
                    line_cost += (*char_cost) as i64;
                }
                costs.push(line_cost);
            }
        };
    }
    costs.sort();
    costs[((costs.len() - 1) / 2) as usize]
}

fn day_10() {
    let filename = "2021/day_10/input.txt";
    let char_list = parse_file(filename);

    // Part 1
    let syntax_cost = calculate_syntax_cost(&char_list);
    println!("The total syntax error cost is {}", syntax_cost);

    // // Part 2
    let complete_cost = calculate_complete_cost(&char_list);
    println!("The total complete error cost is {}", complete_cost);
}

fn main() {
    let now = Instant::now();
    day_10();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
