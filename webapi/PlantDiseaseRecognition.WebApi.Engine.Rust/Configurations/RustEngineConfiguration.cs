using System.ComponentModel.DataAnnotations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;

public class RustEngineConfiguration
{
	[Required]
	public required DeviceType DeviceType { get; set; }
}