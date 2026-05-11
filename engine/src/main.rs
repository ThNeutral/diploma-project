use burn::backend::ndarray::NdArray;
use burn::tensor;

use crate::models::effnet_b0::Model;

mod models;

fn main() {
    let device = Default::default();

    let pdr_model = Model::default();

    let input = tensor::Tensor::<NdArray<f32>, 4>::zeros([1, 3, 224, 224], &device);
    println!("Input shape {}", input.shape());
    let output = pdr_model.forward(input);
    println!("Output {}", output);
}
