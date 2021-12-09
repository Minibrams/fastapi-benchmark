package main

import (
	"fmt"
	"net/http"
	"strconv"
	"time"
)

func get(response http.ResponseWriter, request *http.Request) {
	query := request.URL.Query()
	waitms, present := query["waitms"]

	if !present || len(waitms) == 0 {
		waitms = [] string { "1000" }
	}

	waitForMs, err := strconv.Atoi(waitms[0])

	if err != nil {
		waitForMs = 1000
	}

	time.Sleep(time.Duration(waitForMs) * time.Millisecond)
	fmt.Fprintf(response, "Waited for " + waitms[0] + " milliseconds")
}

func main() {
	http.HandleFunc("/", get)
	http.ListenAndServe(":8090", nil)
}
