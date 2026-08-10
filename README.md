# cicd-platform-demo

Minimal Maven/Spring Boot service used to test
[Neerols/cicd-platform](https://github.com/Neerols/cicd-platform) GitLab CI
pipelines end-to-end: build → test → release (Docker image via kaniko) →
deploy to Kubernetes via the platform's built-in Helm chart.

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for how to wire this into your real
GitLab project.

## Quick local run

```bash
mvn package
java -jar target/cicd-platform-demo.jar
curl http://localhost:8080/actuator/health
curl http://localhost:8080/version
```

## Local Docker build

```bash
mvn package
docker build -t cicd-platform-demo:local .
docker run --rm -p 8080:8080 -e APP_VERSION=local cicd-platform-demo:local
```
