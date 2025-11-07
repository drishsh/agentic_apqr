# ERP Folder Structure

## Overview
This folder has been reorganized to merge BMR_BPR and PROC data under unified batch folders, segregated by ERP sub-agent responsibility.

## Structure

```
ERP/
├── Batch_1_Jan_Feb/
│   ├── Manufacturing/          # Manufacturing Sub-Agent
│   │   ├── 05. Dispensing Logs
│   │   ├── 06. Sifting, Dry Blending & Lubrication
│   │   ├── 07. Compression
│   │   ├── 10. Pre Dispensing
│   │   └── 11. Packaging
│   ├── SupplyChain/           # SupplyChain Sub-Agent
│   │   ├── 01. Aspirin_Procurement_Details
│   │   └── 08. Packaging_Materials_Procurement
│   └── Engineering/           # Engineering Sub-Agent
│       └── 09. Sampling And Quarantine
│
├── Batch_2_Feb_Mar/
│   ├── Manufacturing/
│   │   ├── 05. Dispensing_Logs
│   │   ├── 06. Sifting, Dry Blending & Lubrication
│   │   ├── 07. Compression
│   │   ├── 10. Pre Dispensing
│   │   └── 11. Packaging
│   └── SupplyChain/
│       ├── 01. Aspirin_Procurement_Details
│       └── 08. Packaging_Materials_Procurement
│
├── Batch_3_Mar_Apr/
│   ├── Manufacturing/
│   │   ├── 05. Dispensing_Logs
│   │   ├── 06. Sifting, Dry Blending & Lubrication
│   │   ├── 07. Compression
│   │   ├── 10. Pre Dispensing
│   │   └── 11. Packaging
│   └── SupplyChain/
│       ├── 01. Aspirin_Procurement_Details
│       └── 08. Packaging_Materials_Procurement
│
└── Batch_4_Apr_May/
    ├── Manufacturing/
    │   ├── 05. Dispensing_Logs
    │   ├── 06. Sifting, Dry Blending & Lubrication
    │   ├── 07. Compression
    │   ├── 10. Pre Dispensing
    │   └── 11. Packaging
    └── SupplyChain/
        ├── 01. Aspirin_Procurement_Details
        └── 08. Packaging_Materials_Procurement
```

## Sub-Agent Responsibilities

### Manufacturing Sub-Agent
- **05. Dispensing Logs**: BMR dispensing records, material reconciliation, balance verification logs, cleaning logs
- **06. Sifting, Dry Blending & Lubrication**: Blending operation records
- **07. Compression**: Tablet compression process documentation
- **10. Pre Dispensing**: Pre-dispensing verification and preparation records
- **11. Packaging**: Packaging operation documentation

### SupplyChain Sub-Agent
- **01. Aspirin_Procurement_Details**: Raw material procurement (API, Binder, Disintegrant, Filler, Lubricant), COAs, SDSs, shipment details, vendor master, material master
- **08. Packaging_Materials_Procurement**: Packaging materials procurement, labels, cartons, bottles

### Engineering Sub-Agent
- **09. Sampling And Quarantine**: Sampling protocols and quarantine records (where available)

## Changes Made
1. ✅ Merged BMR_BPR and PROC folders into unified batch structure
2. ✅ Organized by batch number/month (4 batches)
3. ✅ Segregated by ERP sub-agent responsibility
4. ✅ Removed duplicate APQR Documents folders
5. ✅ Removed training records (belong in DMS domain)
6. ✅ Centralized procurement data in proper subfolders

## Batch Timeline
- **Batch 1**: January - February (ASP-25-001)
- **Batch 2**: February - March (ASP-25-002)
- **Batch 3**: March - April (ASP-25-003)
- **Batch 4**: April - May (ASP-25-004)

