using Asp.Versioning;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using PlantDiseaseRecognition.WebApi.Api.Models;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;

namespace PlantDiseaseRecognition.WebApi.Api.Controllers;

[ApiController]
[Route("/api/v{version:apiVersion}/metadata")]
[ApiVersion(ApiVersions.One)]
public class LabelsController : ControllerBase
{
	private readonly IMetadataSource _metadataSource;

	public LabelsController(
		IMetadataSource metadataSource
	)
	{
		_metadataSource = metadataSource;
	}

	private record GetLabelsResponse(IReadOnlyList<string> Labels);

	[HttpGet]
	[Route("labels")]
	public async Task<IActionResult> GetLabels()
	{
		var labels = _metadataSource.GetLabels();
		var response = new GetLabelsResponse(labels);
		return Ok(response);
	}

	private record GetInputSizeResponse(IReadOnlyList<int> InputSize);

	[HttpGet]
	[Route("input-size")]
	public async Task<IActionResult> GetInputSize()
	{
		var inputSize = _metadataSource.GetInputSize();
		var response = new GetInputSizeResponse(inputSize);
		return Ok(response);
	}
}