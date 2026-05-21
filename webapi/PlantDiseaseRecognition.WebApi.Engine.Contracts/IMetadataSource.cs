namespace PlantDiseaseRecognition.WebApi.Engine.Contracts;

public interface IMetadataSource
{
	IReadOnlyList<string> GetLabels();
	IReadOnlyList<int> GetInputSize();
}