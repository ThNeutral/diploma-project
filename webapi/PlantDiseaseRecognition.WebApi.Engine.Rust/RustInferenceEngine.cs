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

	public unsafe float Infer(Stream data, int width, int height)
	{
		var size = 3 * width * height;
		var buffer = Pool.Rent(size);
		try
		{
			ParseStreamIntoBuffer(data, buffer, width, height);
			fixed (float* bufferPtr = buffer)
			{
				var view = new ImageView()
				{
					Ptr = (IntPtr)bufferPtr,
					Len = (nuint)size,
					Width = (uint)width,
					Height = (uint)height,
					Channels = 3
				};

				switch (_configuration.DeviceType)
				{
					case DeviceType.Cpu:
						{
							RustWrapper.run_inference_on_cpu(view);
							return 1;
						}
					case DeviceType.Gpu:
						{
							RustWrapper.run_inference_on_gpu(view);
							return 1;
						}
					default:
						throw new UnreachableException($"Invalid DeviceType: {_configuration.DeviceType}");
				}
			}
		}
		catch (Exception e)
		{
			_logger.LogError(e, "[{function_name}] Failed", nameof(Infer));
			return -1;
		}
		finally
		{
			Pool.Return(buffer);
		}
	}

	private static void ParseStreamIntoBuffer(
		Stream data,
		float[] buffer,
		int width,
		int height
	)
	{
		using var image = Image.Load<Rgb24>(data);

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
