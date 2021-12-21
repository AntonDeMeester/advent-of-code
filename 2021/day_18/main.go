package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
	"strconv"
)

type snailfish struct {
	value      int
	leftSnail  *snailfish
	rightSnail *snailfish
	parent     *snailfish
	isLeft     bool
	isValue    bool
}

func (s snailfish) toString() string {
	var left string
	var right string
	if !s.isValue {
		left = s.leftSnail.toString()
		right = s.rightSnail.toString()
		return fmt.Sprintf("[%s,%s]", left, right)
	}
	return strconv.Itoa(s.value)
}

func (s *snailfish) getLeftNeighbour() *snailfish {
	// Find the first left parent of which we can take a left value
	curr := s
	for curr.parent != nil && curr.isLeft {
		curr = curr.parent
	}
	if curr.parent == nil {
		return nil
	}
	neighbour := curr.parent.leftSnail

	for {
		if neighbour == nil {
			return nil
		}
		if neighbour.isValue {
			return neighbour
		}
		neighbour = neighbour.rightSnail
	}
}

func (s *snailfish) getRightNeighbour() *snailfish {
	curr := s
	for curr.parent != nil && !curr.isLeft {
		curr = curr.parent
	}
	if curr.parent == nil {
		return nil
	}
	neighbour := curr.parent.rightSnail

	for {
		if neighbour == nil {
			return nil
		}
		if neighbour.isValue {
			return neighbour
		}
		neighbour = neighbour.leftSnail
	}
}

func (s snailfish) getMagnitude() int {
	if s.isValue {
		return s.value
	}
	return s.leftSnail.getMagnitude()*3 + s.rightSnail.getMagnitude()*2
}

func pop(sls []*snailfish) ([]*snailfish, *snailfish) {
	return sls[:len(sls)-1], sls[len(sls)-1]
}

func parseLines(lines []string) []*snailfish {
	res := []*snailfish{}
	for _, l := range lines {
		stack := []*snailfish{}
		stack = append(stack, &snailfish{})
		isLeft := true
		for _, c := range []rune(l) {
			var lastFish *snailfish
			stack, lastFish = pop(stack)
			switch c {
			case '[':
				newFish := &snailfish{parent: lastFish, isLeft: isLeft, isValue: false}
				if isLeft {
					lastFish.leftSnail = newFish
				} else {
					lastFish.rightSnail = newFish
				}
				stack = append(stack, lastFish, newFish)
				isLeft = true
			case ']':
			case ',':
				isLeft = false
				stack = append(stack, lastFish)
			default:
				valueFish := &snailfish{value: int(c - '0'), isValue: true, parent: lastFish, isLeft: isLeft}
				if isLeft {
					lastFish.leftSnail = valueFish
				} else {
					lastFish.rightSnail = valueFish
				}
				stack = append(stack, lastFish)
			}
		}
		toAppend := (*stack[0]).leftSnail
		toAppend.parent = nil
		toAppend.isLeft = false
		toAppend.isValue = false
		res = append(res, toAppend)
	}
	return res
}

func addSnails(left, right *snailfish) *snailfish {
	newSnail := &snailfish{leftSnail: left, rightSnail: right}
	left.parent = newSnail
	left.isLeft = true
	right.parent = newSnail
	right.isLeft = false
	return newSnail
}

func explode(snail *snailfish) {
	if left := snail.getLeftNeighbour(); left != nil {
		left.value += snail.leftSnail.value
	}
	if right := snail.getRightNeighbour(); right != nil {
		right.value += snail.rightSnail.value
	}
	if snail.isLeft {
		snail.parent.leftSnail = &snailfish{value: 0, isValue: true, parent: snail.parent, isLeft: true}
	} else {
		snail.parent.rightSnail = &snailfish{value: 0, isValue: true, parent: snail.parent, isLeft: false}
	}
}

func split(snail *snailfish) {
	leftValue := int(math.Floor(float64(snail.value) / 2))
	rightValue := snail.value - leftValue
	newLeftValue := &snailfish{isValue: true, value: leftValue, parent: snail, isLeft: true}
	newRightValue := &snailfish{isValue: true, value: rightValue, parent: snail, isLeft: false}
	snail.value = 0
	snail.isValue = false

	snail.leftSnail = newLeftValue
	snail.rightSnail = newRightValue
}

func explodeSnakeRecursive(snail *snailfish, depth int) bool {
	if snail == nil {
		return false
	}
	if depth >= 4 && !snail.isValue {
		explode(snail)
		return true
	}
	if explodeSnakeRecursive(snail.leftSnail, depth+1) {
		return true
	}
	return explodeSnakeRecursive(snail.rightSnail, depth+1)
}

func splitSnakeRecursive(snail *snailfish) bool {
	if snail == nil {
		return false
	}
	if snail.isValue && snail.value >= 10 {
		split(snail)
		return true
	}
	if splitSnakeRecursive(snail.leftSnail) {
		return true
	}
	return splitSnakeRecursive(snail.rightSnail)
}

func reduceSnail(snail *snailfish) *snailfish {
	for {
		exploded := explodeSnakeRecursive(snail, 0)
		if !exploded {
			if !splitSnakeRecursive(snail) {
				return snail
			}
		}
		// fmt.Printf("%+v\n", snail.toString())
	}
}

func partOne(snails []*snailfish) int {
	res := snails[0]
	for i := 1; i < len(snails); i++ {
		res = addSnails(res, snails[i])
		res = reduceSnail(res)
		// fmt.Printf("%+v\n", res.toString())
	}
	return res.getMagnitude()
}

func findGreatest(l []string) int {
	res := 0
	snails := parseLines(l)
	for i := 0; i < len(snails); i++ {
		for j := i; j < len(snails); j++ {
			snails = parseLines(l)
			add := addSnails(snails[i], snails[j])
			add = reduceSnail(add)
			if s := add.getMagnitude(); s > res {
				res = s
			}

			snails = parseLines(l)
			add = addSnails(snails[j], snails[i])
			add = reduceSnail(add)
			if s := add.getMagnitude(); s > res {
				res = s
			}
		}
	}
	return res
}

func day18() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 18)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	snails := parseLines(rawLines)

	// Part 1
	snailMagnitude := partOne(snails)
	fmt.Printf("The snail magnitude is %d\n", snailMagnitude)

	// Part 2
	sols := findGreatest(rawLines)
	fmt.Printf("The largest sum of two snails is %d\n", sols)

}

func main() {
	adventUtils.Benchmark(day18)
}
