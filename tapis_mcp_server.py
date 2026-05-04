from __future__ import annotations
import sys
import logging
from mcp.server.fastmcp import FastMCP
from tapipy.tapis import Tapis
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from create_embeddings import initializeVectorIndex
# Use stderr so it doesn't interfere with the MCP protocol
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("Tapis-general-purpose-Server")

# Initialize Tapis (Use env vars for security)
t = Tapis(base_url="", username="", password="")
t.get_tokens()

initializeVectorIndex()

@mcp.tool()
def list_tapis_systems():
    """List all available compute systems in Tapis."""
    systems = t.systems.getSystems()
    return [s.id for s in systems]

@mcp.tool()
def get_system_status(system_id: str):
    """Check if a specific Tapis system is enabled."""
    sys_info = t.systems.getSystem(systemId=system_id)
    return f"System {system_id} is {'Enabled' if sys_info.enabled else 'Disabled'}"

@mcp.tool()
def list_files(system_id: str, path: str):
    """
    Step 1/2 in Workflow: List files in a specific Tapis system and path.
    Useful for verifying data existence before running a job.
    """
    files = t.files.listFiles(systemId=system_id, path=path)
    return [f.name for f in files]

@mcp.tool()
def search_apps(keyword: str):
    """
    Step 3 in Workflow: Search for available Tapis applications by keyword.
    Helps the agent find the correct appId and appVersion.
    """
    apps = t.apps.getApps()
    return [f"{a.id}-{a.version}" for a in apps if keyword.lower() in a.id.lower()]

@mcp.tool()
def submit_job(
    name: str, 
    app_id: str, 
    app_version: str, 
    exec_system_id: str,
    # Use | None instead of Optional, and lowercase list/dict
    file_inputs: list[dict[str, str]] | None = None 
):
    """
    Step 4 in Workflow: Submits a job to Tapis. 
    Requires IDs gathered from list_systems and search_apps.
    """
    job_request = {
        "name": name,
        "appId": app_id,
        "appVersion": app_version,
        "execSystemId": exec_system_id,
        "fileInputs": file_inputs if file_inputs else []
    }
    
    # Validation point: This is where CodeBERT would inspect 'job_request'
    res = t.jobs.submitJob(**job_request)
    return f"Job submitted. Status: {res.status}. UUID: {res.uuid}"

@mcp.tool()
def get_job_status(job_uuid: str):
    """
    Step 5 in Workflow: Poll the status of a submitted job.
    """
    status = t.jobs.getJobStatus(jobUuid=job_uuid)
    return f"Job {job_uuid} is currently: {status.status}"

if __name__ == "__main__":
    mcp.run(transport='stdio')

@mcp.tool()
def search_docs(query: str):
    """Searches Tapis documentation and conceptual guides using Neo4j RAG."""
    # Perform vector similarity search in the graph
    results = vector_db.similarity_search(query, k=3)
    
    # Return the page contents
    return [doc.page_content for doc in results]
    
if __name__ == "__main__":
    mcp.run(transport='stdio')
