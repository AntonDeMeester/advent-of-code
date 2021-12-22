package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strconv"
	"strings"
)

type coord struct {
	x, y, z int
}
type rebootStep struct {
	from   coord
	to     coord
	action bool
}
type area struct {
	from coord
	to   coord
}
type box struct {
	from     coord
	to       coord
	subboxes []*box
}

func parseLines(l []string) []rebootStep {
	res := []rebootStep{}
	for _, line := range l {
		step := rebootStep{}
		actionSplit := strings.Split(line, " ")
		if actionSplit[0] == "off" {
			step.action = false
		} else if actionSplit[0] == "on" {
			step.action = true
		} else {
			panic(fmt.Sprintf("Could not parse %s", line))
		}

		commaSplit := strings.Split(actionSplit[1], ",")
		xSplit := strings.Split(commaSplit[0][2:], "..")
		ySplit := strings.Split(commaSplit[1][2:], "..")
		zSplit := strings.Split(commaSplit[2][2:], "..")
		x1, _ := strconv.Atoi(xSplit[0])
		x2, _ := strconv.Atoi(xSplit[1])
		y1, _ := strconv.Atoi(ySplit[0])
		y2, _ := strconv.Atoi(ySplit[1])
		z1, _ := strconv.Atoi(zSplit[0])
		z2, _ := strconv.Atoi(zSplit[1])

		step.from = coord{x1, y1, z1}
		step.to = coord{x2, y2, z2}
		res = append(res, step)
	}
	return res
}

func getState(c coord, m map[coord]bool) bool {
	v, ok := m[c]
	return ok && v
}

func countInit(steps []rebootStep) int {
	m := map[coord]bool{}
	for _, s := range steps {
		for i := adventUtils.MaxInt(s.from.x, -50); i <= adventUtils.MinInt(s.to.x, 50); i++ {
			for j := adventUtils.MaxInt(s.from.y, -50); j <= adventUtils.MinInt(s.to.y, 50); j++ {
				for k := adventUtils.MaxInt(s.from.z, -50); k <= adventUtils.MinInt(s.to.z, 50); k++ {
					m[coord{i, j, k}] = s.action
				}
			}
		}
	}
	cnt := 0
	for i := -50; i <= 50; i++ {
		for j := -50; j <= 50; j++ {
			for k := -50; k <= 50; k++ {
				if getState(coord{i, j, k}, m) {
					cnt++
				}
			}
		}
	}
	return cnt
}

func countReboot(steps []rebootStep) int {
	// Stolen from https://github.com/p88h/aoc2021/blob/main/other/day22b.py
	// And https://github.com/Fadi88/AoC/blob/master/2021/day22/code.py
	boxes := []*box{}
	for _, s := range steps {
		newBox := box{from: s.from, to: s.to, subboxes: []*box{}}
		for _, b := range boxes {
			b.subtract(newBox)
		}
		if s.action {
			boxes = append(boxes, &newBox)
		}
	}
	cnt := 0
	for _, b := range boxes {
		cnt += b.count()
	}
	return cnt
}

func intersects(one, two box) bool {
	if one.to.x < two.from.x || one.from.x > two.to.x {
		return false
	}
	if one.to.y < two.from.y || one.from.y > two.to.y {
		return false
	}
	if one.to.z < two.from.z || one.from.z > two.to.z {
		return false
	}
	return true
}

func getIntersection(from1, to1, from2, to2 int) (int, int) {
	// Needs to have an intersection
	if from1 <= from2 {
		// from1 from2 ...
		if to1 <= to2 {
			// from1 from2 to1 to2
			return from2, to1
		} else {
			// from1 from2 to2 to1
			return from2, to2
		}
	} else {
		//from2 from1
		if to1 <= to2 {
			// from2 from1 to1 to2
			return from1, to1
		} else {
			// from2 from1 to2 to1
			return from1, to2
		}
	}
}

func getIntersectionBox(one, two box) box {
	fromx, tox := getIntersection(one.from.x, one.to.x, two.from.x, two.to.x)
	fromy, toy := getIntersection(one.from.y, one.to.y, two.from.y, two.to.y)
	fromz, toz := getIntersection(one.from.z, one.to.z, two.from.z, two.to.z)
	return box{from: coord{fromx, fromy, fromz}, to: coord{tox, toy, toz}, subboxes: []*box{}}
}

func (b *box) subtract(other box) {
	if !intersects(*b, other) {
		return
	}
	for _, subb := range b.subboxes {
		subb.subtract(other)
	}
	intersection := getIntersectionBox(*b, other)
	b.subboxes = append(b.subboxes, &intersection)
}

func (b box) count() int {
	count := (b.to.x - b.from.x + 1) * (b.to.y - b.from.y + 1) * (b.to.z - b.from.z + 1)
	for _, sub := range b.subboxes {
		count -= sub.count()
	}
	return count
}

func day22() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 22)
	if err != nil {
		panic(fmt.Errorf("%+v\n", err))
	}
	reboots := parseLines(rawLines)
	// fmt.Printf("The reboot steps are %+v\n", reboots)

	// Part 1
	initCount := countInit(reboots)
	fmt.Printf("The number of cubes for init which are on is %d\n", initCount)

	// Part 2
	totalCount := countReboot(reboots)
	fmt.Printf("The number of cubes which are on is %d\n", totalCount)

}

func main() {
	adventUtils.Benchmark(day22)
}
