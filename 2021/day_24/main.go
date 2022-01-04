package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
	"strconv"
	"strings"
)

type instruction struct {
	command, v1, v2 string
}

type block struct {
	i, div, var6, var16 int
}

type combination struct {
	i1, i2 block
}

type memory struct {
	w, x, y, z int
	inputs     []int
}

func parseLines(l []string) []instruction {
	res := []instruction{}
	for _, line := range l {
		command := strings.Split(line, " ")
		if len(command) == 2 {
			res = append(res, instruction{command[0], command[1], ""})
		} else if len(command) == 3 {
			res = append(res, instruction{command[0], command[1], command[2]})
		} else {
			panic(fmt.Sprintf("Could not parse %s", line))
		}
	}
	return res
}

func getValue(m memory, l string) int {
	if l == "w" {
		return m.w
	} else if l == "x" {
		return m.x
	} else if l == "y" {
		return m.y
	} else if l == "z" {
		return m.z
	} else {
		panic(fmt.Sprintf("Could not find %s", l))
	}
}

func parseOrGet(m memory, l string) int {
	v, err := strconv.Atoi(l)
	if err != nil {
		return getValue(m, l)
	}
	return v
}

func storeValue(m memory, l string, v int) memory {
	if l == "w" {
		m.w = v
	} else if l == "x" {
		m.x = v
	} else if l == "y" {
		m.y = v
	} else if l == "z" {
		m.z = v
	} else {
		panic(fmt.Sprintf("Could not store to %s", l))
	}
	return m
}

func executeInp(i instruction) func(memory) memory {
	return func(m memory) memory {
		v := m.inputs[0]
		m.inputs = m.inputs[1:]
		m = storeValue(m, i.v1, v)
		return m
	}
}

func executeAdd(i instruction) func(memory) memory {
	loc := i.v1

	return func(m memory) memory {
		v1 := getValue(m, loc)
		v2 := parseOrGet(m, i.v2)
		return storeValue(m, loc, v1+v2)
	}
}

func executeMul(i instruction) func(memory) memory {
	loc := i.v1

	return func(m memory) memory {
		v1 := getValue(m, loc)
		v2 := parseOrGet(m, i.v2)
		return storeValue(m, loc, v1*v2)
	}
}

func executeDiv(i instruction) func(memory) memory {
	loc := i.v1

	return func(m memory) memory {
		v1 := getValue(m, loc)
		v2 := parseOrGet(m, i.v2)
		return storeValue(m, loc, v1/v2)
	}
}

func executeMod(i instruction) func(memory) memory {
	loc := i.v1
	return func(m memory) memory {
		v1 := getValue(m, loc)
		v2 := parseOrGet(m, i.v2)
		return storeValue(m, loc, v1%v2)
	}
}

func executeEql(i instruction) func(memory) memory {
	loc := i.v1

	return func(m memory) memory {
		v1 := getValue(m, loc)
		v2 := parseOrGet(m, i.v2)
		var v int
		if v1 == v2 {
			v = 1
		} else {
			v = 0
		}
		return storeValue(m, loc, v)
	}
}

func generateInput(n int64, it int) []int {
	i := []int{}
	for k := 0; k < it; k++ {
		i = append(i, int(n%9)+1)
		n = n / 9
	}
	// Reverse
	res := []int{}
	for j := len(i) - 1; j >= 0; j-- {
		res = append(res, i[j])
	}
	return res
}

func parseInstructions(i []instruction) []func(memory) memory {
	res := [](func(memory) memory){}
	for _, ins := range i {
		switch ins.command {
		case "inp":
			res = append(res, executeInp(ins))
		case "add":
			res = append(res, executeAdd(ins))
		case "mul":
			res = append(res, executeMul(ins))
		case "div":
			res = append(res, executeDiv(ins))
		case "mod":
			res = append(res, executeMod(ins))
		case "eql":
			res = append(res, executeEql(ins))
		default:
			panic(fmt.Sprintf("Could not parse %s", i))
		}
	}
	return res
}

