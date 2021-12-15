package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strings"
)

func parseLines(l []string) (data []rune, templates map[string]rune) {
	data = []rune{}
	for _, r := range l[0] {
		data = append(data, r)
	}

	templates = map[string]rune{}
	for _, l := range l[2:] {
		s := strings.Split(l, " -> ")
		templates[s[0]] = rune(s[1][0])
	}
	return
}

func iteration(polymer []rune, templates map[string]rune) []rune {
	res := []rune{}
	for i := 0; i < len(polymer)-1; i++ {
		res = append(res, polymer[i])
		combo := string([]rune{polymer[i], polymer[i+1]})
		if value, ok := templates[combo]; ok {
			res = append(res, value)
		}
	}
	res = append(res, polymer[len(polymer)-1])
	return res
}

func findMaxMinusMin(polymer []rune) int {
	counts := map[rune]int{}
	for _, r := range polymer {
		if _, ok := counts[r]; ok {
			counts[r] += 1
		} else {
			counts[r] = 1
		}
	}
	max := 0
	min := 1000000
	for _, v := range counts {
		if v > max {
			max = v
		}
		if v < min {
			min = v
		}
	}
	return max - min
}

func findMaxMinusMinMap(polymer map[string]int, first rune, last rune) int {
	counts := map[rune]int{}
	for key, value := range polymer {
		f := rune(key[0])
		addToMapWithDefaultRune(counts, f, value)
		s := rune(key[1])
		addToMapWithDefaultRune(counts, s, value)
	}
	counts[first] += 1
	counts[last] += 1

	max := 0
	min := 1000000000000000000
	for _, v := range counts {
		if v > max {
			max = v
		}
		if v < min {
			min = v
		}
	}
	return (max - min) / 2
}

func partOne(polymer []rune, templates map[string]rune) int {
	for i := 0; i < 10; i++ {
		polymer = iteration(polymer, templates)
	}
	return findMaxMinusMin(polymer)
}

func addToMapWithDefault(m map[string]int, key string, value int) map[string]int {
	if _, ok := m[key]; ok {
		m[key] += value
	} else {
		m[key] = value
	}
	return m
}

func addToMapWithDefaultRune(m map[rune]int, key rune, value int) map[rune]int {
	if _, ok := m[key]; ok {
		m[key] += value
	} else {
		m[key] = value
	}
	return m
}

func iterationWithMap(polymer map[string]int, templates map[string]rune) map[string]int {
	newMap := map[string]int{}
	for key, amount := range polymer {
		if middle, ok := templates[key]; ok {
			left := string([]rune{rune(key[0]), middle})
			addToMapWithDefault(newMap, left, amount)

			right := string([]rune{middle, rune(key[1])})
			addToMapWithDefault(newMap, right, amount)
		} else {
			addToMapWithDefault(newMap, key, amount)
		}
	}
	return newMap
}

func parseToMap(polymer []rune) map[string]int {
	polymerMap := map[string]int{}
	for i := 0; i < len(polymer)-1; i++ {
		combo := string([]rune{polymer[i], polymer[i+1]})
		if _, ok := polymerMap[combo]; ok {
			polymerMap[combo] += 1
		} else {
			polymerMap[combo] = 1
		}
	}
	return polymerMap
}

func partTwo(polymer []rune, templates map[string]rune) int {
	polymerMap := parseToMap(polymer)
	for i := 0; i < 40; i++ {
		polymerMap = iterationWithMap(polymerMap, templates)
	}
	return findMaxMinusMinMap(polymerMap, polymer[0], polymer[len(polymer)-1])
}

func day14() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 14)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	data, templates := parseLines(rawLines)

	// Part 1
	c := partOne(data, templates)
	fmt.Printf("After 10 iterations, the difference between the most and least used polymer is %d\n", c)

	// Part 2
	cMore := partTwo(data, templates)
	fmt.Printf("After 40 iterations, the difference between the most and least used polymer is %d\n", cMore)

}

func main() {
	adventUtils.Benchmark(day14)
}
