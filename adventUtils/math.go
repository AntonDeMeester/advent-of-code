package adventUtils

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
	res := 0
	for _, i := range n {
		if res < i {
			res = i
		}
	}
	return res
}

func MinInt(n ...int) int {
	res := 0
	for _, i := range n {
		if res > i {
			res = i
		}
	}
	return res
}
