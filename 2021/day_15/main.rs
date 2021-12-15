use std::cmp;
use std::collections::binary_heap::BinaryHeap;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::time::Instant;

const DIRECTIONS: [(i32, i32); 4] = [(1, 0), (0, 1), (-1, 0), (0, -1)];

#[derive(cmp::PartialEq, cmp::Eq, cmp::PartialOrd, cmp::Ord)]
struct HeapPosition {
    estimate: i32,
    coord: (i32, i32),
}

fn parse_file(path: &str) -> HashMap<(i32, i32), i32> {
    let parsed = fs::read_to_string(path).expect("Could not read file");
    let raw_cave = parsed.lines().into_iter().map(|line| {
        line.chars().into_iter().map(|c| {
            c.to_string()
                .parse::<i32>()
                .expect("Could not parse character to number")
        })
    });
    let mut cave = HashMap::<(i32, i32), i32>::new();
    for (i, l) in raw_cave.enumerate() {
        for (j, e) in l.enumerate() {
            cave.insert((i as i32, j as i32), e);
        }
    }
    cave
}

fn a_star_search(cave: &HashMap<(i32, i32), i32>) -> i32 {
    let mut score = HashMap::<(i32, i32), i32>::new();
    let mut guess = HashMap::<(i32, i32), i32>::new();

    let (mut max_x, mut max_y) = (0, 0);
    for (k, _) in cave {
        score.insert(*k, i32::MAX);
        guess.insert(*k, 0);
        max_x = cmp::max(max_x, k.0);
        max_y = cmp::max(max_y, k.1);
    }

    let mut to_check = BinaryHeap::new();
    let mut to_check_set = HashSet::new();
    to_check.push(cmp::Reverse(HeapPosition {
        estimate: max_x + max_y,
        coord: (0, 0),
    }));
    to_check_set.insert((0, 0));
    score.insert((0, 0), 0);
    let goal = (max_x, max_y);

    while !to_check.is_empty() {
        let current = to_check.pop().expect("Could not find a new item").0;
        if current.coord == goal {
            return score[&current.coord];
        }
        to_check_set.remove(&current.coord);

        let current_cost = score[&current.coord];

        for d in DIRECTIONS {
            let next = (current.coord.0 + d.0, current.coord.1 + d.1);
            let enter_cost: i32;
            match cave.get(&next) {
                Some(v) => enter_cost = *v,
                None => continue,
            }

            let next_cost = score[&next];
            let tentative = current_cost + enter_cost;
            if tentative > next_cost {
                continue;
            }
            score.insert(next, tentative);
            guess.insert(next, tentative + (max_x - next.0) + (max_y - next.1));
            if !to_check_set.contains(&next) {
                to_check_set.insert(next);
                to_check.push(cmp::Reverse(HeapPosition {
                    coord: next,
                    estimate: tentative,
                }))
            }
        }
    }
    panic!("Could not find the path")
}

fn big_risk_search(cave: &HashMap<(i32, i32), i32>) -> i32 {
    let mut big_cave = HashMap::new();

    let (mut max_x, mut max_y) = (0, 0);
    for (k, _) in cave {
        max_x = cmp::max(max_x, k.0);
        max_y = cmp::max(max_y, k.1);
    }

    for i in 0..5 {
        for j in 0..5 {
            for (k, v) in cave {
                let next = (k.0 + max_x * i, k.1 + max_y * j);
                big_cave.insert(next, (v - 1 + i + j) % 9 + 1);
            }
        }
    }
    a_star_search(&big_cave)
}

fn day_15() {
    let filename = "2021/day_15/input.txt";
    let cave = parse_file(filename);

    // Part 1
    let risk = a_star_search(&cave);
    println!("The total risk is {}", risk);

    // Part 2
    let big_risk = big_risk_search(&cave);
    println!("The total risk for the big champer is {}", big_risk);
}

fn main() {
    let now = Instant::now();
    day_15();
    println!("Rust took {} microseconds", now.elapsed().as_micros());
}
