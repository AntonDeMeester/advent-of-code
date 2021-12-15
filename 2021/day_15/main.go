package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
)

type coord [2]int
type cave map[coord]int

var DIRECTIONS = [4]coord{coord{1, 0}, coord{0, 1}, coord{-1, 0}, coord{0, -1}}

func parseLines(l []string) cave {
	coordMap := cave{}
	for i, row := range l {
		for j, value := range []rune(row) {
			v := int(value) - '0'
			coordMap[coord{i, j}] = v
		}
	}
	return coordMap
}

func getMinGuess(coords []coord, guessMap map[coord]int) (coord, []coord) {
	var min coord
	minIndex := 0
	minCost := math.MaxInt32
	for i, c := range coords {
		if v, _ := guessMap[c]; v < minCost {
			min = c
			minCost = v
			minIndex = i
		}
	}
	coords[minIndex] = coords[len(coords)-1]
	return min, coords[:len(coords)-1]
}

func isInCoord(i coord, l []coord) bool {
	for _, j := range l {
		if i == j {
			return true
		}
	}
	return false
}

func findLowRiskRoute(c cave) int {
	// Stolen from https://en.wikipedia.org/wiki/A*_search_algorithm
	score := map[coord]int{}
	guess := map[coord]int{}

	maxX, maxY := 0, 0

	for k := range c {
		score[k] = math.MaxInt32
		guess[k] = 0
		if k[0] > maxX {
			maxX = k[0]
		}
		if k[1] > maxY {
			maxY = k[1]
		}
	}

	start := coord{0, 0}
	goal := coord{maxX, maxY}

	toCheck := []coord{start}
	current := start

	score[start] = 0
	guess[start] = maxX + maxY

	for len(toCheck) > 0 {
		current, toCheck = getMinGuess(toCheck, guess)
		if current == goal {
			s, ok := score[current]
			if !ok {
				panic("Something went wrong")
			}
			return s
		}

		currCost, _ := score[current]

		for _, d := range DIRECTIONS {
			next := coord{current[0] + d[0], current[1] + d[1]}
			enterCost, ok := c[next]
			if !ok {
				continue
			}

			nextCost, _ := score[next]
			tentativeCost := currCost + enterCost
			if tentativeCost > nextCost {
				continue
			}
			score[next] = tentativeCost
			guess[next] = tentativeCost + (maxX - next[0]) + (maxY - next[1])
			if !isInCoord(next, toCheck) {
				toCheck = append(toCheck, next)
			}
		}
	}

	panic("Could not reach goal")
}

func findBigLowRiskRoute(c cave) int {
	newCave := cave{}
	maxX, maxY := 0, 0
	for k := range c {
		if k[0]+1 > maxX {
			maxX = k[0] + 1
		}
		if k[1]+1 > maxY {
			maxY = k[1] + 1
		}
	}
	for i := 0; i < 5; i++ {
		for j := 0; j < 5; j++ {
			for k, v := range c {
				next := coord{k[0] + maxX*i, k[1] + maxX*j}
				newCave[next] = (v-1+i+j)%9 + 1
			}
		}
	}
	return findLowRiskRoute(newCave)
}

func day15() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 15)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	c := parseLines(rawLines)

	// Part 1
	risk := findLowRiskRoute(c)
	fmt.Printf("The total riskiness is %d\n", risk)

	// Part 2
	bigRisk := findBigLowRiskRoute(c)
	fmt.Printf("The total riskiness of the big map is %d\n", bigRisk)

}

func main() {
	adventUtils.Benchmark(day15)
}
