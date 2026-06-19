pub struct Vm<'a> {
    pc: usize,
    acc: u8,
    ok: bool,
    input: &'a [u8],
}

impl<'a> Vm<'a> {
    pub fn new(input: &'a [u8]) -> Self {
        Self {
            pc: 0,
            acc: 0,
            ok: true,
            input,
        }
    }

    pub fn run(&mut self, bytecode: &[u8]) -> bool {
        while self.pc + 2 < bytecode.len() {
            let op = bytecode[self.pc];
            let arg1 = bytecode[self.pc + 1];
            let _arg2 = bytecode[self.pc + 2]; // Reservado para alineación de 3 bytes
            self.pc += 3;

            match op {
                0x01 => {
                    // LOAD_INPUT
                    if (arg1 as usize) < self.input.len() {
                        self.acc = self.input[arg1 as usize];
                    } else {
                        return false;
                    }
                }
                0x02 => {
                    // XOR
                    self.acc ^= arg1;
                }
                0x03 => {
                    // ADD
                    self.acc = self.acc.wrapping_add(arg1);
                }
                0x04 => {
                    // SUB
                    self.acc = self.acc.wrapping_sub(arg1);
                }
                0x05 => {
                    // ROL
                    self.acc = self.acc.rotate_left(arg1 as u32);
                }
                0x06 => {
                    // ROR
                    self.acc = self.acc.rotate_right(arg1 as u32);
                }
                0x07 => {
                    // CMP
                    if self.acc != arg1 {
                        self.ok = false;
                    }
                }
                0x08 => {
                    // JNZ_FAIL (Termina de inmediato si ok es falso)
                    if !self.ok {
                        return false;
                    }
                }
                0x09 => {
                    // HALT_OK
                    return self.ok;
                }
                0x0A => {
                    // HALT_FAIL
                    return false;
                }
                _ => {
                    // Opcode desconocido
                    return false;
                }
            }
        }
        self.ok
    }
}
