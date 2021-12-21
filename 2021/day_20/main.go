package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
)

type coord struct {
	x, y int
}

func parseLines(l []string) ([]bool, map[coord]bool) {
	enhance := []bool{}
	for _, c := range []rune(l[0]) {
		if c == '#' {
			enhance = append(enhance, true)
		} else {
			enhance = append(enhance, false)
		}
	}

	image := map[coord]bool{}
	for x, row := range l[2:] {
		for y, c := range []rune(row) {
			if c == '#' {
				image[coord{x, y}] = true
			} else {
				image[coord{x, y}] = false
			}

		}
	}
	return enhance, image
}

func countLitAfterTwice(p []bool, img map[coord]bool) int {
	for i := 0; i < 2; i++ {
		countTrue(img)
		img = enchanceStep(p, img, i)
	}
	return countTrue(img)
}

func countLitAfterFifty(p []bool, img map[coord]bool) int {
	for i := 0; i < 50; i++ {
		countTrue(img)
		img = enchanceStep(p, img, i)
	}
	return countTrue(img)
}

func enchanceStep(p []bool, img map[coord]bool, step int) map[coord]bool {
	minX, maxX, minY, maxY := math.MaxInt, math.MinInt, math.MaxInt, math.MinInt
	for key := range img {
		if key.x > maxX {
			maxX = key.x
		}
		if key.x < minX {
			minX = key.x
		}
		if key.y > maxY {
			maxY = key.y
		}
		if key.y < minY {
			minY = key.y
		}
	}
	res := map[coord]bool{}
	for i := minX - 1; i <= maxX+1; i++ {
		for j := minY - 1; j <= maxY+1; j++ {
			empty := false
			if p[0] && step%2 == 1 {
				empty = true
			}
			surr := getSurrounding(i, j, empty, img)
			converted := convert(surr)
			res[coord{i, j}] = p[converted]
		}
	}
	// fmt.Printf("%v+\n", res)
	return res
}

func getSurrounding(x int, y int, empty bool, img map[coord]bool) []bool {
	res := []bool{}
	for i := -1; i <= 1; i++ {
		for j := -1; j <= 1; j++ {
			v, ok := img[coord{x + i, y + j}]
			if ok {
				res = append(res, v)
			} else {
				res = append(res, empty)
			}
		}
	}
	return res
}

func convert(i []bool) int {
	res := 0
	for _, v := range i {
		res *= 2
		if v {
			res += 1
		}
	}
	return res
}

func countTrue(img map[coord]bool) int {
	res := 0
	for _, v := range img {
		if v {
			res += 1
		}
	}
	return res
}

func day20() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 20)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	pattern, image := parseLines(rawLines)
	// fmt.Printf("The pattern is %+v, the image is %+v\n", pattern, image)

	// Part 1
	countTwo := countLitAfterTwice(pattern, image)
	fmt.Printf("The number of lit fields after two steps is %d\n", countTwo)

	// Part 2
	countFifty := countLitAfterFifty(pattern, image)
	fmt.Printf("The number of lit fields after 50 steps is %d\n", countFifty)

}

func main() {
	adventUtils.Benchmark(day20)
}
