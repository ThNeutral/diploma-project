using System.Runtime.InteropServices;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

internal class RustLoggerService : IHostedService
{
	private static ILogger<RustLoggerService>? _logger;

	public RustLoggerService(ILogger<RustLoggerService> logger)
	{
		_logger = logger;
	}

	public Task StartAsync(CancellationToken cancellationToken)
	{
		RustWrapper.init_logging(LogCallback);
		return Task.CompletedTask;
	}

	public Task StopAsync(CancellationToken cancellationToken)
	{
		return Task.CompletedTask;
	}

	private static void LogCallback(int level, IntPtr message)
	{
		var msg = Marshal.PtrToStringUTF8(message) ?? "<null>";
		var logLevel = level switch
		{
			0 => LogLevel.Trace,
			1 => LogLevel.Debug,
			2 => LogLevel.Information,
			3 => LogLevel.Warning,
			4 => LogLevel.Error,
			_ => LogLevel.Information
		};

		_logger?.Log(logLevel, "[Rust]: {Message}", msg);
	}
}