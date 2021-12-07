package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
	"strconv"
	"strings"
)

func parseLine(l []string) []int {
	rawNumbers := strings.Split(l[0], ",")
	res := []int{}
	for _, s := range rawNumbers {
		n, err := strconv.Atoi(s)
		if err != nil {
			panic(err)
		}
		res = append(res, n)
	}
	return res
}

func findMinFuel(d []int) int {
	max := adventUtils.MaxInt(d...)
	min := adventUtils.MinInt(d...)

	minFuel := int(1e10)

	for i := min; i <= max; i++ {
		fuel := 0
		for _, v := range d {
			fuel += int(math.Abs(float64(i - v)))
		}
		if fuel < minFuel {
			minFuel = fuel
		}
	}
	return minFuel
}

func findMinFuelComplex(d []int) int {
	max := adventUtils.MaxInt(d...)
	min := adventUtils.MinInt(d...)

	minFuel := int(1e10)

	for i := min; i <= max; i++ {
		fuel := 0
		for _, v := range d {
			distance := math.Abs(float64(i - v))
			fuel += int((distance + 1) * distance / 2)
		}
		if fuel < minFuel {
			minFuel = fuel
		}
	}
	return minFuel
}

func day_6() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 7)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	crabs := parseLine(rawLines)

	// Part 1
	minFuel := findMinFuel(crabs)
	fmt.Printf("The minimum simple fuel is %d\n", minFuel)

	// // Part 2
	minFuelComplex := findMinFuelComplex(crabs)
	fmt.Printf("The minimum complex fuel is %d\n", minFuelComplex)

}

func main() {
	adventUtils.Benchmark(day_6)
}
