package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readFile(fileName string) ([]string, error) {
	data, err := os.ReadFile(fileName)
	if err != nil {
		return nil, err
	}
	parsed := string(data)
	split := strings.Split(parsed, "\n")
	return split, nil
}

func parseToInt(s []string) []int {
	numbered_lines := []int{}
	for _, line := range s {
		if line == "" {
			continue
		}
		parsed, err := strconv.Atoi(line)
		if err != nil {
			panic(err)
		}
		numbered_lines = append(numbered_lines, parsed)
	}
	return numbered_lines

}

func checkIncreasing(l []int) []bool {
	previous := 10000000
	result := []bool{}
	for _, current := range l {
		result = append(result, previous < current)
		previous = current
	}
	return result
}

func checkIncreasingSliding(l []int) []bool {
	window := [3]int{0, 0, 0}
	result := []bool{}
	for i, v := range l {
		if i >= 3 {
			result = append(result, v > window[0])
		}
		window = [3]int{window[1], window[2], v}
	}
	return result
}

func countTrue(l []bool) int {
	result := 0
	for _, value := range l {
		if value == true {
			result += 1
		}
	}
	return result
}

func main() {
	filename := "input.txt"
	lines, err := readFile(filename)
	if err != nil {
		lines, err = readFile(fmt.Sprintf("2021/day_1/%s", filename))
		if err != nil {
			panic(err)
		}
	}
	numbers := parseToInt(lines)
	// increasing := checkIncreasing(numbers) // Part 1
	increasing := checkIncreasingSliding(numbers) // Part 2
	countIncreasing := countTrue(increasing)
	fmt.Printf("There are %d increasing values in the list", countIncreasing)
}
