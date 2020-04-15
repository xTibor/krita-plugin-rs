use image::{Bgra, ImageBuffer};
use std::env;
use std::io::{self, Read, Write};
use std::num::NonZeroU32;
use wfc_image::*;

// The image crate doesn't export BGRA image types for some reason.
type BgraImage = ImageBuffer<Bgra<u8>, Vec<u8>>;

fn main() {
    let args: Vec<String> = env::args().collect();
    let width: u32 = args[1].parse().unwrap();
    let height: u32 = args[2].parse().unwrap();

    let data_size = (width * height * 4) as usize;
    let mut data: Vec<u8> = vec![0; data_size];
    io::stdin().read_exact(&mut data).unwrap();

    let image_buffer = BgraImage::from_raw(width, height, data).unwrap();

    let wfc_input_image = image::open("src/ditto.png").unwrap();
    let wfc_pattern_size = NonZeroU32::new(3).unwrap();
    let wfc_output_size = Size::new(width, height);
    let wfc_orientation = &[Orientation::Original];
    let wfc_retries = retry::NumTimes(10);
    let wfc_result = wfc_image::generate_image(&wfc_input_image, wfc_pattern_size, wfc_output_size, wfc_orientation, WrapXY, ForbidNothing, wfc_retries);
    let image_buffer = wfc_result.unwrap().into_bgra();

    io::stdout().write_all(&image_buffer.into_raw()).unwrap();
}
