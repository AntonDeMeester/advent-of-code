package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strconv"
	"strings"
)

type point struct {
	x int
	y int
}

type line struct {
	start point
	end   point
}

func getDimDirection(start int, end int) int {
	if end > start {
		return 1
	}
	if end < start {
		return -1
	}
	return 0

}

func (l line) getDirection() (int, int) {
	return getDimDirection(l.start.x, l.end.x), getDimDirection(l.start.y, l.end.y)
}

func (l line) contains(x int, y int) bool {
	checkX, checkY := l.start.x, l.start.y
	lx, ly := l.getDirection()
	for a := 0; a < 10e5; a++ {
		if checkX == x && checkY == y {
			return true
		}
		if checkX == l.end.x && checkY == l.end.y {
			return false
		}
		checkX += lx
		checkY += ly
	}
	fmt.Printf("Infinite loop for %+v and %d, %d direction\n", l, lx, ly)
	panic("Infinite loop")
}

func parseCoordinates(lines []string) []line {
	res := []line{}
	for _, row := range lines {
		splitCoord := strings.Split(row, " -> ")
		start := parsePoint(splitCoord[0])
		end := parsePoint(splitCoord[1])
		res = append(res, line{start, end})
	}
	return res
}

func parsePoint(c string) point {
	splitPoint := strings.Split(c, ",")
	x, err := strconv.Atoi(splitPoint[0])
	if err != nil {
		panic(err)
	}
	y, err := strconv.Atoi(splitPoint[1])
	if err != nil {
		panic(err)
	}
	return point{x, y}
}

func filterNotStraight(inputLines []line) []line {
	res := []line{}
	for _, l := range inputLines {
		if l.start.x == l.end.x || l.start.y == l.end.y {
			res = append(res, l)
		}
	}
	return res
}

func countGeisers(lines []line) [][]int {
	maxX, maxY := 0, 0
	for _, l := range lines {
		maxX = adventUtils.MaxInt(maxX, l.start.x, l.end.x)
		maxY = adventUtils.MaxInt(maxY, l.start.y, l.end.y)
	}

	res := [][]int{}
	for x := 0; x < maxX+1; x++ {
		row := []int{}
		for y := 0; y < maxY+1; y++ {
			geiser := 0
			for _, l := range lines {
				if l.contains(x, y) {
					geiser += 1
				}
			}
			row = append(row, geiser)
		}
		res = append(res, row)
	}

	return res
}

func countDangerous(grid [][]int) int {
	res := 0
	for _, row := range grid {
		for _, ele := range row {
			if ele > 1 {
				res += 1
			}
		}
	}
	return res
}

func day_5() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 5)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	lines := parseCoordinates(rawLines)

	filtered := filterNotStraight(lines)
	geiserGrid := countGeisers(filtered)
	dangeriousCount := countDangerous(geiserGrid)
	fmt.Printf("There are %d dangerious places for the geiser considering only hor and vert \n", dangeriousCount)

	geiserGridTwo := countGeisers(lines)
	dangeriousCountTwo := countDangerous(geiserGridTwo)
	fmt.Printf("There are %d dangerious places for the geiser \n", dangeriousCountTwo)
}

func main() {
	adventUtils.Benchmark(day_5)
}
