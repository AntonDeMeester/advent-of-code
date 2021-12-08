use std::fs;
use std::time::Instant;

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> Vec<i64> {
    lines[0]
        .split(",")
        .map(|i| i.parse::<i64>().expect("Could not parse number"))
        .collect()
}

fn parse_to_map(fish: &Vec<i64>) -> [i64; 9] {
    let mut res = [0; 9];
    for f in fish {
        res[(*f) as usize] += 1;
    }
    res
}

fn pass_day(fish_map: &[i64; 9]) -> [i64; 9] {
    let mut new_map = [0; 9];
    for i in (1..9).rev() {
        new_map[i - 1] = fish_map[i];
    }
    new_map[8] = fish_map[0];
    new_map[6] += fish_map[0];
    new_map
}

fn count_after_days(fish_map: &[i64; 9], days: i32) -> i64 {
    let mut after_day = *fish_map;
    for _ in 0..days {
        after_day = pass_day(&after_day);
    }
    let mut res = 0;
    for i in after_day {
        res += i;
    }
    res
}

fn day_6() {
    let filename = "2021/day_6/input_easy.txt";
    let lines = read_file(filename);
    let fishes = parse_lines(&lines);
    let fish_map = parse_to_map(&fishes);

    // Part 1
    let fish_80 = count_after_days(&fish_map, 80);
    println!("After 80 days there are {} fish!", fish_80);

    // Part 2
    let fish_256 = count_after_days(&fish_map, 256);
    println!("After 256 days there are {} fish!", fish_256);
}

fn main() {
    let now = Instant::now();
    day_6();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
