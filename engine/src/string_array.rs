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
