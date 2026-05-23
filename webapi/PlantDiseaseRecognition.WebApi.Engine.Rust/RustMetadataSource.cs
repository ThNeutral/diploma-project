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
		var inputSizeList = inputSizeFromRust.ToList();

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
		var labelsList = labelsFromRust.ToList();

		_cachedLabels = labelsList;
		return _cachedLabels;
	}
}

