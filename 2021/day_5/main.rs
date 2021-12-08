use std::cmp::Ordering;
use std::convert::TryInto;
use std::fs;
use std::time::Instant;

#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Copy, Clone)]
struct Line {
    start: Point,
    end: Point,
}

fn read_file(path: &str) -> Vec<String> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines.map(|s| s.to_string()).collect()
}

fn parse_lines(lines: &Vec<String>) -> Vec<Line> {
    let mut parsed = Vec::<Line>::new();

    for l in lines {
        let parsed_line: Vec<Vec<i32>> = l
            .split(" -> ")
            .map(|s| {
                s.split(",")
                    .map(|i| i.parse::<i32>().expect("Could not parse coordinate to int"))
                    .collect()
            })
            .collect();
        parsed.push(Line {
            start: Point {
                x: parsed_line[0][0],
                y: parsed_line[0][1],
            },
            end: Point {
                x: parsed_line[1][0],
                y: parsed_line[1][1],
            },
        });
    }

    return parsed;
}

fn create_map(lines: &Vec<Line>) -> Vec<Vec<i8>> {
    let (mut max_x, mut max_y) = (0, 0);
    for l in lines {
        if l.start.x > max_x {
            max_x = l.start.x;
        }
        if l.end.x > max_x {
            max_x = l.end.x;
        }
        if l.start.y > max_y {
            max_y = l.start.y;
        }
        if l.end.y > max_y {
            max_y = l.end.y;
        }
    }
    let mut map = vec![vec![0; (max_y + 1).try_into().unwrap()]; (max_x + 1).try_into().unwrap()];
    for l in lines {
        let (dx, dy) = get_direction(&l.start, &l.end);
        let (mut curr_x, mut curr_y) = (l.start.x, l.start.y);
        while curr_x != l.end.x || curr_y != l.end.y {
            map[curr_x as usize][curr_y as usize] += 1;
            curr_x += dx;
            curr_y += dy;
        }
        map[curr_x as usize][curr_y as usize] += 1;
    }
    map
}

fn get_direction(start: &Point, end: &Point) -> (i32, i32) {
    let dx = match end.x.cmp(&start.x) {
        Ordering::Greater => 1,
        Ordering::Equal => 0,
        Ordering::Less => -1,
    };
    let dy = match end.y.cmp(&start.y) {
        Ordering::Greater => 1,
        Ordering::Equal => 0,
        Ordering::Less => -1,
    };
    (dx, dy)
}

fn count_dangerous(map: Vec<Vec<i8>>) -> i32 {
    let mut res = 0;
    for row in map {
        for element in row {
            if element > 1 {
                res += 1;
            }
        }
    }
    res
}

fn count_straight_geisers(lines: &Vec<Line>) -> i32 {
    let straight: Vec<Line> = lines
        .into_iter()
        .filter(|l| l.start.x == l.end.x || l.start.y == l.end.y)
        .cloned()
        .collect();
    let map = create_map(&straight);
    count_dangerous(map)
}

fn count_geisers(lines: &Vec<Line>) -> i32 {
    let map = create_map(&lines);
    count_dangerous(map)
}

fn day_5() {
    let filename = "2021/day_5/input.txt";
    let lines = read_file(filename);
    let parsed_lines = parse_lines(&lines);

    // Part 1
    let dangerious_straights = count_straight_geisers(&parsed_lines);
    println!(
        "There are {} dangerious places for the geiser considering only hor and vert",
        dangerious_straights
    );

    // Part 2
    let dangerious = count_geisers(&parsed_lines);
    println!(
        "There are {} dangerious places for the geiser \n",
        dangerious
    );
}

fn main() {
    let now = Instant::now();
    day_5();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
