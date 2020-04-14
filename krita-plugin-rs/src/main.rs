use std::io::{self, Write, Read};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let width: usize = args[1].parse().unwrap();
    let height: usize = args[2].parse().unwrap();

    let data_size = width * height * 4;
    let mut data: Vec<u8> = vec![0; data_size];
    io::stdin().read_exact(&mut data).unwrap();

    for y in 0..height {
        for x in 0..width {
            let i = (y * width + x) * 4;
            data[i + 0] = (x & y) as u8; // B
            data[i + 1] = (x | y) as u8; // G
            data[i + 2] = (x ^ y) as u8; // R

            // Keep alpha for demo
            //data[i + 3] = 0xFF; // A
        }
    }

    io::stdout().write_all(&data).unwrap();
}
