using System.Runtime.InteropServices;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

[StructLayout(LayoutKind.Sequential)]
public struct StringArray
{
	public IntPtr Ptr;
	public nuint Len;
}

[StructLayout(LayoutKind.Sequential)]
public struct UsizeArray
{
	public IntPtr Ptr;
	public nuint Len;
}

[StructLayout(LayoutKind.Sequential)]
public struct FloatArray
{
	public IntPtr Ptr;
	public nuint Len;
}

[StructLayout(LayoutKind.Sequential)]
public struct ImageView
{
	public IntPtr Ptr;
	public nuint Len;
	public nuint Width;
	public nuint Height;
	public nuint Channels;
}