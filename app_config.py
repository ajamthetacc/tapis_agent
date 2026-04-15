import os
from dotenv import load_dotenv
from pathlib import Path

HERE = Path(__file__).parent.resolve()
PARENT = Path(__file__).parent.parent.resolve()

# load .env file to environment
# get the path to .env file
path = "/".join(os.path.realpath(__file__).split("/")[0:-1])
env_path = path + "/.env"
load_dotenv(env_path, override=True)

# get all the environment variables
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL", "https://ollama.pods.tacc.develop.tapis.io"
)

## LLMSherpa running local
LLMSHERPA_API_URL = "http://localhost:5010/api/parseDocument?renderFormat=all"

config = {
    # Neo4j DB Config -----------------
    "neo4j_url": NEO4J_URL,
    "neo4j_user": NEO4J_USER,
    "neo4j_password": NEO4J_PASSWORD,
    "neo4j_database": NEO4J_DATABASE,
    # Whether to run the question/answer task on the input benchmark.
    # Will require an LLM config object (see below)
    "run_question_answer": True,
    # Max number of questions that will be asked from the benchmark;
    # Set to 0 to execute the entire suite
    "max_questions_to_ask": 0,
    # LLM Config ----------------------
    # For Ollama ---
    # "llm_provider": "ollama",
    # "llm_name": "llama3.1:8b",
    # "llm_base_url": "https://ollama.pods.tacc.develop.tapis.io",
    # "embedding": {
    #     "model": "mxbai-embed-large",
    #     "dimension": 1024,
    #     "similarity": "cosine",
    #     "node_label": "Embedding",
    # },
    # For Tejas/SambaNova ---
    "llm_provider": "samba_nova",
    "llm_name": "Meta-Llama-3.1-405B-Instruct",
    "llm_base_url": "https://tejas.tacc.utexas.edu/v1/c31853e6-0a58-4483-9e92-e7c32b021d44",
    "samba_nova_api_key": "",
    "embedding": {
        # "model": "E5-Mistral-7B-Instruct",
        "model": "e5-mistral-7B-instruct",
        "dimension": 4096,
        "similarity": "cosine",
        "node_label": "Embedding",
    },
    # Graph Building ------------------
    "source_rag": {
        "type": "pdf",
        "conf": {
            "llmsherpa_api_url": LLMSHERPA_API_URL,
            # assumes the Tapis documentation repo has been checked out in a directory next to this one.
            "pdf_file": os.path.join(
                PARENT, "comp-eng-benchmark/tapis/docs_2_pdf/tapis2pdf.pdf"
            ),
        },
    },
    "vector_index_on_node": "Chunk",
    "vector_index_name": "chunkVectorIndex",
    "benchmark_qa_input_to_rag": os.path.join(HERE, "data/LLM_generated_v2.json"),
    # There are two options here; if running the question/answer task as part of this run,
    # this should be a *directory* that already exists and the program will generate a file
    # name that includes a time stamp for the run, e.g.,
    "rag_llm_generated_output_to_input_benchmark_eval": os.path.join(HERE, "data"),
    # Alternatively, if just running the evaluator, specify a path to a previously generated file, e.g.,
    # "rag_llm_generated_output_to_input_benchmark_eval": os.path.join(HERE, "data", "LLM_generated_v2.json"),
    # Evaluation of the Results -------
    # Whether to run the evaluation of the results (QAEvaluator)
    "run_evaluation": True,
    "benchmark": {
        "use_ollama": False,
        "use_samba_nova":False,
        "use_llm_judge": False,
        # For Ollama Pods
        "model_name_ollama": "llama3.1:8b",
        "model_name_openai": "gpt-4o",
        "model_name_samba_nova": "Meta-Llama-3.1-405B-Instruct",
        "qa_sets_path": os.path.join(HERE, "data/rag_llm_generated_output.json"),
        # Should be a directory that already exists; file will include timestamp.
        "eval_output": os.path.join(
            HERE,
            "data/outputs",
        ),
    },
}

"""
use this config for openai

{
    "neo4j_url": NEO4J_URL,
    "neo4j_user": NEO4J_USER,
    "neo4j_password": NEO4J_PASSWORD,
    "neo4j_database": NEO4J_DATABASE,
    "llm_provider": "openai",
    "llm_name": "gpt-4o",
    "llm_base_url":"https://api.openai.com/v1",
    "embedding": {"model": "text-embedding-3-large",
                  "dimension":3072,
                  "similarity":"cosine",
                  "node_label":"Embedding"
                 },
    "source_rag":{"type":"pdf",
                  "conf":{
                            "llmsherpa_api_url": LLMSHERPA_API_URL,
                            #"pdf_file": "/Users/spadhy/git-repos/documentation/source/technical/tapis2pdf_SHORT.pdf"
                            "pdf_file":  "/Users/spadhy/git-repos/documentation/source/technical/tapis2pdf_FULL.pdf"
                  }},
   
   "vector_index_on_node":"Chunk",
   "vector_index_name":"chunkVectorIndex",
    "benchmark_qa_input_to_rag": "/Users/spadhy/git-repos/graphci4ai/data/tapis_benchmark.json",
    "rag_llm_generated_output_to_input_benchmark_eval":"/Users/spadhy/git-repos/graphci4ai/data/rag_llm_generated_output.json",
    "benchmark": {
    "use_ollama": True,
    "use_llm_judge": True,
    "model_name_ollama": "llama3.1:8b",
    "model_name_openai": "gpt-4o",
    "qa_sets_path": "/Users/spadhy/git-repos/graphci4ai/data/rag_llm_generated_output.json",
    "eval_output": "/Users/spadhy/git-repos/graphci4ai/data/outputs/qa_eval_results_of_rag_output.csv",
    }
}

"""
