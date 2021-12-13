package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strconv"
	"strings"
)

type fold struct {
	direction string
	value     int
}

func parseLines(l []string) ([][]bool, []fold) {
	temp := [][2]int{}
	folds := []fold{}
	maxX, maxY := 0, 0
	for _, line := range l {
		split := strings.Split(line, ",")
		if len(split) == 2 {
			x, errX := strconv.Atoi(split[0])
			y, errY := strconv.Atoi(split[1])
			if errX != nil || errY != nil {
				panic(fmt.Sprintf("Could not parse %s", line))
			}
			if x+1 > maxX {
				maxX = x + 1
			}
			if y+1 > maxY {
				maxY = y + 1
			}
			temp = append(temp, [2]int{x, y})
		}
		if line == "" {
			continue
		}
		splitSpace := strings.Split(line, " ")
		if len(splitSpace) == 3 {
			splitEqual := strings.Split(splitSpace[2], "=")
			v, err := strconv.Atoi(splitEqual[1])
			if err != nil {
				panic(fmt.Sprintf("Could not parse %s", line))
			}
			folds = append(folds, fold{direction: splitEqual[0], value: v})
		}
	}
	paper := [][]bool{}
	for i := 0; i < maxX; i++ {
		paper = append(paper, make([]bool, maxY))
	}
	for _, t := range temp {
		paper[t[0]][t[1]] = true
	}
	return paper, folds
}

func foldPaper(paper [][]bool, fold fold) [][]bool {
	maxX, maxY := len(paper), len(paper[0])
	xSize, ySize := maxX, maxY
	if fold.direction == "y" {
		ySize = adventUtils.MaxInt(maxY-fold.value-1, fold.value-1)
	} else {
		xSize = adventUtils.MaxInt(maxX-fold.value-1, fold.value-1)
	}

	res := [][]bool{}
	for i := 0; i < xSize; i++ {
		res = append(res, make([]bool, ySize))
	}
	for i := 0; i < xSize; i++ {
		for j := 0; j < ySize; j++ {
			var originX, originY, mirrorX, mirrorY int
			if fold.direction == "y" {
				originX, mirrorX = i, i
				originY, mirrorY = j, maxY-j-1
			} else {
				originX, mirrorX = i, maxX-i-1
				originY, mirrorY = j, j
			}
			res[i][j] = paper[originX][originY] || paper[mirrorX][mirrorY]
		}

	}
	return res
}

func countMarks(paper [][]bool) int {
	res := 0
	for _, row := range paper {
		for _, elem := range row {
			if elem {
				res += 1
			}
		}
	}
	return res
}

func doOneFold(paper [][]bool, folds []fold) int {
	return countMarks(foldPaper(paper, folds[0]))
}

func printInstructions(paper [][]bool, folds []fold) {
	for _, f := range folds {
		paper = foldPaper(paper, f)
	}
	output := make([]string, len(paper))
	for _, row := range paper {
		for i, e := range row {
			if e {
				output[i] += "X"
			} else {
				output[i] += " "
			}
		}
	}
	for _, l := range output {
		fmt.Println(l)
	}
}

func day13() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 13)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	paper, folds := parseLines(rawLines)

	// Part 1
	foldMarks := doOneFold(paper, folds)
	fmt.Printf("The total number of crosses after the folds is %d\n", foldMarks)

	// Part 2
	printInstructions(paper, folds)
	// fmt.Printf("The total number of paths with one repeat is %d\n", pathsRepeat)

}

func main() {
	adventUtils.Benchmark(day13)
}
