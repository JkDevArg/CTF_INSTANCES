// ISA-V2 interpreter. Bytes come from a fetch fn that materializes them
// on demand from the sharded backing store. The encoded byte is then
// XOR'd with a position-keyed keystream before dispatch.
//
// Spec: v2/docs/isa_v2.md.
// Living reference: v2/tools/reference_vm.py.

#[inline(always)]
fn keystream(pc: usize, seed: u32) -> u8 {
    let mut x = (pc as u32).wrapping_add(seed);
    x = x.wrapping_mul(0x9E3779B1);
    x ^= x >> 13;
    x = x.wrapping_mul(0x85EBCA77);
    x ^= x >> 16;
    (x & 0xFF) as u8
}

pub type Fetch = fn(usize) -> u8;

pub struct Vm<'a> {
    regs: [u32; 8],
    state: u32,
    crc: u32,
    ok: bool,
    pc: usize,
    seed: u32,
    program_len: usize,
    input: &'a [u8],
    charset: &'static [u8],
}

impl<'a> Vm<'a> {
    pub fn new(
        input: &'a [u8],
        charset: &'static [u8],
        seed: u32,
        program_len: usize,
    ) -> Self {
        Self {
            regs: [0; 8],
            state: 0,
            crc: 0,
            ok: true,
            pc: 0,
            seed,
            program_len,
            input,
            charset,
        }
    }

    pub fn run(mut self, fetch: Fetch) -> bool {
        while self.pc < self.program_len {
            let op = fetch(self.pc) ^ keystream(self.pc, self.seed);
            self.pc += 1;
            if !self.step(op, fetch) {
                return false;
            }
        }
        self.ok
    }

    fn read(&mut self, fetch: Fetch, k: usize) -> Option<[u8; 5]> {
        if self.pc + k > self.program_len {
            return None;
        }
        let mut buf = [0u8; 5];
        for i in 0..k {
            buf[i] = fetch(self.pc + i) ^ keystream(self.pc + i, self.seed);
        }
        self.pc += k;
        Some(buf)
    }

