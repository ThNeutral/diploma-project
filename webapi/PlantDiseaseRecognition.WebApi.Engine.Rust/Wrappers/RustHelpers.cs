using System.Runtime.InteropServices;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

internal static class RustHelpers
{
	public unsafe static List<float> ToList(this FloatArray arr)
	{
		var list = new List<float>((int)arr.Len);
		var ptr = (float*)arr.Ptr;
		for (int i = 0; i < (int)arr.Len; i++)
		{
			list.Add(ptr[i]);
		}

		RustWrapper.free_float_array(arr);
		return list;
	}

	public static List<int> ToList(this UsizeArray arr)
	{
		var list = new List<int>((int)arr.Len);
		for (int i = 0; i < (int)arr.Len; i++)
		{
			var value = Marshal.ReadIntPtr(arr.Ptr, i * IntPtr.Size);
			list.Add((int)value);
		}

		RustWrapper.free_usize_array(arr);
		return list;
	}

	public static List<string> ToList(this StringArray arr)
	{
		var list = new List<string>((int)arr.Len);
		for (int i = 0; i < (int)arr.Len; i++)
		{
			var ptr = Marshal.ReadIntPtr(arr.Ptr, i * IntPtr.Size);
			var str = Marshal.PtrToStringUTF8(ptr)
				?? throw new InvalidOperationException("Received unmarshallable string.");

			list.Add(str);
		}

		RustWrapper.free_string_array(arr);
		return list;
	}
}