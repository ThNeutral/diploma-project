using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
internal delegate void LogCallback(int level, IntPtr message);

internal static partial class RustWrapper
{
	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial StringArray get_labels_array_unsafe();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void free_string_array(StringArray arr);

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_logging(LogCallback callback);

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_model_cpu();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void run_inference_on_cpu(ImageView view);

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_model_gpu();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void run_inference_on_gpu(ImageView view);
}