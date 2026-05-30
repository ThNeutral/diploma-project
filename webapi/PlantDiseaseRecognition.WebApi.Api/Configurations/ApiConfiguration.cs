using System.ComponentModel.DataAnnotations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;

namespace PlantDiseaseRecognition.WebApi.Api.Configurations;

public class ApiConfiguration
{
	public const string SectionName = "ApiConfiguration";

	[Required]
	public required RustEngineConfiguration RustEngine { get; set; }

	[Required]
	public required int MaxConcurrentRequests { get; set; }
}