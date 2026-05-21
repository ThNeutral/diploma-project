namespace PlantDiseaseRecognition.WebApi.Engine.Contracts;

public interface IInferenceEngine
{
	float Infer(Stream data, int width, int height);
}
