using Microsoft.Extensions.Hosting;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

class RustModelInitializerService : IHostedService
{
	private readonly RustEngineConfiguration _configuration;

	public RustModelInitializerService(
		RustEngineConfiguration configuration
	)
	{
		_configuration = configuration;
	}

	public Task StartAsync(CancellationToken cancellationToken)
	{
		switch (_configuration.DeviceType)
		{
			case DeviceType.Cpu:
				{
					RustWrapper.init_model_cpu();
					break;
				}
			case DeviceType.Gpu:
				{
					RustWrapper.init_model_gpu();
					break;
				}
		}
		return Task.CompletedTask;
	}

	public Task StopAsync(CancellationToken cancellationToken)
	{
		return Task.CompletedTask;
	}
}