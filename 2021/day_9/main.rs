use std::collections::HashSet;
use std::fs;
use std::time::Instant;

const DIRECTIONS: [[i32; 2]; 4] = [[1, 0], [0, 1], [-1, 0], [0, -1]];

fn parse_file(path: &str) -> Vec<Vec<i32>> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let split_lines = parsed.lines();
    split_lines
        .map(|s| {
            s.chars()
                .into_iter()
                .map(|c| {
                    c.to_string()
                        .parse::<i32>()
                        .expect("Could not parse character to number")
                })
                .collect()
        })
        .collect()
}

fn get_surrounding(point: &[i32; 2], map: &Vec<Vec<i32>>) -> [i32; 4] {
    let mut res = [-1; 4];
    for (i, d) in DIRECTIONS.iter().enumerate() {
        let (next_x, next_y) = (point[0] + d[0], point[1] + d[1]);
        if next_x >= 0 && next_x < map.len() as i32 && next_y >= 0 && next_y < map[0].len() as i32 {
            res[i] = map[next_x as usize][next_y as usize];
        }
    }
    res
}

fn is_lowest(point: &[i32; 2], map: &Vec<Vec<i32>>) -> bool {
    let surrounding = get_surrounding(point, map);
    let value = map[point[0] as usize][point[1] as usize];
    surrounding.iter().all(|x| value < *x || *x == -1)
}

fn sum_minima(map: &Vec<Vec<i32>>) -> i32 {
    let mut result = 0;
    for (i, row) in map.iter().enumerate() {
        for (j, element) in row.iter().enumerate() {
            if is_lowest(&[i as i32, j as i32], map) {
                result += element + 1;
            }
        }
    }
    result
}

fn multiply_basins(map: &Vec<Vec<i32>>) -> i32 {
    let mut largest_basins = [0, 0, 0];
    for (i, row) in map.iter().enumerate() {
        for j in 0..row.len() {
            let point = [i as i32, j as i32];
            if is_lowest(&point, map) {
                let size = find_basin_size(&point, map);
                if size > largest_basins[0] {
                    largest_basins[0] = size;
                    largest_basins.sort();
                }
            }
        }
    }
    largest_basins[0] * largest_basins[1] * largest_basins[2]
}

fn find_basin_size(point: &[i32; 2], map: &Vec<Vec<i32>>) -> i32 {
    let mut to_check = vec![*point];
    let mut checked = HashSet::<[i32; 2]>::new();
    let mut res = 0;
    let (max_x, max_y) = (map.len() as i32, map[0].len() as i32);

    while !to_check.is_empty() {
        let current = to_check.pop().expect("We checked for emptiness before");

        // Skip is we already visited
        if !checked.insert(current) {
            continue;
        }
        // Skip height 9
        if map[current[0] as usize][current[1] as usize] == 9 {
            continue;
        }

        res += 1;
        // Add new lines
        for d in DIRECTIONS {
            let (next_x, next_y) = (current[0] + d[0], current[1] + d[1]);
            if next_x >= 0 && next_x < max_x && next_y >= 0 && next_y < max_y {
                to_check.push([next_x, next_y]);
            }
        }
    }
    res
}

fn day_8() {
    let filename = "2021/day_9/input.txt";
    let map = parse_file(filename);

    // Part 1
    let sum_minima = sum_minima(&map);
    println!("The sum of the lowest points are {}", sum_minima);

    // Part 2
    let multiply_basins = multiply_basins(&map);
    println!("The product of all basin sizes {}", multiply_basins);
}

fn main() {
    let now = Instant::now();
    day_8();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
