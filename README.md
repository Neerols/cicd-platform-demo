# cicd-platform-demo

Minimal Flask service used to test [Neerols/cicd-platform](https://github.com/Neerols/cicd-platform)
GitLab CI pipelines end-to-end: build → test → package → deploy to Kubernetes via Helm.

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for how to wire this into your real `.gitlab-ci.yml`.

## Quick local run

```bash
pip install -r requirements-dev.txt
pytest
docker compose up --build
curl http://localhost:8080/health
```

## Helm (manual, without CI)

```bash
helm upgrade --install cicd-platform-demo ./helm \
  -n cicd-platform-demo --create-namespace \
  --set image.repository=<your-registry>/cicd-platform-demo \
  --set image.tag=<tag>
```
