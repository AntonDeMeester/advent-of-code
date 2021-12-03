use std::fs;

#[derive(Debug)]
struct Command {
    amount: i32,
    direction: String,
}

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> Vec<Command> {
    let mut result = Vec::<Command>::new();
    for l in lines {
        let splitted: Vec<String> = l.split_ascii_whitespace().map(|s| s.to_string()).collect();
        result.push(Command {
            amount: splitted[1].parse().unwrap(),
            direction: (*splitted[0]).to_string(),
        });
    }
    result
}

fn execute_commands_one(commands: &Vec<Command>) -> (i32, i32) {
    let (mut depth, mut distance) = (0, 0);
    for c in commands {
        match c.direction.as_str() {
            "forward" => distance += c.amount,
            "down" => depth += c.amount,
            "up" => depth -= c.amount,
            _ => panic!("Cannot parse command {:?}", c),
        };
    }
    (depth, distance)
}

fn execute_commands_two(commands: &Vec<Command>) -> (i32, i32) {
    let (mut aim, mut depth, mut distance) = (0, 0, 0);
    for c in commands {
        match c.direction.as_str() {
            "forward" => {
                distance += c.amount;
                depth += aim * c.amount;
            }
            "down" => aim += c.amount,
            "up" => aim -= c.amount,
            _ => panic!("Cannot parse command {:?}", c),
        };
    }
    (depth, distance)
}

fn main() {
    let filename = "2021/day_2/input.txt";
    let lines = read_file(filename);
    let parsed_commands = parse_lines(&lines);
    // let (depth, distance) = execute_commands_one(&parsed_commands); // Part 1
    let (depth, distance) = execute_commands_two(&parsed_commands); // Part 2
    println!(
        "We went {depth}m deep and {length}m far, totalling {total}",
        depth = depth,
        length = distance,
        total = depth * distance
    );
}
