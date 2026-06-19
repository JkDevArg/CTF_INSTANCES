.PHONY: gen build test dist-player safety clean

# Regenerate generated sources from the constraint model + ISA.
gen:
	python3 tools/gen_challenge.py

# Release build (consumes the generated sources).
build: gen
	cargo build --release

# Cargo tests in release profile (matches the player's binary semantics).
test: gen
	cargo test --release

# Pre-distribution safety check: scans the binary for any leak.
safety: build
	python3 tools/safety_check.py \
		--binary target/release/matevm2 \
		--challenge challenge.json

# Build the player-facing distribution.
# Includes ONLY the stripped binary and a minimal README.
# Runs the safety check before publishing the directory.
dist-player: build safety
	rm -rf dist-player
	mkdir -p dist-player
	cp target/release/matevm2 dist-player/matevm2
	strip dist-player/matevm2
	cp player/README.md dist-player/README.md
	@echo "---"
	@echo "dist-player/ ready:"
	@ls -la dist-player/
	@echo "---"
	@echo "DO NOT ship: src/, tools/, author/, docs/, challenge.json,"
	@echo "constraints.json, Cargo.toml, Cargo.lock, target/"

clean:
	cargo clean
	rm -rf dist-player challenge.json src/generated.rs src/msg.rs
