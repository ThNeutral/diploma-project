using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;

namespace PlantDiseaseRecognition.WebApi.LoadTesting;

public class TestWebApplicationFactory : WebApplicationFactory<Program>
{
	private readonly DeviceType _deviceType;

	public TestWebApplicationFactory(DeviceType deviceType)
	{
		_deviceType = deviceType;
	}

	protected override IHost CreateHost(IHostBuilder builder)
	{
		builder.ConfigureHostConfiguration(config =>
		{
			config.AddInMemoryCollection(new Dictionary<string, string?>
			{
				["ApiConfiguration:RustEngine:DeviceType"] = _deviceType.ToString()
			});
		});

		return base.CreateHost(builder);
	}
}