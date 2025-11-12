# APQR System Flowcharts (Mermaid 8.8.0 Compatible)

This file contains Mermaid.js diagrams compatible with older versions.

**Recommended: Use Mermaid Live Editor**
1. Visit: https://mermaid.live/
2. Copy any diagram code below
3. Paste into editor (renders automatically)
4. Export as PNG/SVG

**OR Update VS Code Extension:**
- Install "Markdown Preview Mermaid Support" (latest version)
- Restart VS Code

---

## 1. High-Level System Architecture

```mermaid
graph TB
    User[User Query Input] --> Orchestrator[Orchestrator Agent]
    
    Orchestrator --> LIMS[LIMS Domain Agent]
    Orchestrator --> ERP[ERP Domain Agent]
    Orchestrator --> DMS[DMS Domain Agent]
    
    LIMS --> QC[QC Sub-Agent]
    LIMS --> Validation[Validation Sub-Agent]
    LIMS --> RnD[R&D Sub-Agent]
    
    ERP --> Manufacturing[Manufacturing Sub-Agent]
    ERP --> Engineering[Engineering Sub-Agent]
    ERP --> SupplyChain[Supply Chain Sub-Agent]
    
    DMS --> QA[QA Sub-Agent]
    DMS --> Regulatory[Regulatory Sub-Agent]
    DMS --> Training[Training Sub-Agent]
    DMS --> Management[Management Sub-Agent]
    
    QC --> Compiler[Compiler Agent]
    Validation --> Compiler
    RnD --> Compiler
    Manufacturing --> Compiler
    Engineering --> Compiler
    SupplyChain --> Compiler
    QA --> Compiler
    Regulatory --> Compiler
    Training --> Compiler
    Management --> Compiler
    
    Compiler --> FinalReport[Final Report to User]
    
    style User fill:#e1f5ff
    style Orchestrator fill:#fff4e1
    style LIMS fill:#e8f5e9
    style ERP fill:#f3e5f5
    style DMS fill:#fce4ec
    style Compiler fill:#fff9c4
    style FinalReport fill:#e1f5ff
```

---

## 2. Sequential Workflow (Current System)

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant LIMS
    participant Compiler
    participant ERP
    participant DMS
    
    User->>Orchestrator: Complete documentation query
    Note over Orchestrator: Analyzes query
    
    Orchestrator->>LIMS: Route to LIMS
    LIMS->>LIMS: QC searches data
    LIMS->>Compiler: Forward data
    
    Compiler->>Compiler: LIMS done, ERP pending
    Compiler->>Orchestrator: Route to ERP next
    
    Orchestrator->>ERP: Route to ERP
    ERP->>ERP: Supply Chain searches
    ERP->>Compiler: Forward data
    
    Compiler->>Compiler: LIMS+ERP done, DMS pending
    Compiler->>Orchestrator: Route to DMS next
    
    Orchestrator->>DMS: Route to DMS
    DMS->>DMS: QA searches
    DMS->>Compiler: Forward data
    
    Compiler->>Compiler: All domains complete
    Compiler->>User: Final Report
    
    Note over User,DMS: Total Time: 2-3 minutes
```

---

## 3. Async Workflow (Future)

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant LIMS
    participant ERP
    participant DMS
    participant Compiler
    
    User->>Orchestrator: Complete documentation query
    Note over Orchestrator: Routes to ALL domains in parallel
    
    par Parallel Execution
        Orchestrator->>LIMS: Query LIMS
        Orchestrator->>ERP: Query ERP
        Orchestrator->>DMS: Query DMS
    end
    
    LIMS->>Compiler: Forward LIMS data
    ERP->>Compiler: Forward ERP data
    DMS->>Compiler: Forward DMS data
    
    Compiler->>Compiler: All received, compile
    Compiler->>User: Final Report
    
    Note over User,Compiler: Total Time: 40-50 seconds
```

---

## 4. Model Selection Architecture

```mermaid
graph LR
    subgraph Pro Agents
        Orch[Orchestrator PRO]
        LIMSD[LIMS Domain PRO]
        ERPD[ERP Domain PRO]
        DMSD[DMS Domain PRO]
        Comp[Compiler PRO]
    end
    
    subgraph Flash Agents
        QC[QC FLASH]
        Val[Validation FLASH]
        Mfg[Manufacturing FLASH]
        SC[Supply Chain FLASH]
        QA[QA FLASH]
    end
    
    Orch --> LIMSD
    Orch --> ERPD
    Orch --> DMSD
    
    LIMSD --> QC
    LIMSD --> Val
    ERPD --> Mfg
    ERPD --> SC
    DMSD --> QA
    
    QC --> Comp
    Val --> Comp
    Mfg --> Comp
    SC --> Comp
    QA --> Comp
    
    style Orch fill:#ffcccc
    style LIMSD fill:#ffcccc
    style ERPD fill:#ffcccc
    style DMSD fill:#ffcccc
    style Comp fill:#ffcccc
    
    style QC fill:#ccffcc
    style Val fill:#ccffcc
    style Mfg fill:#ccffcc
    style SC fill:#ccffcc
    style QA fill:#ccffcc
```

---

## 5. Simple Data Flow

