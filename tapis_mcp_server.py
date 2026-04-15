import sys
import logging
from mcp.server.fastmcp import FastMCP
from tapipy.tapis import Tapis
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from create_embeddings import initializeVectorIndex
# Use stderr so it doesn't interfere with the MCP protocol
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("Tapis-Systems-Server")

# Initialize Tapis (Use env vars for security)
t = Tapis(base_url="https://dev.develop.tapis.io", username="testuser2", password="")
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
def search_docs(query: str):
    """Searches Tapis documentation and conceptual guides using Neo4j RAG."""
    # Perform vector similarity search in the graph
    results = vector_db.similarity_search(query, k=3)
    
    # Return the page contents
    return [doc.page_content for doc in results]
    
if __name__ == "__main__":
    mcp.run(transport='stdio')