func bruteForce(ins []instruction) int64 {
	parsed := parseInstructions(ins)
	for i := int64(math.Pow(9, 14)) - 1; i >= 0; i-- {
		input := generateInput(i, 14)
		m := memory{inputs: input}
		if m.inputs[13] == 1 && m.inputs[12] == 1 && m.inputs[11] == 1 && m.inputs[10] == 1 && m.inputs[9] == 1 && m.inputs[8] == 1 {
			fmt.Printf("We are now at %+v \n", m.inputs)
		}
		for _, f := range parsed {
			m = f(m)
		}
		if m.z == 0 {
			res := int64(0)
			for _, v := range input {
				res *= 10
				res += int64(v)
			}
			return res

		}
	}
	panic("Could not find the right monad number")
}

func generateStaticInstructions(ins []instruction) []block {
	res := []block{}
	for i := 0; i < len(ins); i = i + 18 {
		div := parseOrGet(memory{}, ins[i+4].v2)
		var6 := parseOrGet(memory{}, ins[i+5].v2)
		var16 := parseOrGet(memory{}, ins[i+15].v2)
		res = append(res, block{int(i / 18), div, var6, var16})
	}
	return res
}

var staticInstruction [][3]int = [][3]int{
	{1, 14, 7},   //i00: p0 => i0 + 7         ----------|
	{1, 12, 4},   //i01: p1 => i1 + 4         --------| |
	{1, 11, 8},   //i02: p2 => i2 + 8         --|     | |
	{26, -4, 1},  //i03: p2 => i3 - 4         --|     | |
	{1, 10, 5},   //i04: p3 => i4 + 5         ------| | |
	{1, 10, 14},  //i05: p4 => i5 + 14        ----| | | |
	{1, 15, 12},  //i06: p5 => i6 + 12        --| | | | |
	{26, -9, 10}, //i07: p5 => i7 - 9         --| | | | |
	{26, -9, 5},  //i08: p4 => i8 - 9         ----| | | |
	{1, 12, 7},   //i09: p6 => i9 + 7    	  --|   | | |
	{26, -15, 6}, //i10: p6 => i10 - 15       --|   | | |
	{26, -7, 8},  //i11: p3 => i11 - 7        ------| | |
	{26, -10, 4}, //i12: p1 => i12 - 10       --------| |
	{26, 0, 6},   //i13: p0 => i13 - 0        ----------|

	// p0 ==> i13 = i0 + 7  - 0  ==> i0 = i13 - 7
	// p1 ==> i12 = i1 + 4  - 10 ==> i1 = i12 + 6
	// p2 ==> i3  = i2 + 8  - 4  ==> i2 = i3  + 4
	// p3 ==> i11 = i4 + 5  - 7  ==> i4 = i11 + 2
	// p4 ==> i8  = i5 + 14 - 9  ==> i5 = i8  - 5
	// p5 ==> i7  = i6 + 12 - 9  ==> i6 = i7  - 3
	// p6 ==> i10 = i9 + 7  - 15 ==> i9 = i10 + 8

	// Largest
	//		i0 = 2 => i13 = 9
	// 		i1 = 9 => i12 = 3
	// 		i2 = 9 => i3  = 5
	//		i4 = 9 => i11 = 7
	//		i5 = 4 => i8  = 9
	// 		i6 = 6 => i7  = 9
	//		i9 = 9 => i10 = 1
	// 29959469991739

	//		i0 = 9 => i13 = 2
	// 		i1 = 3 => i12 = 9
	// 		i2 = 5 => i3  = 9
	//		i4 = 7 => i11 = 9
	//		i5 = 9 => i8  = 4
	// 		i6 = 9 => i7  = 6
	//		i9 = 6 => i10 = 9
	// 9,3,5,9,7,9,9,6,4,6,9,9,9,2

	// Smallest
	//		i0 = 1 => i13 = 8
	// 		i1 = 7 => i12 = 1
	// 		i2 = 5 => i3  = 1
	//		i4 = 3 => i11 = 1
	//		i5 = 1 => i8  = 6
	// 		i6 = 1 => i7  = 4
	//		i9 = 9 => i10 = 1
	// 29959469991739
}

