using Microsoft.Extensions.DependencyInjection;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust.IoC;

public static class ServiceCollectionExtensions
{
	public static void AddRustEngine(this IServiceCollection services, RustEngineConfiguration configuration)
	{
		services.AddSingleton(configuration);

		services.AddScoped<IInferenceEngine, RustInferenceEngine>();
		services.AddScoped<IMetadataSource, RustMetadataSource>();
		services.AddHostedService<RustLoggerService>();
		services.AddHostedService<RustModelInitializerService>();
	}
}