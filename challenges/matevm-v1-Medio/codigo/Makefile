build:
	cargo build --release

dist: build
	mkdir -p dist
	cp target/release/matevm dist/matevm
	strip dist/matevm

run:
	cargo run

test:
	cargo test

solve:
	python3 solution/solve.py

clean:
	cargo clean
	rm -rf dist
