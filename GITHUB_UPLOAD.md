# Upload EduPulse to GitHub (Windows)

1. Extract this ZIP and open the extracted `EduPulse_Training_Project` folder in VS Code.
2. Install Git for Windows if needed: https://git-scm.com/download/win
3. Create an empty repository on https://github.com/new. Do not initialize it with a README, license, or `.gitignore` because those files are already in this project.
4. Open VS Code Terminal in the project root and run:

```powershell
git init
git add .
git status
```

5. Review `git status` before committing. Do not commit passwords, API keys, personal information, or private datasets you do not have permission to publish. The `.gitignore` excludes common local secrets and environments.
6. Commit and push (replace the URL with your repository's HTTPS URL):

```powershell
git commit -m "Initial commit - EduPulse project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/EduPulse_Training_Project.git
git push -u origin main
```

If Git says `Author identity unknown`, configure your Git name and email using the values you want attached to commits:

```powershell
git config --global user.name "Your Name"
git config --global user.email "YOUR-GITHUB-EMAIL"
```

Then repeat the commit and push commands. GitHub authentication may open a browser.

## Run the app locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run App.py
```

If PowerShell blocks activation, you can skip activation and use `.venv\Scripts\python.exe -m pip install -r requirements.txt` followed by `.venv\Scripts\python.exe -m streamlit run App.py`.
