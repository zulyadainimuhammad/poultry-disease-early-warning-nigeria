# Publish the Poultry Disease Intelligence dashboard and create a QR code

## What public access requires

The current `http://localhost:8501` address is only reachable from the computer running Streamlit. A QR code containing that address will not let other people open the dashboard from their phones. The app must first be deployed to a public HTTPS address.

This project is prepared for **Streamlit Community Cloud**, which Streamlit currently documents as a free way to deploy apps from GitHub and share a public `streamlit.app` URL. The repository must be accessible to the deployment account, and the account needs admin permission on the selected repository. Read the current official instructions before deployment:

- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

## Repository preparation

1. Keep the application in `app/dashboard.py`.
2. Keep `.streamlit/config.toml` at the repository root.
3. Keep `app/requirements.txt` next to `app/dashboard.py`. Community Cloud checks the entrypoint directory for a requirements file before the repository root. This app-specific file intentionally avoids installing the full Jupyter/research environment in the hosted app.
4. Ensure these tracked files exist in the GitHub branch selected for deployment:
   - `app/dashboard.py`
   - `app/requirements.txt`
   - `.streamlit/config.toml`
   - `src/data/cleaning.py`
   - `src/data/panel.py`
   - `src/data/eda.py`
   - `data/raw/Quantitative data 2026-10-01.csv`
   - `artifacts/evaluation/rolling_origin_oos_predictions.csv`
5. Do not upload private information, passwords, API keys or local `.env` files. The current dashboard does not require secrets for data access.

## Deploy on Streamlit Community Cloud

1. Push the tested dashboard branch to GitHub and open/merge a pull request when the local tests pass.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Authorise Streamlit to access the repository.
4. Choose **Create app** → **Yup, I have an app**.
5. Select repository `zulyadainimuhammad/poultry-disease-early-warning-nigeria`.
6. Select the branch containing the dashboard files.
7. Set the main file path to `app/dashboard.py`.
8. In Advanced settings, select Python 3.11 to match the local environment used for development.
9. Choose a short custom subdomain if available, such as `poultry-disease-intelligence-nigeria`.
10. Deploy and wait for the app health check to complete.
11. Open the generated HTTPS `*.streamlit.app` URL in an incognito/private browser and on a mobile phone to verify public access.

A public app deployed from a public GitHub repository is publicly viewable. Confirm that the source data can be publicly redistributed and that no confidential material is in the repository before making the app public.

## Configure the built-in QR display

After the app is deployed:

1. Copy its full public HTTPS URL from Streamlit Community Cloud.
2. Open the deployed app's **Settings** → **Secrets** panel.
3. Add this TOML entry, replacing the value with the actual URL:

```toml
APP_PUBLIC_URL = "https://your-custom-name.streamlit.app"
```

4. Save the secret and allow the app to restart.
5. Open the app's **Share / QR** tab. It should display a QR code and a download button.
6. Scan the QR code with a phone that is not connected to the same computer. Confirm it opens the public dashboard.

`APP_PUBLIC_URL` is just a public web address, not a password or private credential. Do not place API keys or passwords in this field.

## Create a separate printable QR image (optional)

Once the QR dependency is installed locally, run from the repository root:

```powershell
python scripts/generate_dashboard_qr.py https://your-custom-name.streamlit.app
```

The PNG is saved to `artifacts/dashboard_qr.png`. Test the printed or projected image from a normal audience distance before the presentation.

## Public-hosting limits and operating practice

- Community Cloud is a free community hosting option, not a service-level-guaranteed production platform. Capacity, sleeping/idle behaviour, and usage limits can change; consult the current Community Cloud documentation and status pages before relying on it for a live event.
- The public app uses the repository snapshot at the chosen branch. Pushing new commits can update the deployed app. Test changes locally and through the deployment logs before presenting.
- The app is an exploratory research prototype. It does not connect to live surveillance feeds, provide veterinary diagnosis, or issue operational alerts.
- A public QR link makes the dashboard accessible to anyone who has it (and potentially searchable if the app is public/searchable). Do not use it to expose sensitive farmer, farm, personal or restricted surveillance data.
