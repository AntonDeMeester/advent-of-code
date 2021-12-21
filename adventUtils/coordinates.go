package adventUtils

import (
	"fmt"
	"strconv"
	"strings"
)

func ParseCoordinates(l string) []int {
	s := strings.Split(l, ",")
	res := []int{}
	for _, c := range s {
		x, err := strconv.Atoi(c)
		if err != nil {
			panic(fmt.Sprintf("Could not parse coordinates from %s", l))
		}
		res = append(res, x)
	}
	return res
}
