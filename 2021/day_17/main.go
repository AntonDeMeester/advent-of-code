package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strconv"
	"strings"
)

type area [4]int

func parseInt(l string) int {
	n, err := strconv.Atoi(l)
	if err != nil {
		panic("Could not parse integer")
	}
	return n
}

func parseLines(l []string) area {
	splitOnCommma := strings.Split(l[0], ", ")
	splitX := strings.Split(splitOnCommma[0][len("target area: x="):], "..")
	splitY := strings.Split(splitOnCommma[1][len("y="):], "..")
	minX, maxX := parseInt(splitX[0]), parseInt(splitX[1])
	minY, maxY := parseInt(splitY[0]), parseInt(splitY[1])
	return area{minX, maxX, minY, maxY}
}

func fallsIn(x int, y int, a area) (int, bool) {
	currX, currY := 0, 0
	maxHeight := 0
	dx, dy := x, y
	for currX <= a[1] && currY >= a[2] {
		if a[0] <= currX && currX <= a[1] && a[2] <= currY && currY <= a[3] {
			return maxHeight, true
		}
		currX += dx
		currY += dy
		if currY > maxHeight {
			maxHeight = currY
		}

		if dx > 0 {
			dx -= 1
		} else if dx < 0 {
			dx += 1
		}
		dy -= 1
	}
	return -1, false
}

func findMaxHeight(a area) int {
	maxHeight := 0
	for i := 0; i < a[1]/2; i++ {
		for j := 0; j <= -a[2]; j++ {
			height, ok := fallsIn(i, j, a)
			if ok && height > maxHeight {
				maxHeight = height
			}
		}
	}
	return maxHeight
}

func findCorrectSolutions(a area) int {
	sols := 0
	for i := 0; i <= a[1]; i++ {
		for j := a[2]; j <= -a[2]; j++ {
			_, ok := fallsIn(i, j, a)
			if ok {
				sols += 1
			}
		}
	}
	return sols
}

func day17() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 17)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	a := parseLines(rawLines)

	// Part 1
	maxHeight := findMaxHeight(a)
	fmt.Printf("The maximum height achieved is %d\n", maxHeight)

	// Part 2
	sols := findCorrectSolutions(a)
	fmt.Printf("The total number of possible ways is %d\n", sols)

}

func main() {
	adventUtils.Benchmark(day17)
}
