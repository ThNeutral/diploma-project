namespace PlantDiseaseRecognition.WebApi.Engine.Contracts;

public interface IInferenceEngine
{
	float Infer(string base64EncodedImage, int width, int height);
}
