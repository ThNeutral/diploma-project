using System.Buffers;
using System.Diagnostics;
using Microsoft.Extensions.Logging;
using PlantDiseaseRecognition.WebApi.Engine.Contracts;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Wrappers;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;

namespace PlantDiseaseRecognition.WebApi.Engine.Rust;

public class RustInferenceEngine : IInferenceEngine
{
	private static readonly ArrayPool<float> Pool = ArrayPool<float>.Shared;

	private readonly ILogger<RustInferenceEngine> _logger;
	private readonly RustEngineConfiguration _configuration;

	public RustInferenceEngine(ILogger<RustInferenceEngine> logger, RustEngineConfiguration configuration)
	{
		_logger = logger;
		_configuration = configuration;
	}

	public async Task<IReadOnlyList<float>> InferAsync(Stream data, int width, int height)
	{
		var size = 3 * width * height;
		var buffer = Pool.Rent(size);
		try
		{
			await ParseStreamIntoBufferAsync(data, buffer, width, height);
			return RunInferenceOnBuffer(buffer, width, height, size);
		}
		finally
		{
			Pool.Return(buffer);
		}
	}

	private unsafe IReadOnlyList<float> RunInferenceOnBuffer(float[] buffer, int width, int height, int size)
	{
		fixed (float* bufferPtr = buffer)
		{
			var view = new ImageView()
			{
				Ptr = (IntPtr)bufferPtr,
				Len = (nuint)size,
				Width = (nuint)width,
				Height = (nuint)height,
				Channels = 3
			};

			_logger.LogInformation($"Sending ImageView({view.Len}: {view.Channels}x{view.Width}x{view.Height}) to Rust.");

			return _configuration.DeviceType switch
			{
				DeviceType.Cpu => RustWrapper.run_inference_on_cpu(view).ToList(),
				DeviceType.Gpu => RustWrapper.run_inference_on_gpu(view).ToList(),
				_ => throw new UnreachableException($"Invalid DeviceType: {_configuration.DeviceType}")
			}
		;
		}
	}

	private async Task ParseStreamIntoBufferAsync(
		Stream data,
		float[] buffer,
		int width,
		int height
	)
	{
		using var image = await Image.LoadAsync<Rgb24>(data);
		_logger.LogInformation($"Received image of size {image.Width}x{image.Height}");


		image.ProcessPixelRows(accessor =>
		{
			for (int row = 0; row < height; row++)
			{
				var pixelRow = accessor.GetRowSpan(row);
				for (int col = 0; col < width; col++)
				{
					var px = pixelRow[col];
					buffer[0 * height * width + row * width + col] = px.R / 255f;
					buffer[1 * height * width + row * width + col] = px.G / 255f;
					buffer[2 * height * width + row * width + col] = px.B / 255f;
				}
			}
		});
	}
}
