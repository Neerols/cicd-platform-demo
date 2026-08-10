# How to use this demo with cicd-platform

This repo is a minimal Flask service meant to exercise your `Neerols/cicd-platform`
GitLab CI pipeline templates end-to-end: build, test, package, and deploy to Kubernetes via Helm.

## What's inside

- `app/` — Flask app with `/`, `/health`, `/version`, `/fail` endpoints.
- `tests/test_health.py` — pytest unit tests for the app.
- `Dockerfile` — builds a small non-root container image, runs via gunicorn on port 8080.
- `docker-compose.yml` — optional local run/fallback, not required for Helm deploy.
- `helm/` — Helm chart with Deployment, Service, optional Ingress, liveness/readiness
  probes on `/health`, resource limits, and `APP_VERSION`/`PORT` env vars driven by `values.yaml`.
- `.gitlab-ci.yml.example` — placeholder stages; replace with an `include:` of your
  actual `cicd-platform` pipeline file and its expected variables.

## Steps to wire it into your real pipeline

1. In GitLab, import or mirror this GitHub repo (or push it as a mirror) into a project
   in your GitLab instance where `cicd-platform` runners/templates are available.
2. Rename `.gitlab-ci.yml.example` to `.gitlab-ci.yml` and replace its contents with the
   `include:` for your platform (e.g. the consumer or two-releases example from
   `Neerols/cicd-platform`).
3. Set the CI/CD variables your platform expects for a Helm/Kubernetes deploy, typically:
   - `KUBE_CONTEXT` / kubeconfig or service account credentials for the target cluster
   - `HELM_CHART_PATH=helm`
   - `HELM_RELEASE_NAME=cicd-platform-demo`
   - `K8S_NAMESPACE` for the target namespace
   - `IMAGE_TAG` (e.g. `$CI_COMMIT_SHORT_SHA`)
   - Container registry variables if your platform pushes to an external registry rather
     than the built-in GitLab Container Registry.
4. Confirm build stage produces and pushes an image tagged consistently with what
   `helm/values.yaml` (`image.repository`/`image.tag`) expects, or override them via
   `--set image.tag=$IMAGE_TAG` / `--set image.repository=...` in the deploy job.
5. Run the pipeline. Expected flow:
   - Build: Docker image built from `Dockerfile`.
   - Test: `pip install -r requirements-dev.txt && pytest` runs the 4 tests in `tests/`.
   - Package: image pushed to registry.
   - Deploy: `helm upgrade --install cicd-platform-demo ./helm -n <namespace> --set image.tag=<tag>`.
6. Smoke test after deploy: `curl http://<service-or-ingress-host>/health` should return
   `{"status": "ok"}` with HTTP 200. `/version` should reflect `APP_VERSION` set for that release.
7. To test rollback/failure handling in your platform, point a smoke test or synthetic
   check at `/fail` (returns HTTP 500) and see how the pipeline reacts.

## Notes

- No secrets or real registry/cluster values are included — replace the placeholders
  in `helm/values.yaml` (`image.repository`, `ingress.host`) with your real values.
- The Helm chart is intentionally simple (Deployment + Service + optional Ingress) so
  it's easy to see exactly what each pipeline stage changed.
