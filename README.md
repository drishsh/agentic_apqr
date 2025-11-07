# APQR Agentic System

**Advanced Pharmaceutical Quality & Records Management System**

A multi-agent system skeleton designed for pharmaceutical quality assurance and records management. The system uses an orchestrator-compiler architecture to route queries to specialized agents and synthesize their responses into coherent answers.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER QUERY                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                          │
│  • Accepts user query payload (JSON)                         │
│  • Routes to appropriate agents based on keywords            │
│  • Forwards original query to each routed agent              │
│  • Collects and aggregates responses                         │
└────────────┬────────────────┬────────────────┬──────────────┘
             │                │                │
             ▼                ▼                ▼
      ┌──────────┐     ┌──────────┐    ┌──────────┐
      │   LIMS   │     │   ERP    │    │   DMS    │
      │  AGENT   │     │  AGENT   │    │  AGENT   │
      └────┬─────┘     └────┬─────┘    └────┬─────┘
           │                │                │
           └────────────────┴────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMPILER AGENT                             │
│  • Receives original query + agent responses                 │
│  • Deduplicates information                                  │
│  • Prioritizes by relevance                                  │
│  • Detects contradictions                                    │
│  • Generates friendly summary with citations                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               COMPILED RESPONSE TO USER                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
apqr-system/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── __init__.py                       # Package initialization
│
├── agents/                           # Agent implementations
│   ├── __init__.py
│   ├── orchestrator_agent.py        # Main orchestrator with routing logic
│   ├── compiler_agent.py            # Response synthesis and compilation
│   ├── lims_agent.py                # Laboratory Information Management System
│   ├── erp_agent.py                 # Enterprise Resource Planning
│   └── dms_agent.py                 # Document Management System
│
├── configs/                          # Configuration files
│   ├── __init__.py
│   └── agents_config.yaml           # Agent endpoints, tools, permissions
│
└── tests/                            # Test suite
    ├── __init__.py
    ├── test_orchestrator_routing.py # Orchestrator routing tests
    └── test_compiler_integration.py # Compiler synthesis tests
```

## 🎯 Key Features

### Orchestrator Agent
- **Keyword-based routing** to LIMS, ERP, DMS agents
- **Multi-agent dispatch** for complex queries
- **Original query forwarding** to all routed agents
- **Response aggregation** for compiler

**Routing Keywords:**
- **LIMS**: assay, test, lab, quality control, OOS, CoA, dissolution, HPLC
- **ERP**: GRN, batch, manufacturing, BMR/BPR, training, CAPA, procurement
- **DMS**: SOP, protocol, document, validation, procedure, cleaning

### Compiler Agent
- **Deduplication**: Removes redundant information
- **Prioritization**: Ranks results by relevance
- **Contradiction Detection**: Identifies conflicting data
- **Summary Generation**: Creates concise, user-friendly responses
- **Citation Tracking**: Shows which agents provided information

### Main Agents (Stubs)
All three main agents (LIMS, ERP, DMS) are implemented as stubs with:
- ✅ Query processing interface
- ✅ JSON response format
- ✅ Mock data for testing
- ✅ HTTP/gRPC endpoint wrappers (ready for implementation)
- ⚠️ TODO markers for actual tool integration

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher required
python --version

# Install dependencies
pip install -r requirements.txt
```

### Installation

```bash
# Clone or navigate to the project directory
cd apqr-system

# Install in development mode (optional)
pip install -e .
```

## 🧪 Running Tests

### Run All Tests

```bash
# From the apqr-system directory
python -m pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Test orchestrator routing only
python tests/test_orchestrator_routing.py

# Test compiler integration only
python tests/test_compiler_integration.py
```

### Run with Coverage

```bash
python -m pytest tests/ --cov=agents --cov-report=html
```

## 💡 Usage Examples

### Example 1: Basic Orchestrator Usage

```python
from agents.orchestrator_agent import create_orchestrator, QueryPayload

# Create orchestrator
orchestrator = create_orchestrator()

# Create query payload
payload = QueryPayload(
    query="What are the assay results for batch LOT-12345?",
    session_id="user-session-123"
)

# Process query
result = orchestrator.process_query(payload)

print(f"Routed to: {result['routed_agents']}")
print(f"Ready for compiler: {result['ready_for_compiler']}")
```

### Example 2: Compiler Usage

```python
from agents.compiler_agent import create_compiler

# Create compiler
compiler = create_compiler()

# Mock agent responses
responses = [
    {
        "agent": "LIMS",
        "results": [
            {
                "lot_number": "LOT-12345",
                "test": "Assay",
                "result": "98.5%",
                "status": "PASS"
            }
        ]
    }
]

# Compile responses
result = compiler.compile(
    query="What are the assay results?",
    responses=responses
)

print(f"Summary: {result.summary}")
print(f"Citations: {result.citations}")
```

### Example 3: Individual Agent Usage

```python
from agents.lims_agent import create_lims_agent

# Create LIMS agent
lims = create_lims_agent()

# Process query
result = lims.process_query("Show me test results for LOT-12345")

print(f"Agent: {result['agent']}")
print(f"Results: {result['results']}")
```

