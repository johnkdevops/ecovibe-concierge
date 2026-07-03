#!/bin/bash
# ------------------------------------------------------------------------------
# 🌱 ECOVIBE CONCIERGE - GOOGLE CLOUD SERVICE ACCOUNT PROVISIONING & IAM BINDINGS
# ------------------------------------------------------------------------------
# Fully optimized for local Git Bash on Windows & remote cloud deployment.
# ------------------------------------------------------------------------------

# Clear Windows carriage returns (\r) from variables
PROJECT_ID=$(echo "$PROJECT_ID" | tr -d '\r')

if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "undefined" ]; then
    PROJECT_ID="eco-vibe-project"
fi

echo "=== 🌱 ECOVIBE CUSTOM IAM SETUP ==="
echo "Active Project ID: $PROJECT_ID"

# Resolve project number safely
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)" 2>/dev/null | tr -d '\r')
if [ -z "$PROJECT_NUMBER" ]; then
    echo "❌ Error: Could not retrieve project number. Verify authentication with 'gcloud auth login'."
    exit 1
fi
echo "Found Project Number: $PROJECT_NUMBER"

# Define Service Account variables cleanly (Fixed malformed string interpolation)
SA_NAME="ecovibe-run-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Verifying custom service account '$SA_EMAIL'..."

# Check if service account exists (Windows Git Bash-safe command evaluation)
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" &>/dev/null; then
    echo "Creating custom service account '$SA_NAME'..."
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="EcoVibe Cloud Run Service Account" \
        --project="$PROJECT_ID"
    # Allow 5 seconds for Google's global IAM directory to propagate changes
    echo "Waiting for identity propagation..."
    sleep 5
else
    echo "✅ Service account '$SA_NAME' already exists."
fi

# Apply the least-privilege role bindings using cleansed strings
echo "Binding 'roles/datastore.user' (Cloud Firestore User) to $SA_EMAIL..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/datastore.user" \
    --no-user-output-enabled

echo "Binding 'roles/aiplatform.user' (Vertex AI User) to $SA_EMAIL..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user" \
    --no-user-output-enabled

echo ""
echo "✅ Custom IAM Service Account configuration complete!"
echo "Target Identity: $SA_EMAIL"
echo "Permissions Bound: Firestore & Vertex AI"
echo ""