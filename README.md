# tesla-prox

## Summary
  Function that checks how close GPS corrdinates are to an address.

## Setup For GCP
 - Set up GCP project, and IAM service accounts
 - Google Maps credentials


## Optional
- [Secret Manager](secret_manager.py): You can choose to store sensitive data in GCP Secret manager or store it locally. You can use secret_manager.py script to assist with this.
- [Cloud Build](cloudbuild.yaml): can use [cloudbuild.yaml](cloudbuild.yaml) to build out the Cloud Function.