```mermaid
graph TD
    Start[User Query: Complete documentation]
    
    Start --> Analyze{Orchestrator Analyzes}
    Analyze -->|Need 3 domains| Route1[Route to LIMS]
    
    Route1 --> LIMS[LIMS QC searches COA]
    LIMS --> Comp1[Compiler: LIMS done]
    
    Comp1 --> Route2[Route to ERP]
    Route2 --> ERP[ERP Supply Chain searches]
    ERP --> Comp2[Compiler: ERP done]
    
    Comp2 --> Route3[Route to DMS]
    Route3 --> DMS[DMS QA searches]
    DMS --> Comp3[Compiler: DMS done]
    
    Comp3 --> Final[Generate Final Report]
    Final --> User[Return to User]
    
    style Start fill:#e1f5ff
    style Analyze fill:#fff4e1
    style Comp3 fill:#c8e6c9
    style User fill:#e1f5ff
```

---

## 6. Agent Hierarchy (Simplified)

```mermaid
graph TD
    Root[Root Agent]
    Root --> Orch[Orchestrator]
    
    Orch --> LIMS[LIMS Domain]
    Orch --> ERP[ERP Domain]
    Orch --> DMS[DMS Domain]
    
    LIMS --> LIMS1[QC Sub-Agent]
    LIMS --> LIMS2[Validation Sub-Agent]
    LIMS --> LIMS3[R&D Sub-Agent]
    
    ERP --> ERP1[Manufacturing Sub-Agent]
    ERP --> ERP2[Engineering Sub-Agent]
    ERP --> ERP3[Supply Chain Sub-Agent]
    
    DMS --> DMS1[QA Sub-Agent]
    DMS --> DMS2[Regulatory Sub-Agent]
    DMS --> DMS3[Training Sub-Agent]
    
    LIMS1 --> Comp[Compiler]
    LIMS2 --> Comp
    LIMS3 --> Comp
    ERP1 --> Comp
    ERP2 --> Comp
    ERP3 --> Comp
    DMS1 --> Comp
    DMS2 --> Comp
    DMS3 --> Comp
    
    Comp --> User[User Response]
    
    style Root fill:#e3f2fd
    style Orch fill:#fff9c4
    style LIMS fill:#e8f5e9
    style ERP fill:#f3e5f5
    style DMS fill:#fce4ec
    style Comp fill:#ffecb3
    style User fill:#e1f5ff
```

---

## 7. APQR Generation Flow

```mermaid
graph TD
    User[User: Generate APQR]
    User --> Orch[Orchestrator]
    Orch --> APQR[APQR Filler Agent]
    
    APQR --> Query[Query all domains]
    Query --> L[Query LIMS]
    Query --> E[Query ERP]
    Query --> D[Query DMS]
    
    L --> Collect[Collect Data]
    E --> Collect
    D --> Collect
    
    Collect --> Index[Load document index]
    Index --> Pop[Populate 24 sections]
    
    Pop --> Gen[Generate Documents]
    Gen --> Word[Word Document]
    Gen --> HTML[HTML Document]
    
    Word --> Link[Return link to user]
    HTML --> Link
    
    style User fill:#e1f5ff
    style APQR fill:#fff4e1
    style Gen fill:#c8e6c9
    style Link fill:#e1f5ff
```

---

## 8. Cost Comparison

```mermaid
graph LR
    subgraph Current All Pro
        A1[Orchestrator PRO $$$]
        B1[Domain PRO $$$]
        C1[Sub-Agent PRO $$$]
        D1[Compiler PRO $$$]
        
        A1 --> B1
        B1 --> C1
        C1 --> D1
        D1 --> Cost1[Total: $0.15 per query]
    end
    
    subgraph Optimized
        A2[Orchestrator PRO $$$]
        B2[Domain PRO $$$]
        C2[Sub-Agent FLASH $]
        D2[Compiler PRO $$$]
        
        A2 --> B2
        B2 --> C2
        C2 --> D2
        D2 --> Cost2[Total: $0.087 per query]
    end
    
    style Cost1 fill:#ffcccc
    style Cost2 fill:#ccffcc
    style C2 fill:#c8e6c9
```

---

## How to View These Diagrams

### Option 1: Mermaid Live Editor (EASIEST)
1. Go to https://mermaid.live/
2. Copy any diagram code above (between ```mermaid and ```)
3. Paste into the editor
4. Diagram renders automatically
5. Click "Export PNG" or "Export SVG"

### Option 2: VS Code Extension
1. Open Extensions (Cmd+Shift+X or Ctrl+Shift+X)
2. Search "Markdown Preview Mermaid Support"
3. Install the extension by Matt Bierner
4. Restart VS Code
5. Open this file and click Preview button

### Option 3: GitHub
1. Push this file to GitHub
2. View the .md file on GitHub
3. Diagrams render automatically

---

## Troubleshooting

**If diagrams still don't render:**
- Your Mermaid version is too old
- Use Mermaid Live Editor (no installation needed)
- Or update your markdown viewer extension

**Syntax Errors:**
- Make sure to copy the ENTIRE code block including ```mermaid and closing ```
- Don't add extra spaces or lines

---

*Last Updated: November 12, 2025*
*Compatible with Mermaid 8.8.0+*

