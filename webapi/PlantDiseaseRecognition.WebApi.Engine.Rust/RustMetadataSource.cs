using System.Runtime.InteropServices;
using Microsoft.Extensions.Logging;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

public class RustMetadataSource : IMetadataSource
{
	private readonly ILogger<RustMetadataSource> _logger;

	private IReadOnlyList<string>? _cachedLabels;
	private IReadOnlyList<int>? _cachedInputSize;

	public RustMetadataSource(
		ILogger<RustMetadataSource> logger
	)
	{
		_logger = logger;
	}

	public IReadOnlyList<int> GetInputSize()
	{
		if (_cachedInputSize is not null)
		{
			return _cachedInputSize;
		}

		var inputSizeFromRust = RustWrapper.get_input_size_unsafe();

		_logger.LogDebug("[{Method}]: Received data from rust: Ptr: {Ptr:X}, Len: {Len}",
			nameof(GetInputSize),
			inputSizeFromRust.Ptr,
			inputSizeFromRust.Len);

		var inputSizeList = new List<int>();
		checked
		{
			inputSizeList.Capacity = (int)inputSizeFromRust.Len;
		}

		for (var i = 0; i < inputSizeList.Capacity; i++)
		{
			var ptr = Marshal.ReadIntPtr(inputSizeFromRust.Ptr, i * IntPtr.Size);
			checked
			{
				inputSizeList.Add((int)ptr);

			}
		}

		_logger.LogDebug("[{Method}]: Parsed data: Input size: [{InputSize}], Ptr: {Ptr:X}",
			nameof(GetInputSize),
			string.Join(", ", inputSizeList),
			inputSizeFromRust.Ptr);

		RustWrapper.free_usize_array(inputSizeFromRust);

		_logger.LogDebug("[{Method}]: Freed usize array", nameof(GetInputSize));

		_cachedInputSize = inputSizeList;
		return inputSizeList;
	}

	public IReadOnlyList<string> GetLabels()
	{
		if (_cachedLabels is not null)
		{
			return _cachedLabels;
		}

		var labelsFromRust = RustWrapper.get_labels_array_unsafe();

		_logger.LogDebug("[{Method}]: Received data from rust: Ptr: {Ptr:X}, Len: {Len}",
			nameof(GetLabels),
			labelsFromRust.Ptr,
			labelsFromRust.Len);

		var labelsList = new List<string>();
		checked
		{
			labelsList.Capacity = (int)labelsFromRust.Len;
		}

		for (var i = 0; i < labelsList.Capacity; i++)
		{
			var ptr = Marshal.ReadIntPtr(labelsFromRust.Ptr, i * IntPtr.Size);
			var str = Marshal.PtrToStringUTF8(ptr)
				?? throw new InvalidOperationException("Received unmarshallable string.");

			labelsList.Add(str);
		}

		_logger.LogDebug("[{Method}]: Parsed data: Labels: {Lables}, Ptr: {Ptr:X}",
			nameof(GetLabels),
			string.Join(", ", labelsList),
			labelsFromRust.Ptr);

		RustWrapper.free_string_array(labelsFromRust);

		_logger.LogDebug("[{Method}]: Freed string array", nameof(GetLabels));

		_cachedLabels = labelsList;
		return _cachedLabels;
	}
}

