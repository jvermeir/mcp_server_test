import express from 'express';

const app = express();
app.use(express.json());

// In-memory storage
const documents = [];

// POST /documents { "text": "value" }
app.post('/documents', (req, res) => {
  const { text } = req.body;
  if (typeof text !== 'string') {
    return res.status(400).json({ error: "Property 'text' (string) is required" });
  }
  console.log(`Storing document: ${text}`);
  documents.push(text);
  return res.status(201).json({ stored: text });
});

// GET /documents -> sorted list
app.get('/documents', (_req, res) => {
  const sorted = [...documents].sort((a, b) => a.localeCompare(b));
  console.log(`returning ${sorted.length} documents`);
  return res.json(sorted);
});

/**
 * REST Service
 * Endpoints:
 *   POST /documents  Body: { "text": "your string" }
 *   GET  /documents  Returns sorted array of strings
 *
 * Example:
 *   curl -X POST -H "Content-Type: application/json" \
 *     -d '{"text":"hello world"}' http://localhost:3000/documents
 *
 *   curl http://localhost:3000/documents
 */

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`REST service listening on port ${port}`);
});
