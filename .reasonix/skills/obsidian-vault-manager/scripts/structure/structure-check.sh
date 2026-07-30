#!/usr/bin/env bash
# structure-check.sh — 检查 vault 目录结构
# Usage: ./structure-check.sh /path/to/vault
# 输出格式参照 reports/report-format.md

set -euo pipefail

VAULT_PATH="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCHEMA_FILE="$SCRIPT_DIR/../../references/schema/vault-schema.yaml"
ERRORS=0
WARNINGS=0
DETAILS=""

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "[ERROR] Schema file not found: $SCHEMA_FILE"
    exit 1
fi

# --- Check 1: required directories ---
while IFS= read -r dir; do
    [ -z "$dir" ] && continue
    if [ ! -d "$VAULT_PATH/$dir" ]; then
        DETAILS+="[ERROR] 缺失目录: $dir/\n"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -A100 'required:' "$SCHEMA_FILE" | grep '^    - ' | sed 's/^    - //')

# --- Check 2: unmapped directories ---
ALLOWED=$(grep -A100 'directories:' "$SCHEMA_FILE" | grep '^    - ' | sed 's/^    - //')
IGNORED=$(grep -A100 'ignored:' "$SCHEMA_FILE" | grep '^    - ' | sed 's/^    - //')

for dir in "$VAULT_PATH"/*/; do
    [ -d "$dir" ] || continue
    dirname=$(basename "$dir")
    echo "$IGNORED" | grep -q "^$dirname$" && continue
    echo "$ALLOWED" | grep -q "^$dirname$" && continue
    DETAILS+="[WARNING] 非法目录: $dirname/\n"
    WARNINGS=$((WARNINGS + 1))
done

# --- Output report in standard format ---
echo "# Structure Audit Report"
echo "Date: $(date +%Y-%m-%d\ %H:%M)"
echo "Vault: $VAULT_PATH"
echo ""
echo "## Summary"
echo "- Errors: $ERRORS"
echo "- Warnings: $WARNINGS"
echo ""
echo "## Details"
echo -e "$DETAILS"
