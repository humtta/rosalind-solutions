package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(s string) string {
	return s
}

func main() {
	s := bufio.NewScanner(os.Stdin)
	if !s.Scan() {
		fmt.Fprintln(os.Stderr, "Error reading input:", s.Err())
		os.Exit(1)
	}

	fmt.Println(solve(s.Text()))
}