    fn step(&mut self, op: u8, fetch: Fetch) -> bool {
        let n = self.program_len;
        match op {
            0x01 => {
                self.pc = n;
            }
            0x02 => {
                self.ok = false;
                self.pc = n;
            }
            0x03 => {}
            0x04 => {
                if !self.ok {
                    return false;
                }
            }
            0x05 => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                if self.input.len() != b[0] as usize {
                    self.ok = false;
                }
            }
            0x06 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let (pos, val) = (b[0] as usize, b[1]);
                if pos >= self.input.len() || self.input[pos] != val {
                    self.ok = false;
                }
            }
            0x07 => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                let pos = b[0] as usize;
                if pos >= self.input.len() || !self.charset.contains(&self.input[pos]) {
                    self.ok = false;
                }
            }
            0x08 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let (rd, pos) = ((b[0] & 7) as usize, b[1] as usize);
                if pos >= self.input.len() {
                    return false;
                }
                self.regs[rd] = self.input[pos] as u32;
            }
            0x09 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                self.regs[(b[0] & 7) as usize] = b[1] as u32;
            }
            0x0A => {
                let b = match self.read(fetch, 5) {
                    Some(v) => v,
                    None => return false,
                };
                self.regs[(b[0] & 7) as usize] =
                    u32::from_le_bytes([b[1], b[2], b[3], b[4]]);
            }
            0x0B => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let (rd, lane) = ((b[0] & 7) as usize, (b[1] & 3) as u32);
                self.regs[rd] = (self.state >> (lane * 8)) & 0xFF;
            }
            0x0C => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                self.regs[(b[0] & 7) as usize] = self.regs[(b[1] & 7) as usize];
            }
            0x0D | 0x0F | 0x11 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let rd = (b[0] & 7) as usize;
                let rs = (b[1] & 7) as usize;
                let a = (self.regs[rd] & 0xFF) as u8;
                let v = (self.regs[rs] & 0xFF) as u8;
                let r = match op {
                    0x0D => a ^ v,
                    0x0F => a.wrapping_add(v),
                    _ => a.wrapping_sub(v),
                };
                self.regs[rd] = r as u32;
            }
            0x0E | 0x10 | 0x12 | 0x13 | 0x14 | 0x15 | 0x16 | 0x18 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let rd = (b[0] & 7) as usize;
                let imm = b[1];
                let a = (self.regs[rd] & 0xFF) as u8;
                match op {
                    0x0E => self.regs[rd] = (a ^ imm) as u32,
                    0x10 => self.regs[rd] = a.wrapping_add(imm) as u32,
                    0x12 => self.regs[rd] = a.wrapping_sub(imm) as u32,
                    0x13 => self.regs[rd] = a.wrapping_mul(imm) as u32,
                    0x14 => {
                        let k = (imm as u32) & 7;
                        self.regs[rd] = if k == 0 { a as u32 } else { a.rotate_left(k) as u32 };
                    }
                    0x15 => {
                        let k = (imm as u32) & 7;
                        self.regs[rd] = if k == 0 { a as u32 } else { a.rotate_right(k) as u32 };
                    }
                    0x16 => self.regs[rd] = (a & imm) as u32,
                    0x18 => {
                        if a != imm {
                            self.ok = false;
                        }
                    }
                    _ => unreachable!(),
                }
            }
            0x17 => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                self.regs[(b[0] & 7) as usize] &= 0xFF;
            }
            0x19 => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                let v = (self.regs[(b[0] & 7) as usize] & 0xFF) as u32;
                self.state = (self.state ^ v).rotate_left(7);
                self.state = self.state.wrapping_add(v << 16);
            }
            0x1A => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                let imm = b[0] as u32;
                self.state = self.state.rotate_left(13) ^ (imm << 8) ^ 0x9E3779B9;
            }
            0x1B => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                let v = (self.regs[(b[0] & 7) as usize] & 0xFF) as u32;
                self.crc = self.crc.rotate_left(5) ^ v;
                self.crc = self.crc.wrapping_add(0x9E3779B9);
                self.crc = self.crc.rotate_left(11) ^ (v << 17);
            }
            0x1C => {
                let b = match self.read(fetch, 4) {
                    Some(v) => v,
                    None => return false,
                };
                self.crc = u32::from_le_bytes([b[0], b[1], b[2], b[3]]);
            }
            0x1D => {
                let b = match self.read(fetch, 4) {
                    Some(v) => v,
                    None => return false,
                };
                let t = u32::from_le_bytes([b[0], b[1], b[2], b[3]]);
                if self.crc != t {
                    self.ok = false;
                }
            }
            0x1E => {
                let b = match self.read(fetch, 1) {
                    Some(v) => v,
                    None => return false,
                };
                let rel = b[0] as i8 as isize;
                let new_pc = (self.pc as isize) + rel;
                if new_pc < 0 || new_pc as usize > n {
                    return false;
                }
                self.pc = new_pc as usize;
            }
            0x1F | 0x20 => {
                let b = match self.read(fetch, 2) {
                    Some(v) => v,
                    None => return false,
                };
                let rd = (b[0] & 7) as usize;
                let rel = b[1] as i8 as isize;
                let cond = (self.regs[rd] & 0xFF) == 0;
                let take = if op == 0x1F { cond } else { !cond };
                if take {
                    let new_pc = (self.pc as isize) + rel;
                    if new_pc < 0 || new_pc as usize > n {
                        return false;
                    }
                    self.pc = new_pc as usize;
                }
            }
            0x21 => {
                let b = match self.read(fetch, 4) {
                    Some(v) => v,
                    None => return false,
                };
                self.state = u32::from_le_bytes([b[0], b[1], b[2], b[3]]);
            }
            _ => return false,
        }
        true
    }
}
