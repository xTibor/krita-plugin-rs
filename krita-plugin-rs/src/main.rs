use std::io::{self, Write, Read};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let width: usize = args[1].parse().unwrap();
    let height: usize = args[2].parse().unwrap();

    let data_size = width * height * 4;
    let mut data: Vec<u8> = vec![0; data_size];

    {
        let stdin = io::stdin();
        let mut handle = stdin.lock();
        handle.read_exact(&mut data).unwrap();
    }

    println!("Hello from Rust!");
    println!("width: {}, height: {}", width, height);
    println!("{:02X} {:02X} {:02X} {:02X}", data[0], data[1], data[2], data[3]);
    println!("{:02X} {:02X} {:02X} {:02X}", data[data_size - 4], data[data_size - 3], data[data_size - 2], data[data_size - 1]);
}
