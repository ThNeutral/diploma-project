using Asp.Versioning;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using PlantDiseaseRecognition.WebApi.Api.Models;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;

namespace PlantDiseaseRecognition.WebApi.Api.Controllers;

[ApiController]
[Route("/api/v{version:apiVersion}/labels")]
[ApiVersion(ApiVersions.One)]
public class LabelsController : ControllerBase
{
	private readonly ILabelSource _labelSource;

	public LabelsController(
		ILabelSource labelSource
	)
	{
		_labelSource = labelSource;
	}

	private record GetLabelsResponse(IReadOnlyList<string> Labels);

	[HttpGet]
	public async Task<IActionResult> GetLabels()
	{
		var labels = _labelSource.GetLabels();
		var response = new GetLabelsResponse(labels);
		return Ok(response);
	}
}