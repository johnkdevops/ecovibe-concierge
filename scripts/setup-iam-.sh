#!/bin/bash

# Automatically retrieves the project number and binds the Datastore User role.
# Fallback to default if variable is not active in environment
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID="eco-vibe-project"
fi

echo "Active Project ID: $PROJECT_ID"

# Dynamically extract your GCP Project Number directly from the gcloud metadata API
# This avoids hardcoding the number and makes the script portable
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)" 2>/dev/null)

# Check if the project number was found
if [ -z "$PROJECT_NUMBER" ]; then
    echo "❌ Error: Could not retrieve project number. Ensure you are authenticated with 'gcloud auth login'."
    exit 1
fi

echo "Found Project Number: $PROJECT_NUMBER"
echo "Executing IAM policy binding for Compute Engine service account..."

# Bind the Datastore User role
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" --role="roles/datastore.user"

