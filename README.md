## Microtest

Dead simple async unit test suite for micropython.

Work in progress. Mainly using it on things I'm building for fun and adding to it as needed.

## Usage
Just copy `microtest.py` over to wherever you're using it.

You'll need:
- `micropython` installed where you're running the tests (I'm using a Mac)
- the `uasyncio` package installed

Clone this repo and run `make tests`

You can reference `example.test.py` and the `Makefile` in this repo for tips on
running tests with the `micropython` binary.
