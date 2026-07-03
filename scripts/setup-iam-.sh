#!/bin/bash

### Initializing script parameters and project validation...
# Automatically retrieves the project number and binds the Datastore User role.
# Fallback to default if variable is not active in environment
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID="eco-vibe-project"
fi

echo "=== 🌱 ECOVIBE CUSTOM IAM SETUP ==="
echo "Active Project ID: $PROJECT_ID"

### Resolving project metadata...
# Dynamically extract your GCP Project Number directly from the gcloud metadata API
# This avoids hardcoding the number and makes the script portable
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)" 2>/dev/null)

# Check if the project number was found
if [ -z "$PROJECT_NUMBER" ]; then
    echo "❌ Error: Could not retrieve project number. Ensure you are authenticated with 'gcloud auth login'."
    exit 1
fi

echo "Found Project Number: $PROJECT_NUMBER"

SA_NAME="ecovibe-run-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

### Checking and creating custom service account...

echo "Verifying custom service account '$SA_EMAIL' exists..."

if gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" >/dev/null 2>&1; then
    echo "Creating custom service account '$SA_NAME'..."
    gcloud iam service-accounts create "$SA_NAME" --display-name="EcoVibe Cloud Run Service Account" --project="$PROJECT_ID"
else
    echo "✅ Service account '$SA_NAME' already exists."
fi

### Binding Datastore User role for Firebase connection...
echo "Binding 'roles/datastore.user' (Cloud Firestore User) to $SA_EMAIL..."

# Bind the Datastore User role
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/datastore.user" --no-user-output-enabled

### Binding AI Platform User role for keyless Vertex/Gemini access...
echo "Binding 'roles/aiplatform.user' (Vertex AI User) to $SA_EMAIL..."
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/aiplatform.user" --no-user-output-enabled
echo ""
echo "✅ Custom IAM Service Account configuration complete!"
echo "Target Identity: $SA_EMAIL"
echo "Permissions Bound: Firestore & Vertex AI"
