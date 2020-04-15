use std::io::{self, Write, Read};
use std::env;
use image::{ImageBuffer, Bgra};

// The image crate doesn't export BGRA image types for some reason.
type BgraImage = ImageBuffer<Bgra<u8>, Vec<u8>>;

fn main() {
    let args: Vec<String> = env::args().collect();
    let width: u32 = args[1].parse().unwrap();
    let height: u32 = args[2].parse().unwrap();

    let data_size = (width * height * 4) as usize;
    let mut data: Vec<u8> = vec![0; data_size];
    io::stdin().read_exact(&mut data).unwrap();

    let mut image_buffer = BgraImage::from_raw(width, height, data).unwrap();

    for y in 0..height {
        for x in 0..width {
            let k = (x ^ y) as u8;
            image_buffer.put_pixel(x, y, Bgra([255, k, 255 - k, k]));
        }
    }

    io::stdout().write_all(&image_buffer.into_raw()).unwrap();
}
