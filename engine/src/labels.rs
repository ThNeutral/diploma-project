use crate::models::effnet_b0::METADATA;
use crate::string_array::StringArray;

#[no_mangle]
pub extern "C" fn get_labels_array_unsafe() -> StringArray {
    let strings = METADATA
        .classes
        .into_iter()
        .map(|&s| std::ffi::CString::new(s).unwrap().into_raw())
        .collect::<Vec<_>>();

    let mut strings = std::mem::ManuallyDrop::new(strings);
    StringArray {
        ptr: strings.as_mut_ptr(),
        len: strings.len(),
    }
}
