package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strings"
)

type bingoPattern struct {
	numbers [5][5]int
	state   [5][5]bool
}

type bingoResult struct {
	p      bingoPattern
	rounds []int
}

type bit struct {
	zero int
	one  int
}

func removeEmpty(i []string) []string {
	r := []string{}
	for _, s := range i {
		if s != "" {
			r = append(r, s)
		}
	}
	return r
}

func parseLines(lines []string) ([]int, []bingoPattern) {
	firstLine := strings.Split(lines[0], ",")
	calledNumbers, err := adventUtils.ParseToInt(firstLine)
	if err != nil {
		// for _, e := range err {
		// 	fmt.Errorf("Error at %d: %+v\n", e.err, e.err)
		// }
		panic(err)
	}

	index := 2
	patterns := []bingoPattern{}
	for {
		if index > len(lines) {
			break
		}
		p := bingoPattern{}
		for j := 0; j < 5; j++ {
			nextLine := removeEmpty(strings.Split(lines[index+j], " "))
			bingoNumbers, err := adventUtils.ParseToInt(nextLine)
			if err != nil {
				panic(err)
			}
			copy(p.numbers[j][:], bingoNumbers[:5])
		}
		patterns = append(patterns, p)
		index += 6
	}

	return calledNumbers, patterns
}

func playBingo(called []int, patterns []bingoPattern) (bingoPattern, []int) {
	for i := 1; i <= len(called); i++ {
		s := called[:i]
		for _, p := range patterns {
			success, state := resolveBingo(s, p)
			p.state = state
			if success {
				return p, called[:i]
			}
		}
	}
	panic("Could not resolve Bingo")
}

func resolveBingo(n []int, p bingoPattern) (bool, [5][5]bool) {
	var state [5][5]bool
	for i := 0; i < len(p.numbers); i++ {
		for j := 0; j < len(p.numbers[i]); j++ {
			for _, c := range n {
				if p.numbers[i][j] == c {
					state[i][j] = true
					break
				}
			}
		}
	}
	for i := 0; i < len(p.numbers); i++ {
		if allTrue(state[i]) {
			return true, state
		}
		vert := [5]bool{state[0][i], state[1][i], state[2][i], state[3][i], state[4][i]}
		if allTrue(vert) {
			return true, state
		}
	}
	return false, state
}

func allTrue(i [5]bool) bool {
	for _, v := range i {
		if !v {
			return false
		}
	}
	return true
}

func calculateResult(p bingoPattern, r []int) int {
	left := 0
	for i := 0; i < len(p.numbers); i++ {
		for j := 0; j < len(p.numbers[i]); j++ {
			if !p.state[i][j] {
				left += p.numbers[i][j]
			}
		}
	}
	right := r[len(r)-1]

	return left * right
}

func loseBingo(called []int, patterns []bingoPattern) bingoResult {
	winners := []bingoResult{}
	winnerIndex := []int{}
	for i := 1; i <= len(called); i++ {
		s := called[:i]
		for j, p := range patterns {
			if adventUtils.IsIn(j, winnerIndex) {
				continue
			}
			success, state := resolveBingo(s, p)
			p.state = state
			if success {
				winners = append(winners, bingoResult{p: p, rounds: called[:i]})
				winnerIndex = append(winnerIndex, j)
			}
		}
	}

	return winners[len(winners)-1]
}

func day_4() {
	filename := "input.txt"
	lines, err := adventUtils.ReadFileAdvent(filename, 4)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	calledNumbers, bingo := parseLines(lines)

	pattern, rounds := playBingo(calledNumbers, bingo)
	result := calculateResult(pattern, rounds) // Part 1
	fmt.Printf("Bingo was resolved after %d rounds. Result is %d\n", len(rounds), result)
	lastResult := loseBingo(calledNumbers, bingo)
	lostResult := calculateResult(lastResult.p, lastResult.rounds) // Part 1
	fmt.Printf("Bingo was list after %d rounds. Result is %d\n", len(lastResult.rounds), lostResult)
}

func main() {
	adventUtils.Benchmark(day_4)
}
