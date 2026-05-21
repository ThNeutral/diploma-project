using System.Runtime.InteropServices;
using Microsoft.Extensions.Logging;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

public class RustLabelSource : IMetadataSource
{
	private readonly ILogger<RustLabelSource> _logger;

	private IReadOnlyList<string>? _cachedLabels;

	public RustLabelSource(
		ILogger<RustLabelSource> logger
	)
	{
		_logger = logger;
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

