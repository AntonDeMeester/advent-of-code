package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"sort"
)

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

func getSurrounding(l [2]int, m [][]int) [4]int {
	res := [4]int{}
	dir := [4][2]int{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	maxX := len(m)
	maxY := len(m[0])
	for i, d := range dir {
		nextX, nextY := l[0]+d[0], l[1]+d[1]
		if nextX >= 0 && nextX < maxX && nextY >= 0 && nextY < maxY {
			res[i] = m[nextX][nextY]
		} else {
			res[i] = -1
		}
	}
	return res
}

func isLowest(l [2]int, m [][]int) bool {
	elem := m[l[0]][l[1]]
	sur := getSurrounding(l, m)
	for _, s := range sur {
		if s != -1 {
			if elem >= s {
				return false
			}
		}
	}
	return true
}

func isHighest(l [2]int, m [][]int) bool {
	elem := m[l[0]][l[1]]
	sur := getSurrounding(l, m)
	for _, s := range sur {
		if s != -1 {
			if elem < s {
				return false
			}
		}
	}
	return true
}

func sumMinima(m [][]int) int {
	res := 0
	for i, row := range m {
		for j, elem := range row {
			if isLowest([2]int{i, j}, m) {
				res += elem + 1
			}
		}
	}
	return res
}

func pop(l [][2]int) ([2]int, [][2]int) {
	return l[0], l[1:]
}

func findBasinSize(l [2]int, m [][]int) int {
	toCheck := [][2]int{l}
	checked := map[[2]int]bool{}
	res := 0
	dir := [4][2]int{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	maxX, maxY := len(m), len(m[0])
	for {
		if len(toCheck) == 0 {
			break
		}
		currCheck := toCheck[0]
		toCheck = toCheck[1:]
		// Skip if we already visited
		if _, ok := checked[currCheck]; ok {
			continue
		}
		checked[currCheck] = true
		// If we are at a local maximum, we skip
		if m[currCheck[0]][currCheck[1]] == 9 {
			continue
		}
		res += 1
		// Add next ones
		for _, d := range dir {
			next := [2]int{currCheck[0] + d[0], currCheck[1] + d[1]}
			//Skip if it falls outside the grid
			if next[0] < 0 || next[0] >= maxX || next[1] < 0 || next[1] >= maxY {
				continue
			}
			toCheck = append(toCheck, next)
		}
	}
	return res
}

func multiplyBasins(m [][]int) int {
	res := [3]int{0, 0, 0}
	for i, row := range m {
		for j, _ := range row {
			if isLowest([2]int{i, j}, m) {
				size := findBasinSize([2]int{i, j}, m)
				if size > res[0] {
					res[0] = size
					toSort := res[:]
					sort.Ints(toSort)
					copy(res[:], toSort)
				}
			}
		}
	}
	return res[0] * res[1] * res[2]
}

func day8() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 9)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	patterns := parseLines(rawLines)

	// Part 1
	sumMin := sumMinima(patterns)
	fmt.Printf("The sum of the lowest points are %d\n", sumMin)

	// Part 2
	mulSize := multiplyBasins(patterns)
	fmt.Printf("The product of all basin sizes %d\n", mulSize)

}

func main() {
	adventUtils.Benchmark(day8)
}
