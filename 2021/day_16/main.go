package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"math"
	"strconv"
)

type packet struct {
	version    uint
	packetType uint
	value      uint
	subpackets []packet
}

func parseLines(l []string) [][]uint {
	res := [][]uint{}
	for _, row := range l {
		parsed := []uint{}
		for _, c := range []rune(row) {
			v, err := strconv.ParseUint(string(c), 16, 8)
			if err != nil {
				panic("Cannot parse value to hex")
			}
			for j := 0; j < 4; j++ {
				parsed = append(parsed, uint(v>>uint(3-j)&0x01))
			}
		}
		res = append(res, parsed)
	}
	return res
}

func bitsToNumber(in []uint) uint {
	var res uint
	for _, v := range in {
		res *= 2
		res += v
	}
	return res
}

func extend(l []uint, other []uint) []uint {
	for _, v := range other {
		l = append(l, v)
	}
	return l
}

func extractValue(in []uint) (uint, []uint) {
	i := 0
	bitNumber := []uint{}
	for {
		next := in[i*5 : 5+i*5]
		bitNumber = extend(bitNumber, next[1:])
		if next[0] == 0 {
			break
		}
		i += 1
	}
	return bitsToNumber(bitNumber), in[5+i*5:]
}

func convertLine(in []uint) (res packet, rest []uint) {
	res.version = bitsToNumber(in[:3])
	res.packetType = bitsToNumber(in[3:6])
	if res.packetType == 4 {
		val, other := extractValue(in[6:])
		res.value = val
		rest = other
	} else {
		subpackets := []packet{}
		if in[6] == 0 {
			length := bitsToNumber(in[7:22])
			otherBits := in[22 : 22+length]
			for len(otherBits) > 0 {
				p, other := convertLine(otherBits)
				otherBits = other
				subpackets = append(subpackets, p)
			}
			rest = in[22+length:]
		} else {
			numberPackets := bitsToNumber(in[7:18])
			otherBits := in[18:]
			for i := 0; i < int(numberPackets); i++ {
				p, other := convertLine(otherBits)
				otherBits = other
				subpackets = append(subpackets, p)
			}
			rest = otherBits
		}
		res.subpackets = subpackets
	}
	return res, rest
}

func countPacketVersion(p packet) (res uint) {
	res += p.version
	if p.subpackets != nil {
		for _, sp := range p.subpackets {
			res += countPacketVersion(sp)
		}
	}
	return res
}

func countVersions(in [][]uint) (res uint) {
	for _, l := range in {
		sol, _ := convertLine(l)
		res += countPacketVersion(sol)
	}
	return res
}

func executeOperation(p packet) uint {
	var res uint = 0
	switch p.packetType {
	case 0:
		for _, p := range p.subpackets {
			res += executeOperation(p)
		}
	case 1:
		res = 1
		for _, p := range p.subpackets {
			res *= executeOperation(p)
		}
	case 2:
		res = math.MaxUint
		for _, p := range p.subpackets {
			val := executeOperation(p)
			if val < res {
				res = val
			}
		}
	case 3:
		for _, p := range p.subpackets {
			val := executeOperation(p)
			if val > res {
				res = val
			}
		}
	case 4:
		res = p.value
	case 5:
		if executeOperation(p.subpackets[0]) > executeOperation(p.subpackets[1]) {
			res = 1
		} else {
			res = 0
		}
	case 6:
		if executeOperation(p.subpackets[0]) < executeOperation(p.subpackets[1]) {
			res = 1
		} else {
			res = 0
		}
	case 7:
		if executeOperation(p.subpackets[0]) == executeOperation(p.subpackets[1]) {
			res = 1
		} else {
			res = 0
		}
	}
	return res
}

func executeAllOperations(in [][]uint) (res uint) {
	for _, l := range in {
		sol, _ := convertLine(l)
		res += executeOperation(sol)
	}
	return res
}

func day16() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 16)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	c := parseLines(rawLines)

	// Part 1
	versions := countVersions(c)
	fmt.Printf("The total version amount is %d\n", versions)

	// Part 2
	opSol := executeAllOperations(c)
	fmt.Printf("The total solution of the packets is %d\n", opSol)

}

func main() {
	adventUtils.Benchmark(day16)
}
