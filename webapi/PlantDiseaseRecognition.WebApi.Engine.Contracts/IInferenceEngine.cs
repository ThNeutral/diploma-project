namespace PlantDiseaseRecognition.WebApi.Engine.Contracts;

public interface IInferenceEngine
{
	Task<IReadOnlyList<float>> InferAsync(Stream data, int width, int height);
}