func checkSolution(i [][3]int, input []int) int64 {
	z := 0
	for j, block := range i {
		div := block[0]
		var6 := block[1]
		var16 := block[2]
		inp := input[j]
		if (z%26 + var6) != inp {
			z = z / div
			z = z*26 + (inp + var16)
		} else {
			z = z / div
		}
	}
	if z == 0 {
		res := int64(0)
		for _, v := range input {
			res *= 10
			res += int64(v)
		}
		return res
	}
	return -1

}

func findLargestOne(ins []instruction, c chan int64) {
	// Every 18 lines, there is the same instruction
	static := staticInstruction

	for i := 2*9*9*int64(math.Pow(9, 11)) - 1; i >= 0; i-- {
		input := generateInput(i, 14)
		if input[13] == 1 && input[12] == 1 && input[11] == 1 && input[10] == 1 && input[9] == 1 && input[8] == 1 {
			fmt.Printf("We are now at %+v \n", input)
		}
		z := checkSolution(static, input)
		if z != -1 {
			c <- z
			return
		}

	}
	panic("Could not find solution")
}

func findSmallestOne(ins []instruction, c chan int64) {
	// Every 18 lines, there is the same instruction
	static := staticInstruction

	for i := int64(0); i < int64(2*9*9*math.Pow(9, 11)); i++ {
		input := generateInput(i, 14)
		if input[13] == 1 && input[12] == 1 && input[11] == 1 && input[10] == 1 && input[9] == 1 && input[8] == 1 {
			fmt.Printf("We are now at %+v \n", input)
		}
		z := checkSolution(static, input)
		if z != -1 {
			c <- z
			return
		}

	}
	panic("Could not find solution")
}

func parseCombos(bs []block) []combination {
	stack := []block{}
	combos := []combination{}
	for _, b := range bs {
		if b.div == 1 {
			stack = append(stack, b)
		} else {
			block1 := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			combos = append(combos, combination{block1, b})
		}
	}
	return combos
}

func findLargest(ins []instruction) int64 {
	// Taken a lot from https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs
	blocks := generateStaticInstructions(ins)
	combos := parseCombos(blocks)
	res := make([]int, len(blocks))
	for _, c := range combos {
		diff := c.i1.var16 + c.i2.var6
		res[c.i1.i] = adventUtils.MinInt(9-diff, 9)
		res[c.i2.i] = adventUtils.MinInt(9+diff, 9)
	}
	r := int64(0)
	for _, v := range res {
		r *= 10
		r += int64(v)
	}
	return r
}

func findSmallest(ins []instruction) int64 {
	// Taken a lot from https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs
	blocks := generateStaticInstructions(ins)
	combos := parseCombos(blocks)
	res := make([]int, len(blocks))
	for _, c := range combos {
		diff := c.i1.var16 + c.i2.var6
		res[c.i1.i] = adventUtils.MaxInt(1-diff, 1)
		res[c.i2.i] = adventUtils.MaxInt(1+diff, 1)
	}
	r := int64(0)
	for _, v := range res {
		r *= 10
		r += int64(v)
	}
	return r
}

func day24() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 24)
	if err != nil {
		panic(fmt.Errorf("%+v\n", err))
	}
	instructions := parseLines(rawLines)

	// Part 1
	large := findLargest(instructions)
	fmt.Printf("The largest accepted number in MONAD is %d\n", large)

	// Part 2
	small := findSmallest(instructions)
	fmt.Printf("The smallest accepted number in MONAD is %d\n", small)

}

func main() {
	adventUtils.Benchmark(day24)
}
