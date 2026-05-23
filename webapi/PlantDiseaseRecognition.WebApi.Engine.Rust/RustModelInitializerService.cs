using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

class RustModelInitializerService : IHostedService
{
	private readonly ILogger<RustModelInitializerService> _logger;
	private readonly RustEngineConfiguration _configuration;

	public RustModelInitializerService(
		RustEngineConfiguration configuration,
		ILogger<RustModelInitializerService> logger
	)
	{
		_logger = logger;
		_configuration = configuration;
	}

	public Task StartAsync(CancellationToken cancellationToken)
	{
		switch (_configuration.DeviceType)
		{
			case DeviceType.Cpu:
				{
					_logger.LogDebug("{MethodName}: Initializing model on {DeviceType}", nameof(StartAsync), DeviceType.Cpu);
					RustWrapper.init_model_cpu();
					break;
				}
			case DeviceType.Gpu:
				{
					_logger.LogDebug("{MethodName}: Initializing model on {DeviceType}", nameof(StartAsync), DeviceType.Gpu);
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