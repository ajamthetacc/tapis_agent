from phoenix.otel import register
#from openinference.instrumentation.openai import OpenAIInstrumentor
import os
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:6006/v1/traces"

# def init_tracer():
#     # Registers the tracer to export to Phoenix
#     tracer_provider = register(
#         project_name="tapis-agent",
#         endpoint="http://localhost:6006/v1/traces",
#         set_global_tracer_provider=False
#     )
#     # Automatically instruments OpenAI calls
#     OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
#     return tracer_provider


def init_tracer():
    register(
        project_name="tapis-agent",set_global_tracer_provider=False
    )