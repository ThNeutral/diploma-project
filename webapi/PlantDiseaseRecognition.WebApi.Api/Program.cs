using System.Text.Json;
using PlantDiseaseRecognition.WebApi.Api.Configurations;
using PlantDiseaseRecognition.WebApi.Api.Extensions;
using PlantDiseaseRecognition.WebApi.Engine.Rust.IoC;

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
		o.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower;
	});

builder.Services
	.AddApiVersioning()
	.AddMvc();

var corsAllowAllPolicyName = "AllowAll";
builder.Services.AddCors(options =>
{
	options.AddPolicy(corsAllowAllPolicyName, policy =>
	{
		policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
	});
});

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

app.UseCors(corsAllowAllPolicyName);

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
