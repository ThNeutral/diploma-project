using System.Text.Json;
using PlantDiseaseRecognition.WebApi.Api.Configurations;
using PlantDiseaseRecognition.WebApi.Api.Extensions;
using PlantDiseaseRecognition.WebApi.Api.Models;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Configurations;
using PlantDiseaseRecognition.WebApi.Engine.Rust.IoC;
using PlantDiseaseRecognition.WebApi.Engine.Rust.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

builder.Services
	.AddControllers()
	.AddJsonOptions(o =>
	{
		o.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.KebabCaseLower;
	});

builder.Services
	.AddApiVersioning()
	.AddMvc();

var config = builder
	.Services
	.AddApiConfiguration(
		builder
			.Configuration
			.GetSection(ApiConfiguration.SectionName)
	);

builder.Services
	.AddRustEngine(config.RustEngine);

var app = builder.Build();

app.UseExceptionHandler();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
	app.MapOpenApi();
	app.UseSwaggerUI(o =>
	{
		o.SwaggerEndpoint("/openapi/v1.json", "v1");
	});
}

if (app.Environment.IsProduction())
{
	app.UseHttpsRedirection();
}

app.MapControllers();
app.Run();
