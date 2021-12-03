use std::fs;

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_to_int(lines: &Vec<String>) -> Vec<i32> {
    let mut result = Vec::<i32>::new();
    for value in lines {
        result.push(value.parse().unwrap());
    }
    result
}

fn check_increasing(values: &Vec<i32>) -> Vec<bool> {
    let mut previous: i32 = 100000000;
    let mut result = Vec::<bool>::new();
    for value in values {
        result.push(*value > previous);
        previous = *value;
    }
    result
}

fn check_increasing_sliding(values: &Vec<i32>) -> Vec<bool> {
    let mut window = (0, 0, 0);
    let mut result = Vec::<bool>::new();
    for (i, value) in values.iter().enumerate() {
        if i >= 3 {
            result.push(*value > window.0);
        }
        window = (window.1, window.2, *value);
    }
    result
}

fn count_true(values: &Vec<bool>) -> i32 {
    values.iter().fold(0, |c, item| c + (*item as i32))
}

fn main() {
    let filename = "2021/day_1/input.txt";
    let lines = read_file(filename);
    let numbers = parse_to_int(&lines);
    // let increasing = check_increasing(&numbers); // Part 1
    let increasing = check_increasing_sliding(&numbers); // Part 2
    let count = count_true(&increasing);
    println!("There are {:?} increasing steps", count);
}
