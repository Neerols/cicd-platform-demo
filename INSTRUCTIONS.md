# How to use this demo with cicd-platform

This repo mirrors the real structure `Neerols/cicd-platform` expects for a
Maven/Java service, so you can push it into GitLab and run the full
build → test → release → deploy pipeline against a Kubernetes cluster via Helm.

## What's inside

- `pom.xml` — Spring Boot 3 / Java 21 Maven project. Uses `revision`/`changelist`
  properties the same way `jobs/build_maven_project.yml` sets them
  (`-Drevision=${APP_VERSION_SHORT} -Dchangelist=-${CI_COMMIT_SHORT_SHA}`).
- `src/main/java/...` — minimal REST controller with `/`, `/version`, plus Spring
  Boot Actuator exposing `/actuator/health` (liveness/readiness probes).
- `src/test/java/...` — JUnit 5 tests hitting `/`, `/version`, `/actuator/health`.
- `Dockerfile` — copies the built jar (`target/cicd-platform-demo.jar`, matching
  `finalName` in `pom.xml`) into a slim JRE image, matches what
  `jobs/release_image.yml` (kaniko) expects: a `Dockerfile` at repo root, context `.`.
- `.gitlab-ci.yml` — real pipeline entry point, just an `include:` of
  `templates/maven-service-java-21.yml` from `cicd-platform`, same pattern as
  `examples/consumer-gitlab-ci.yml`.

No custom Helm chart is included here on purpose: `cicd-platform`'s
`jobs/helm_deploy.yml` already deploys every consumer service using its own
built-in chart at `helm/generic-deployment` (passthrough `env`, `volumes`,
`extraContainers`, etc. via `extra_values_yaml`), setting `--set image=<built image>`
automatically. You don't need a chart in the service repo unless you want to
override something with `extra_values_yaml`.

## Steps to run it

1. Push/import this repo into your GitLab instance (or add it as a remote and
   `git push` to a new GitLab project) where `cicd-platform` and its shared
   runners are available.
2. In `.gitlab-ci.yml`, fix the `include.project` path to the real path of
   `cicd-platform` in your GitLab group (currently a placeholder
   `ffinpay/cicd/cicd-platform`, matching what's used in the platform's own
   `examples/consumer-gitlab-ci.yml`).
3. Make sure your project has access to whatever registry/cluster credentials
   `cicd-platform`'s blocks (`.registry_auth`, `.kaniko_auth`, `.k8s_set_context`)
   expect — these come from group/instance-level CI/CD variables already wired
   into the platform, not from this demo repo.
4. Run the pipeline. Stages from `templates/maven-service-java-21.yml`:
   - `collect-metadata` — computes `APP_VERSION`/`APP_VERSION_SHORT`.
   - `build-binary` — `mvn package` with `-Drevision`/`-Dchangelist`, produces
     `target/cicd-platform-demo.jar`.
   - `sonar-scan` (if enabled upstream).
   - `release-image` — kaniko builds `Dockerfile` and pushes
     `${IMAGE_NAME}:${APP_VERSION}` (and `:latest` on tags).
   - `deploy-k8s-dev` / `deploy-k8s-test` / `deploy-k8s-prod` —
     `helm upgrade --install` against `helm/generic-deployment`, `dev` runs
     automatically, `test`/`prod` are manual by default (see `jobs/helm_deploy.yml`).
5. After deploy, smoke test the Kubernetes service: port-forward or hit the
   ingress, then `curl http://<host>/actuator/health` should return `{"status":"UP"}`
   and `curl http://<host>/version` should reflect the `APP_VERSION` set by the
   pipeline (passed as the `APP_VERSION` env var, matching `application.yml`).

## Notes

- No secrets, cluster names, or registry paths are hardcoded here — they all
  come from `cicd-platform`'s own variables and your GitLab project settings.
- If you need extra env vars, volumes, or a sidecar for this demo service, pass
  them via `extra_values_yaml` on the `helm_deploy` job inputs in
  `.gitlab-ci.yml`, following the examples in `cicd-platform`'s
  `examples/multi-cert-gitlab-ci.yml` and `examples/sidecar-container-gitlab-ci.yml`.
