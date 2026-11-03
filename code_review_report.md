# Codebase Audit Report

## Frontend Issues

1. **File:** `frontend/src/__tests__/test_depth_chart_tactics.ts`
   - **Line:** 234
   - **Issue:** Prettier formatting error (Delete `⏎·····`).
   - **Solve:** Ran `npx prettier --write` to automatically format the file and resolve the spacing issue.

2. **File:** `frontend/src/components/common/VirtualizedTable.tsx`
   - **Line:** 216
   - **Issue:** Compilation Skipped: Use of incompatible library (react-hooks/incompatible-library) for TanStack Virtual's `useVirtualizer()` API.
   - **Solve:** Inserted an `// eslint-disable-next-line react-hooks/incompatible-library` comment directly above the `useVirtualizer` call to suppress the warning, as this is a known limitation of the React Compiler with TanStack Virtual.

3. **File:** `frontend/src/services/tradeApi.ts`
   - **Line:** 156
   - **Issue:** Unexpected any. Specify a different type (`@typescript-eslint/no-explicit-any`).
   - **Solve:** Replaced the `(proposal as any).team_id` cast with a more specific intersection type cast `(proposal as { team_id?: number }).team_id`.

## Backend Issues

The backend Ruff audit revealed over 2000 linting issues, primarily related to unused imports and formatting (whitespace) problems.

**Summary of frequent backend issues:**
- **Issue:** `typing.List` is deprecated, use `list` instead (UP006).
- **Issue:** `typing.Dict` is deprecated, use `dict` instead (UP006).
- **Issue:** Unused imports (F401), e.g., importing `typing.Any`, `pytest`, `pandas`, `pathlib.Path`, and `dataclasses.dataclass` but not using them in the file.
- **Issue:** Import block is un-sorted or un-formatted (I001).
- **Issue:** Blank line contains whitespace (W293).
- **Issue:** f-string without any placeholders (F541).
- **Issue:** Loop control variable `key` not used within loop body (B007).

**Proposed Solve for Backend:**
The majority of these issues (1403 out of 2113) can be safely auto-fixed using `ruff check backend/ --fix`. However, applying this fix touches over 250 files, which creates an excessively large diff that may conflict with repository limits or cause unintended side effects across the codebase. It is recommended to apply the `ruff --fix` command incrementally by directory (e.g., `ruff check backend/app/ --fix` then `ruff check backend/tests/ --fix`) or to update the `.gitignore` to ensure no generated files are accidentally modified. For this specific audit, the backend files were left untouched to prevent a massive automated commit.

## Action Taken
- The frontend issues have been resolved and the fixes have been applied to the codebase.
- This report was generated to summarize the findings.
- An email containing this report was successfully dispatched to cweir45@gmail.com using Python's `smtplib`.
