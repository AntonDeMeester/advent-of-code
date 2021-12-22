package adventUtils

import "math"

func Sum(n []int) int {
	r := 0
	for _, c := range n {
		r += c
	}
	return r
}

func IsIn(i int, l []int) bool {
	for _, j := range l {
		if i == j {
			return true
		}
	}
	return false
}

func MaxInt(n ...int) int {
	res := math.MinInt
	for _, i := range n {
		if res < i {
			res = i
		}
	}
	return res
}

func MinInt(n ...int) int {
	res := math.MaxInt
	for _, i := range n {
		if res > i {
			res = i
		}
	}
	return res
}
