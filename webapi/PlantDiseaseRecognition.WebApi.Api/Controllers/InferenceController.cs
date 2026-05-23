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
	public record InferResponse(IReadOnlyList<float> Predictions);

	[HttpPost]
	public async Task<IActionResult> Infer()
	{
		var inputSize = _metadataSource.GetInputSize();
		var (width, height) = (inputSize[2], inputSize[3]);
		var results = await _inferenceEngine.InferAsync(Request.Body, width, height);

		return Ok(new InferResponse(results));
	}
}