use std::fs;
use std::time::Instant;

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> Vec<i32> {
    lines[0]
        .split(",")
        .map(|i| i.parse::<i32>().expect("Could not parse number"))
        .collect()
}

fn find_min_fuel(crabs: &Vec<i32>) -> i32 {
    let max = crabs.iter().max().expect("Could not find maximum");
    let min = crabs.iter().min().expect("Could not find mininum");

    let mut min_fuel = 2147483647i32;

    for i in (*min)..(*max) {
        let mut fuel = 0i32;
        for c in crabs {
            fuel += i32::abs(c - i);
        }
        if fuel < min_fuel {
            min_fuel = fuel;
        }
    }
    min_fuel
}

fn find_min_fuel_complex(crabs: &Vec<i32>) -> i32 {
    let max = crabs.iter().max().expect("Could not find maximum");
    let min = crabs.iter().min().expect("Could not find mininum");

    let mut min_fuel = 2147483647i32;

    for i in (*min)..(*max) {
        let mut fuel = 0i32;
        for c in crabs {
            let dist = i32::abs(c - i);
            fuel += i32::from(dist * (dist + 1) / 2);
        }
        if fuel < min_fuel {
            min_fuel = fuel;
        }
    }
    min_fuel
}

fn day_7() {
    let filename = "2021/day_7/input.txt";
    let lines = read_file(filename);
    let crabs = parse_lines(&lines);

    // Part 1
    let min_easy = find_min_fuel(&crabs);
    println!("The minimum simple fuel is {}", min_easy);

    // Part 2
    let min_hard = find_min_fuel_complex(&crabs);
    println!("The minimum complex fuel is {}", min_hard);
}

fn main() {
    let now = Instant::now();
    day_7();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
