using System.ComponentModel.DataAnnotations;
using PlantDiseaseRecognition.WebApi.Api.Configurations;

namespace PlantDiseaseRecognition.WebApi.Api.Extensions;

public static class IConfigurationManagerExtensions
{
	public static ApiConfiguration AddApiConfiguration(
		this IServiceCollection services,
		IConfiguration configuration)
	{
		var apiConfig = configuration.Get<ApiConfiguration>()
				?? throw new InvalidOperationException("ApiConfiguration section is missing.");

		var errors = new List<ValidationResult>();
		if (!Validator.TryValidateObject(apiConfig, new ValidationContext(apiConfig), errors, true))
		{
			var messages = string.Join("; ", errors.Select(e => e.ErrorMessage));
			throw new InvalidOperationException($"ApiConfiguration is invalid: {messages}");
		}

		services
			.AddOptions<ApiConfiguration>()
			.Bind(configuration)
			.ValidateDataAnnotations()
			.ValidateOnStart();

		return apiConfig;
	}
}