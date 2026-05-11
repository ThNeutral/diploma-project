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

	public record InferRequest(string base64_encoded_image);

	[HttpPost]
	public async Task<IActionResult> Infer([FromBody] InferRequest req)
	{
		return Ok(_inferenceEngine.Infer(req.base64_encoded_image, 224, 224));
	}
}