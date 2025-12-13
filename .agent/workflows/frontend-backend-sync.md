---
description: Workflow for parallel frontend/backend development with shared API contracts
---

# Frontend-Backend Sync Workflow

## The Problem

When frontend and backend develop simultaneously, they can create files out of sync (e.g., frontend expects `player_id` but backend sends `playerId`).

## The Solution: Contract-First Development

### Step 1: Backend Creates Pydantic Schemas First

```bash
# Backend developer creates schema
# backend/app/schemas/scouting.py
```

### Step 2: Export OpenAPI Spec

```bash
cd backend
# turbo
python -c "from app.main import app; import json; print(json.dumps(app.openapi()))" > ../contracts/openapi.json
```

### Step 3: Generate Frontend Types

```bash
cd frontend
# turbo
npx openapi-typescript ../contracts/openapi.json -o src/types/api/generated.ts
```

### Step 4: Frontend Uses Generated Types

```typescript
// This type is auto-generated - NEVER edit manually
import { ScoutingReport } from "@/types/api/generated";
```

## Rules

1. **Backend owns schemas** - Frontend never creates API types manually
2. **Run type generation after ANY schema change**
3. **Never commit `generated.ts` edits** - Always regenerate
4. **Use MSW for mocking** while backend implements

## Commands Reference

| Action         | Command                      | Who Runs       |
| -------------- | ---------------------------- | -------------- |
| Export OpenAPI | `python -c "..."`            | Backend        |
| Generate types | `npx openapi-typescript ...` | Frontend or CI |
| Mock API       | `npx msw init public/`       | Frontend       |
