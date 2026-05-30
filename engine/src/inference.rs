use std::fmt;

use burn::{
  backend::{
    ndarray::{NdArray, NdArrayDevice},
    wgpu::WgpuDevice,
    Wgpu,
  },
  prelude::Backend,
  tensor::{Shape, TensorData},
  Tensor,
};

use crate::{
  array::FloatArray,
  models::effnet_b0::{Model, METADATA},
};

#[repr(C)]
pub struct ImageView {
  pub ptr: *const u8,
  pub len: usize,
  pub width: usize,
  pub height: usize,
  pub channels: usize,
}

impl fmt::Display for ImageView {
  fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
    write!(
      f,
      "ImageView({}x{}x{})",
      self.channels, self.width, self.height
    )
  }
}

#[no_mangle]
pub extern "C" fn init_model_cpu() {
  let device = NdArrayDevice::default();
  let model = Model::<NdArray>::default();
  let tensor = Tensor::zeros(METADATA.input_shape, &device);

  model.forward(tensor);
}

#[no_mangle]
pub extern "C" fn run_inference_on_cpu(view: ImageView) -> FloatArray {
  let device = NdArrayDevice::default();
  log::debug!(
    "[run_inference_on_cpu] Running inference on {:?} for {}",
    device,
    view
  );

  let model = Model::<NdArray>::default();

  let tensor = image_view_to_tensor(&view, &device);

  let result = model.forward(tensor);
  log::debug!("[run_inference_on_cpu] Inference result: {:?}", result);

  let data = result.into_data();
  let mut floats: Vec<f32> = data.to_vec().unwrap();

  floats.shrink_to_fit();

  let mut floats = std::mem::ManuallyDrop::new(floats);

  FloatArray {
    ptr: floats.as_mut_ptr(),
    len: floats.len(),
  }
}

#[no_mangle]
pub extern "C" fn init_model_gpu() {
  let device = WgpuDevice::default();
  let model = Model::<Wgpu>::default();
  let tensor = Tensor::zeros(METADATA.input_shape, &device);
  model.forward(tensor);
}

#[no_mangle]
pub extern "C" fn run_inference_on_gpu(view: ImageView) -> FloatArray {
  let device = WgpuDevice::default();
  log::debug!(
    "[run_inference_on_gpu] Running inference on {:?} for {}",
    device,
    view
  );

  let model = Model::<Wgpu>::default();

  let tensor = image_view_to_tensor(&view, &device);

  let result = model.forward(tensor);
  log::debug!("[run_inference_on_gpu] Inference result: {:?}", result);

  let data = result.into_data();
  let mut floats: Vec<f32> = data.to_vec().unwrap();

  floats.shrink_to_fit();

  let mut floats = std::mem::ManuallyDrop::new(floats);

  FloatArray {
    ptr: floats.as_mut_ptr(),
    len: floats.len(),
  }
}

fn image_view_to_tensor<B>(img: &ImageView, device: &B::Device) -> Tensor<B, 4>
where
  B: Backend,
{
  let pixels: &[u8] = unsafe { std::slice::from_raw_parts(img.ptr, img.len) };

  let floats: Vec<f32> = pixels
    .iter()
    .map(|&p| p as f32 / 255.0)
    .enumerate()
    .map(|(i, p)| {
        let channel = i / (img.width as usize * img.height as usize);
        let mean = [0.485, 0.456, 0.406][channel];
        let std  = [0.229, 0.224, 0.225][channel];
        (p - mean) / std
    })
    .collect();
  
  let data = TensorData::new(
    floats,
    Shape::new([
      1,
      img.channels as usize,
      img.height as usize,
      img.width as usize,
    ]),
  );

  Tensor::<B, 4>::from_data(data, device)
}
