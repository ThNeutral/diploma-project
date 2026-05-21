using Asp.Versioning;
using Microsoft.AspNetCore.Mvc;
using PlantDiseaseRecognition.WebApi.Api.Models;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;

namespace PlantDiseaseRecognition.WebApi.Api.Controllers;

[ApiController]
[Route("/api/v{version:apiVersion}/inference")]
[ApiVersion(ApiVersions.One)]
public class InferenceController : ControllerBase
{
	private readonly IInferenceEngine _inferenceEngine;

	public InferenceController(
		IInferenceEngine inferenceEngine
	)
	{
		_inferenceEngine = inferenceEngine;
	}

	public record InferRequest(IEnumerable<byte> Data, int Height, int Width);

	[HttpPost]
	public async Task<IActionResult> Infer([FromQuery] int width, [FromQuery] int height)
	{
		return Ok(_inferenceEngine.Infer(Request.Body, width, height));
	}
}