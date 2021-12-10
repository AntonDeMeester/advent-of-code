package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"sort"
)

var BRACKETS = map[rune]rune{'}': '{', ']': '[', ')': '(', '>': '<'}
var SYNTAX_COSTS = map[rune]int{')': 3, ']': 57, '}': 1197, '>': 25137}
var COMPLETE_COSTS = map[rune]int{'(': 1, '[': 2, '{': 3, '<': 4}

func parseLines(l []string) [][]rune {
	res := [][]rune{}
	for _, row := range l {
		rowRes := []rune{}
		for _, elem := range []rune(row) {
			rowRes = append(rowRes, elem)
		}
		res = append(res, rowRes)
	}
	return res
}

func getError(l []rune) (rune, []rune) {
	opens := []rune{}
	for _, r := range l {
		match, isClose := BRACKETS[r]
		if isClose {
			if opens[len(opens)-1] != match {
				return r, nil
			} else {
				opens = opens[:len(opens)-1]
			}
		} else {
			opens = append(opens, r)
		}
	}
	return 0, opens
}

func calculateSyntaxCost(ls [][]rune) int {
	res := 0
	for _, l := range ls {
		c, _ := getError(l)
		// Only incomplete not errored
		if c == 0 {
			continue
		}
		cost, ok := SYNTAX_COSTS[c]
		if !ok {
			panic(fmt.Sprintf("Could not find cost of %c", c))
		}
		res += cost
	}
	return res
}

func calculateCompleteCost(ls [][]rune) int {
	lineCosts := []int{}
	for _, l := range ls {
		_, incomplete := getError(l)
		// Only incomplete not errored
		if incomplete == nil {
			continue
		}
		lineCost := 0
		for i := len(incomplete) - 1; i >= 0; i-- {
			c := incomplete[i]
			cost, ok := COMPLETE_COSTS[c]
			if !ok {
				panic(fmt.Sprintf("Could not find cost of %c", c))
			}
			lineCost *= 5
			lineCost += cost
		}
		lineCosts = append(lineCosts, lineCost)
	}
	sort.Ints(lineCosts)
	return lineCosts[(len(lineCosts)-1)/2]
}

func day10() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 10)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	runeList := parseLines(rawLines)

	// Part 1
	syntexCost := calculateSyntaxCost(runeList)
	fmt.Printf("The total syntax error cost is %d\n", syntexCost)

	// Part 2
	completeCost := calculateCompleteCost(runeList)
	fmt.Printf("The total complete error cost is %d\n", completeCost)

}

func main() {
	adventUtils.Benchmark(day10)
}
