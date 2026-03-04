# Production Readiness — Submission Checklist

## Before Opening the PR

1. **Create the feature branch**
   ```bash
   git checkout -b feature/production-readiness
   ```

2. **Stage and commit all changes**
   ```bash
   git add .
   git status   # Review what's included
   git commit -m "Add production readiness: Docker, health, logging, CI"
   ```

3. **Push and open PR**
   ```bash
   git push -u origin feature/production-readiness
   ```
   Then open a pull request on GitHub against `main`.

4. **Use the PR description**
   Copy the content from `docs/PR_DESCRIPTION.md` into the PR description. The PR description must include:
   - What you built
   - What does "healthy" mean for your application?
   - How does the CI pipeline handle the missing LLM API key?
   - What would you change about the Docker setup before a real deployment?

5. **Verify CI passes**
   Check the Actions tab on GitHub. The pipeline must pass before submission.

## Local Verification (Optional)

```bash
# Create .env (required for docker compose)
cp .env.example .env
# Add OPENAI_API_KEY if you want full functionality

# Build and start
docker compose up --build -d

# Test health
curl http://localhost:8000/health

# Test E2E script (from project root)
chmod +x scripts/e2e_test.sh
./scripts/e2e_test.sh

# Open frontend
# http://localhost (port 80)
```

## Reply to the Email

Send the link to your pull request:
`https://github.com/KamranAsghar346/supportLens/pull/<PR_NUMBER>`
