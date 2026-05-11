namespace PlantDiseaseRecognition.WebApi.Engine.Contracts;

public interface ILabelSource
{
	IReadOnlyList<string> GetLabels();
}