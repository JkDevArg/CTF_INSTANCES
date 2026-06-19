use std::io::{self, Write};

mod bytecode;
mod vm;

fn check_license(license: &str) -> bool {
    let license = license.trim();
    if license.len() != 21 {
        return false;
    }
    if !license.starts_with("H4L{") || !license.ends_with('}') {
        return false;
    }

    let program = bytecode::decrypt_program();
    let mut virtual_machine = vm::Vm::new(license.as_bytes());
    virtual_machine.run(&program)
}

fn main() {
    // Decoys strings para despistar
    let _decoys = [
        "H4L{FAKE_FLAG_DO_NOT_SUBMIT}",
        "debug mode disabled",
        "invalid checksum",
        "vm panic",
        "wrong serial",
    ];

    println!("=== MateVM License Checker ===");
    print!("Ingrese licencia: ");
    let _ = io::stdout().flush();

    let mut input = String::new();
    if io::stdin().read_line(&mut input).is_ok() {
        if check_license(&input) {
            println!("Acceso concedido.");
        } else {
            println!("Licencia inválida.");
        }
    } else {
        println!("Licencia inválida.");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_flag_is_accepted() {
        // En los tests sí está permitido declarar la flag correcta ya que #[cfg(test)] no se compila en release
        assert!(check_license("H4L{RUST_VM_BYT3C0D3}"));
    }

    #[test]
    fn invalid_flag_is_rejected() {
        assert!(!check_license("H4L{FAKE_FLAG_DO_NOT_SUBMIT}"));
        assert!(!check_license("H4L{RUST_VM_BYT3C0D4}"));
        assert!(!check_license("H4L{RUST_VM_BYT3C0D}"));
        assert!(!check_license("H4L{RUST_VM_BYT3C0D30}"));
    }

    #[test]
    fn invalid_format_is_rejected() {
        assert!(!check_license("H4X{RUST_VM_BYT3C0D3}"));
        assert!(!check_license("H4L_RUST_VM_BYT3C0D3_"));
    }
}
