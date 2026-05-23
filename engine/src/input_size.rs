use crate::{array::UsizeArray, models::effnet_b0::METADATA};

#[no_mangle]
pub extern "C" fn get_input_size_unsafe() -> UsizeArray {
  let input_shape = METADATA
    .input_shape
    .into_iter()
    .map(|x| x)
    .collect::<Vec<_>>();
  let mut input_shape = std::mem::ManuallyDrop::new(input_shape);

  return UsizeArray {
    ptr: input_shape.as_mut_ptr(),
    len: input_shape.len(),
  };
}
