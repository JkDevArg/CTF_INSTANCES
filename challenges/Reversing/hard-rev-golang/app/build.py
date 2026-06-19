import os
import subprocess

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

go_src = f'''package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// deobfuscate XOR-decodes a byte slice with key 0x42
func deobfuscate(s []byte) string {{
	result := make([]byte, len(s))
	for i, b := range s {{
		result[i] = b ^ 0x42
	}}
	return string(result)
}}

func main() {{
	// Target string XOR-encoded with 0x42 at build time
	encoded := []byte{{{', '.join(str(ord(c) ^ 0x42) for c in FLAG)}}}
	target := deobfuscate(encoded)

	fmt.Print("GoCrackMe v1.0 -- Enter the secret: ")
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\\n')
	input = strings.TrimSpace(input)

	if input == target {{
		fmt.Println("[+] CORRECT! Access granted.")
	}} else {{
		fmt.Println("[-] Wrong. Try again.")
	}}
}}
'''

os.makedirs('/tmp/gobuild', exist_ok=True)
with open('/tmp/gobuild/main.go', 'w') as f:
    f.write(go_src)

os.makedirs('/app/dist', exist_ok=True)

result = subprocess.run(
    ['go', 'build', '-ldflags=-s -w', '-o', '/app/dist/gocrackme', '/tmp/gobuild/main.go'],
    capture_output=True
)
if result.returncode != 0:
    print("[!] Go build failed:")
    print(result.stderr.decode())
    raise SystemExit(1)
else:
    os.chmod('/app/dist/gocrackme', 0o555)
    print("[+] Binary built: /app/dist/gocrackme")
