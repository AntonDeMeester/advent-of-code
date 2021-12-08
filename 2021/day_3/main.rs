use std::cmp::Ordering;
use std::fs;
use std::time::Instant;

#[derive(Debug, Copy, Clone)]
struct BitCount {
    zero: i32,
    one: i32,
}

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn count_bits(lines: &Vec<String>) -> Vec<BitCount> {
    let mut result = vec![BitCount { zero: 0, one: 0 }; lines[0].len()];
    for l in lines {
        for (i, c) in l.chars().enumerate() {
            match c {
                '1' => result[i].one += 1,
                '0' => result[i].zero += 1,
                _ => panic!("Could not parse line {:?}", c),
            }
        }
    }
    result
}

fn calculate_power(lines: &Vec<String>) -> (i32, i32) {
    let parsed = count_bits(&lines);
    let (mut gamma, mut epsilon) = (0, 0);
    for b in parsed {
        gamma *= 2;
        epsilon *= 2;
        match b.one > b.zero {
            true => gamma += 1,
            false => epsilon += 1,
        }
    }
    (gamma, epsilon)
}

fn calculate_life_metrics(lines: &Vec<String>, invert: bool) -> i32 {
    let mut filtered_lines = lines.clone();
    for i in 0..lines[0].len() {
        if filtered_lines.len() <= 1 {
            break;
        }
        let parsed = count_bits(&filtered_lines);
        let bit = parsed[i];
        let filter_char = match (bit.one.cmp(&bit.zero), invert) {
            (Ordering::Greater, false) => '1',
            (Ordering::Equal, false) => '1',
            (Ordering::Less, false) => '0',
            (Ordering::Greater, true) => '0',
            (Ordering::Equal, true) => '0',
            (Ordering::Less, true) => '1',
        };
        filtered_lines = filtered_lines
            .into_iter()
            .filter(|line| (line.as_bytes()[i] as char) == filter_char)
            .collect();
    }
    if filtered_lines.len() != 1 {
        panic!("Filtered lines does not have size 1, {:?}", filtered_lines);
    }
    i32::from_str_radix(&filtered_lines[0].to_string(), 2).unwrap()
}

fn calculate_life_support(lines: &Vec<String>) -> (i32, i32) {
    (
        calculate_life_metrics(&lines, false),
        calculate_life_metrics(&lines, true),
    )
}

fn day_3() {
    let filename = "2021/day_3/input.txt";
    let lines = read_file(filename);
    let (gamma, epsilon) = calculate_power(&lines); // Part 1
    println!(
        "Epsilon is {epsilon}, gamma is {gamma}. The total power consumptions is {total}",
        epsilon = epsilon,
        gamma = gamma,
        total = gamma * epsilon
    );
    let (oxygen, co2) = calculate_life_support(&lines); // Part 2
    println!(
        "Oxygen is {oxygen}, CO2 is {co2}. The total life support is {total}",
        oxygen = oxygen,
        co2 = co2,
        total = oxygen * co2
    );
}

fn main() {
    let now = Instant::now();
    day_3();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
