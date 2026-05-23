use burn::tensor::Float;

#[no_mangle]
pub unsafe extern "C" fn free_string_array(arr: StringArray) {
  if arr.ptr.is_null() {
    return;
  }

  log::debug!("[free_string_array]: Array Pointer Address: {:p}", arr.ptr);

  let slice = std::slice::from_raw_parts_mut(arr.ptr, arr.len);
  for &mut ptr in slice.iter_mut() {
    drop(std::ffi::CString::from_raw(ptr));
  }
  drop(Vec::from_raw_parts(arr.ptr, arr.len, arr.len));
}

#[repr(C)]
pub struct StringArray {
  pub ptr: *mut *mut std::ffi::c_char,
  pub len: usize,
}

#[no_mangle]
pub unsafe extern "C" fn free_usize_array(arr: UsizeArray) {
  if arr.ptr.is_null() {
    return;
  }
  log::debug!("[free_usize_array]: Array Pointer Address: {:p}", arr.ptr);
  drop(Vec::from_raw_parts(arr.ptr, arr.len, arr.len));
}

#[repr(C)]
pub struct UsizeArray {
  pub ptr: *mut usize,
  pub len: usize,
}

#[no_mangle]
pub unsafe extern "C" fn free_float_array(arr: FloatArray) {
  if arr.ptr.is_null() {
    return;
  }
  log::debug!("[free_usize_array]: Array Pointer Address: {:p}", arr.ptr);
  drop(Vec::from_raw_parts(arr.ptr, arr.len, arr.len));
}

#[repr(C)]
pub struct FloatArray {
  pub ptr: *mut f32,
  pub len: usize,
}
