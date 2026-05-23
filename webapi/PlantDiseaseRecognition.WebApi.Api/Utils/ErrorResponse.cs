namespace PlantDiseaseRecognition.WebApi.Api.Utils;

public class ErrorResponse
{
	public static ErrorResponse WithMessage(string message)
	{
		return new ErrorResponse { Message = message };
	}

	public required string Message { get; init; }
}