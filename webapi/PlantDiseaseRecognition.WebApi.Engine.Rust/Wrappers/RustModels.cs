using System.Runtime.InteropServices;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

[StructLayout(LayoutKind.Sequential)]
public struct StringArray
{
	public IntPtr Ptr;
	public nuint Len;
}

[StructLayout(LayoutKind.Sequential)]
public struct ImageView
{
	public IntPtr Ptr;
	public nuint Len;
	public uint Width;
	public uint Height;
	public byte Channels;
}