package main

import (
	"adventofcode/adventUtils"
	"fmt"
)

var DIRECTIONS = [8][2]int{{1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}, {-1, -1}, {0, -1}, {1, -1}}

func parseLines(l []string) [][]int {
	res := [][]int{}
	for _, row := range l {
		rowRes := []int{}
		for _, elem := range []rune(row) {
			rowRes = append(rowRes, int(elem-'0'))
		}
		res = append(res, rowRes)
	}
	return res
}

func increase(state [][]int, x int, y int) [][]int {
	if state[x][y] < 9 {
		state[x][y] += 1
		return state
	}
	if state[x][y] > 9 {
		return state
	}

	state[x][y] += 1 // Increase to make sure you keep track of who flashes
	for _, d := range DIRECTIONS {
		xi, xj := x+d[0], y+d[1]
		if xi >= 0 && xi < len(state) && xj >= 0 && xj < len(state[0]) {
			state = increase(state, xi, xj)
		}
	}
	return state
}

func simulateStep(state [][]int) ([][]int, int) {
	copied := make([][]int, len(state))
	for i, row := range state {
		copyRow := make([]int, len(state[0]))
		copy(copyRow, row)
		copied[i] = copyRow
	}

	for i := 0; i < len(copied); i++ {
		for j := 0; j < len(copied[0]); j++ {
			copied = increase(copied, i, j)
		}
	}
	// Reset 10s
	flashes := 0
	for i, row := range copied {
		for j, elem := range row {
			if elem == 10 {
				flashes += 1
				copied[i][j] = 0
			}
		}
	}
	return copied, flashes
}

func countFlashes(state [][]int) int {
	flashes := 0
	for i := 0; i < 100; i++ {
		var newFlashes int
		state, newFlashes = simulateStep(state)
		flashes += newFlashes
	}
	return flashes
}

func allFlash(state [][]int) bool {
	for _, row := range state {
		for _, elem := range row {
			if elem != 0 {
				return false
			}
		}
	}
	return true
}

func findFirstSimul(state [][]int) int {
	for i := 0; i < 100000; i++ {
		state, _ = simulateStep(state)
		if allFlash(state) {
			return i + 1
		}
	}
	panic("Could not find simultaneous flashing after 100000 rounds")
}

func day11() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 11)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	initial := parseLines(rawLines)

	// Part 1
	flashes := countFlashes(initial)
	fmt.Printf("The total number of flashes is %d\n", flashes)

	// Part 2
	firstAllFlash := findFirstSimul(initial)
	fmt.Printf("The first time everything lights up is after %d steps\n", firstAllFlash)

}

func main() {
	adventUtils.Benchmark(day11)
}
