from mcp.server.fastmcp import FastMCP 
mcp = FastMCP("SharePointServer") 

@mcp.tool() 
def hello(): 
    return "Hello World" 
@mcp.tool() 
def listDocumentFromSharePoint(): 
    # We can call the actual python method here to get the data from the sharePoint 
    return 

print("Starting MCP Server...") 
if __name__ == "__main__": 
    mcp.run()


#npx @modelcontextprotocol/inspector
#python TestMCP.py
