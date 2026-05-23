use std::ffi::CString;

type LogCallback = extern "C" fn(level: i32, message: *const std::ffi::c_char);

static LOG_CALLBACK: std::sync::OnceLock<LogCallback> = std::sync::OnceLock::new();

static FFI_LOGGER: FfiLogger = FfiLogger;

#[no_mangle]
pub extern "C" fn init_logging(cb: LogCallback) {
  LOG_CALLBACK.set(cb).ok();

  log::set_logger(&FFI_LOGGER)
    .map(|()| log::set_max_level(log::LevelFilter::Trace))
    .ok();
}

struct FfiLogger;

impl log::Log for FfiLogger {
  fn log(&self, record: &log::Record) {
    if !self.enabled(record.metadata()) {
      return;
    }

    if let Some(cb) = LOG_CALLBACK.get() {
      let msg = CString::new(record.args().to_string()).unwrap();
      let level = match record.level() {
        log::Level::Error => 4,
        log::Level::Warn => 3,
        log::Level::Info => 2,
        log::Level::Debug => 1,
        log::Level::Trace => 0,
      };
      cb(level, msg.as_ptr());
    }
  }

  fn enabled(&self, metadata: &log::Metadata) -> bool {
    let target = metadata.target();
    !target.starts_with("burn")
      && !target.starts_with("wgpu")
      && !target.starts_with("naga")
      && !target.starts_with("wgpu_core")
  }
  fn flush(&self) {}
}
