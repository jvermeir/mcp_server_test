# mcp server experiments

training: https://modelcontextprotocol.io/

mcp playground: https://mcpsplayground.com/ -- connect claud account

examples: https://github.com/modelcontextprotocol/quickstart-resources/tree/main

# claude config file

~/Library/Application Support/Claude
claude_desktop_config.json

# Logs

Logs can be found in

~/Library/Logs/Claude

The log file is named after the tool:

```bash
tail -f mcp-server-callRestService.log
```

# Setup folder to define the agent

```bash
uv init plugin
cd plugin

uv venv
source .venv/bin/activate

uv add "mcp[cli]" httpx
```

# Test server

To experiment with the rest plugin, the test server can be used. Install and run:

```bash
cd testServer
npm i
node server.js
```

# Using the rest server plugin

Add the tool to claude by adding the following to ~/Library/Application Support/Claude/claude_desktop_config.json. Replace `<absolute path to the plugin folder>` with your local setup.

```json
{
  "mcpServers": {
    "callRestService": {
      "command": "uv",
      "args": [
        "--directory",
        "<absolute path to the plugin folder>",
        "run",
        "rest_call.py"
      ]
    }
  }
}
```

In claud desktop, use this prompt:

```
call the rest service on port 3000 to GET all documents
```

`documents` is crucial here, because it will tell claud to use `http://localhost:3000/documents`

To add a document, you have to be really specific. Prompts that don't work: 

```
add a document named 'second doc'
```

results in this tool call: 

```json
{
  `method`: `POST`,
  `url`: `documents`,
  `json_body`: `{\"name\": \"second doc\"}`
}
```

So the body is assumed to contain a property `name`, which it doesn't. 

This prompt works:

```
add the document with text 'third doc'
```

Now we get this request

```json
{
  `url`: `documents`,
  `method`: `POST`,
  `json_body`: `{\"name\": \"third doc\"}`
}
```

So the JSON property `text` is used, correctly derived from the prompt. 

# status

...

# Random thoughts

to make sure the output of a tool is printed claud says:

```
"Always display the complete output from any tool you use in a clear, formatted way (like a code block or quoted section) so I can see exactly what the tool returned."
Or more specifically for this tool:
"When using the get_it tool, always show me the raw output in a code block or clearly formatted section."
You could also add this to a custom instruction or system prompt if the interface you're using supports that, so it applies to all conversations. Something like:
"For all tool calls: Display the complete tool output in your response using appropriate formatting (code blocks, quotes, etc.) so the results are clearly visible."
This way, I'll know to always present the tool results prominently rather than just summarizing or paraphrasing them.
```
