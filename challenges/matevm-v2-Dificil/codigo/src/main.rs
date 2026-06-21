use std::io::{self, Write};

mod generated;
mod msg;
mod runner;

fn check(license: &str) -> bool {
    let trimmed = license.trim_end_matches(['\r', '\n']);
    if trimmed.len() > 80 {
        return false;
    }
    // read_volatile is treated as a side effect by LLVM and cannot be elided.
    // black_box is only a hint and gets const-folded across function boundaries
    // under LTO. The combination of read_volatile here and the same trick inside
    // materialize() is what keeps both the cleartext and the encoded buffer
    // out of .rodata.
    static SEED_CELL: u32 = generated::KEYSTREAM_SEED;
    let seed = unsafe { std::ptr::read_volatile(&SEED_CELL) };
    let vm = runner::Vm::new(
        trimmed.as_bytes(),
        generated::CHARSET,
        seed,
        generated::PROGRAM_LEN,
    );
    vm.run(generated::materialize)
}

fn main() {
    println!("{}", msg::banner());
    print!("{}", msg::prompt());
    let _ = io::stdout().flush();

    let mut input = String::new();
    if io::stdin().read_line(&mut input).is_ok() {
        if check(&input) {
            println!("{}", msg::msg_ok());
        } else {
            println!("{}", msg::msg_fail());
        }
    } else {
        println!("{}", msg::msg_fail());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const REAL: &str = "H4L{STATEFUL_VM_BYTECODE_2026}";

    #[test]
    fn real_flag_accepts() {
        assert!(check(REAL));
    }

    #[test]
    fn mutations_reject() {
        let bad = [
            "H4L{STATEFUL_VM_BYTECODE_2027}",
            "H4L{STATEFUL_VM_BYTECODE_2025}",
            "H4L{ATATEFUL_VM_BYTECODE_2026}",
            "H4L{STATEFUL_VM_BYTACODE_2026}",
            "H4L{FAKE_FLAG_DO_NOT_SUBMIT_X}",
        ];
        for b in bad {
            assert!(!check(b), "{b} should not be accepted");
        }
    }

    #[test]
    fn envelope_rejects() {
        assert!(!check("H4X{STATEFUL_VM_BYTECODE_2026}"));
        assert!(!check("H4L{STATEFUL_VM_BYTECODE_2026]"));
        assert!(!check("H4L{STATEFUL_VM_BYTECODE_202}"));
        assert!(!check("H4L{STATEFUL_VM_BYTECODE_20266}"));
        assert!(!check("H4L{STATEFUL VM_BYTECODE_2026}"));
    }

    #[test]
    fn trailing_newline_ok() {
        assert!(check("H4L{STATEFUL_VM_BYTECODE_2026}\n"));
        assert!(check("H4L{STATEFUL_VM_BYTECODE_2026}\r\n"));
    }
}
