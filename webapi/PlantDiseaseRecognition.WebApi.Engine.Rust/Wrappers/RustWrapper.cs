using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
internal delegate void LogCallback(int level, IntPtr message);

internal static partial class RustWrapper
{
	#region labels

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial StringArray get_labels_array_unsafe();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void free_string_array(StringArray arr);

	#endregion

	#region input_size

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial UsizeArray get_input_size_unsafe();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void free_usize_array(UsizeArray arr);

	#endregion

	#region logging

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_logging(LogCallback callback);

	#endregion

	#region inference_cpu

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_model_cpu();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void run_inference_on_cpu(ImageView view);

	#endregion

	#region inference_gpu

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void init_model_gpu();

	[LibraryImport(DllConstants.Location)]
	[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
	public static partial void run_inference_on_gpu(ImageView view);

	#endregion
}