## 🧩 End-to-End Demo

Run a complete example demonstrating the full flow:

```python
from agents.orchestrator_agent import create_orchestrator, QueryPayload
from agents.compiler_agent import create_compiler

# Initialize components
orchestrator = create_orchestrator()
compiler = create_compiler()

# Step 1: User query
query = "Find assay results and related SOP documents for batch testing"
payload = QueryPayload(query=query, session_id="demo-session")

# Step 2: Orchestrator routes and collects responses
orchestrator_output = orchestrator.process_query(payload)

print(f"✓ Query routed to: {orchestrator_output['routed_agents']}")

# Step 3: Extract responses for compiler
agent_responses = []
for agent_name, response_data in orchestrator_output['agent_responses']['responses_by_agent'].items():
    agent_responses.append({
        "agent": agent_name,
        "results": response_data['results']
    })

# Step 4: Compiler synthesizes results
compilation = compiler.compile(query, agent_responses)

print(f"\n✓ Compilation complete")
print(f"  Summary: {compilation.summary}")
print(f"  Citations: {compilation.citations}")
print(f"  Details: {len(compilation.details)} items")
```

## 🔧 Configuration

Edit `configs/agents_config.yaml` to customize:

- Agent endpoints (local, HTTP, gRPC)
- Routing keywords for each agent
- Tool permissions
- Database connection strings
- Logging levels
- Performance settings

Example configuration snippet:

```yaml
agents:
  lims:
    enabled: true
    endpoint:
      type: "local"  # Change to "http" or "grpc" in production
      url: "http://localhost:8001/lims"
    routing_keywords:
      - "assay"
      - "test"
      - "lab"
```

## 📝 Test Coverage

### Orchestrator Tests (27 tests)
- ✅ Keyword-based routing to LIMS (assay, test, OOS, CoA)
- ✅ Keyword-based routing to ERP (GRN, batch, training, CAPA)
- ✅ Keyword-based routing to DMS (SOP, protocol, document)
- ✅ Multi-agent routing for complex queries
- ✅ Generic query handling (routes to all agents)
- ✅ Original query forwarding to compiler
- ✅ Case-insensitive routing
- ✅ Integration with compiler

### Compiler Tests (18 tests)
- ✅ Single agent compilation
- ✅ Multi-agent response synthesis
- ✅ Deduplication of responses
- ✅ Relevance-based prioritization
- ✅ Summary generation with citations
- ✅ Contradiction detection
- ✅ Empty response handling
- ✅ Configuration options (max length, detection toggles)
- ✅ End-to-end compilation flow

**Total: 45+ Unit Tests**

## 🔨 Next Steps for Implementation

### 1. Connect to Real Data Sources

Replace stub implementations with actual database connections:

```python
# In lims_agent.py
def _mock_query_processing(self, query: str):
    # TODO: Replace with actual LIMS database query
    # Example: return self.db_connection.execute(sql_query)
    pass
```

### 2. Implement Tools

Add document processing and search tools:

```python
# Example tools to implement:
- PDF parsing (pdf_tools)
- Excel parsing (xlsx_tools)
- Document search (search_tools)
- OCR processing (ocr_tools)
```

### 3. Deploy HTTP/gRPC Endpoints

```python
from flask import Flask, request, jsonify
from agents.lims_agent import create_lims_agent

app = Flask(__name__)
lims = create_lims_agent()

@app.route('/lims/query', methods=['POST'])
def lims_query():
    data = request.json
    result = lims.process_query(data['query'], data.get('context'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8001)
```

### 4. Add Authentication & Security

- Implement API key authentication
- Add rate limiting
- Enable audit logging
- Set up SSL/TLS for production

### 5. Enhance with ML/NLP

- Replace keyword routing with ML-based classification
- Use semantic similarity for better deduplication
- Implement advanced contradiction detection
- Add query intent recognition

## 🐛 Troubleshooting

### Import Errors

```bash
# If you get import errors, make sure you're in the right directory
cd apqr-system
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### YAML Loading Issues

```bash
# Install PyYAML if missing
pip install pyyaml>=6.0.1
```

### Test Failures

```bash
# Run tests with verbose output to see details
python -m pytest tests/ -vv
```

## 📚 References

This system follows patterns from:
- `edugent` folder: Multi-agent architecture, agent templates
- `APQR_ADK_System`: Orchestrator design, configuration patterns
- `x.cloned`: Agent initialization, tool integration patterns

## 🤝 Contributing

### Adding a New Agent

1. Create `agents/new_agent.py` following the template pattern
2. Add routing keywords to `configs/agents_config.yaml`
3. Register in orchestrator's `_initialize_agent_registry()`
4. Create tests in `tests/test_new_agent.py`
5. Update `agents/__init__.py` exports

### Adding a New Tool

1. Create tool function in appropriate agent file
2. Document parameters and return format
3. Add to agent's tools list in config
4. Write unit tests for the tool

## 📄 License

[Add your license information here]

## 👥 Authors

APQR Team

---

**Version:** 1.0.0  
**Status:** Development/Skeleton  
**Last Updated:** November 2025

For questions or issues, please refer to the TODO markers in the code or consult the configuration documentation.

