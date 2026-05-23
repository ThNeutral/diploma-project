using Asp.Versioning;
using Microsoft.AspNetCore.Mvc;
using PlantDiseaseRecognition.WebApi.Api.Models;
using PlantDiseaseRecognition.WebApi.Api.Utils;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;

namespace PlantDiseaseRecognition.WebApi.Api.Controllers;

[ApiController]
[Route("/api/v{version:apiVersion}/inference")]
[ApiVersion(ApiVersions.One)]
public class InferenceController : ControllerBase
{
	private readonly ILogger<InferenceController> _logger;

	private readonly IMetadataSource _metadataSource;
	private readonly IInferenceEngine _inferenceEngine;

	public InferenceController(
		IMetadataSource metadataSource,
		IInferenceEngine inferenceEngine,
		ILogger<InferenceController> logger
	)
	{
		_metadataSource = metadataSource;
		_inferenceEngine = inferenceEngine;
		_logger = logger;
	}

	public record InferRequest(int Height, int Width);
	public record InferResponse(IReadOnlyDictionary<int, float> Predictions);

	[HttpPost]
	public async Task<IActionResult> Infer([FromQuery] int width, [FromQuery] int height)
	{
		var inputSize = _metadataSource.GetInputSize();
		var (expectedWidth, expectedHeight) = (inputSize[2], inputSize[3]);
		if (width != expectedWidth || height != expectedHeight)
		{
			_logger.LogWarning($"Metadata check failed. Received 3x{width}x{width}. Expected 3x{expectedWidth}x{expectedHeight}");
			return BadRequest(ErrorResponse.WithMessage($"Invalid size of image. Expected 3x{expectedWidth}x{expectedHeight}"));
		}

		var results = _inferenceEngine.Infer(Request.Body, width, height);

		return Ok(new InferResponse(results));
	}
}