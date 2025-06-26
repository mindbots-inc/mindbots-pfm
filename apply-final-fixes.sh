#!/bin/bash
set -e

echo "🔧 Applying final fixes to all workflows..."

# Define repositories and their workflow types
declare -A REPO_WORKFLOWS=(
  ["repos/mindbots-core"]="full"
  ["repos/mindbots-services"]="full"
  ["repos/mindbots-local-scripts"]="full"
  ["repos/mindbots-agents"]="full"
  ["repos/core-agent-generator"]="full"
  ["repos/mindbots-pfm"]="minimal"
  ["repos/flow"]="full"
  ["repos/mindbots-infra"]="minimal"
)

for repo in "${!REPO_WORKFLOWS[@]}"; do
  workflow_type="${REPO_WORKFLOWS[$repo]}"
  echo "=== Processing $repo with $workflow_type workflow ==="
  
  cd /workspace/$repo
  
  # Copy the updated template with the epic validation fix
  case $workflow_type in
    "full")
      cp /workspace/.github/workflow-templates/enforce-branch-flow-full.yml .github/workflows/enforce-branch-flow.yml
      ;;
    "simplified")
      cp /workspace/.github/workflow-templates/enforce-branch-flow-simplified.yml .github/workflows/enforce-branch-flow.yml
      ;;
    "minimal")
      cp /workspace/.github/workflow-templates/enforce-branch-flow-minimal.yml .github/workflows/enforce-branch-flow.yml
      ;;
  esac
  
  # Add and track changes
  git add .github/workflows/enforce-branch-flow.yml
  
  echo "✅ Updated $repo"
done

echo "✅ All workflows updated!"
