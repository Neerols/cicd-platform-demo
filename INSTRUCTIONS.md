# Как использовать это демо с cicd-platform

Этот репозиторий повторяет структуру, которую `Neerols/cicd-platform` ожидает
от Maven/Java-сервиса, поэтому его можно запушить в GitLab и прогнать полный
пайплайн build → test → release → deploy в Kubernetes-кластер через Helm.

## Что внутри

- `pom.xml` — Maven-проект на Spring Boot 3 / Java 21. Использует свойства
  `revision`/`changelist` так же, как их подставляет `jobs/build_maven_project.yml`
  (`-Drevision=${APP_VERSION_SHORT} -Dchangelist=-${CI_COMMIT_SHORT_SHA}`).
- `src/main/java/...` — минимальный REST-контроллер с `/`, `/version`, а также
  Spring Boot Actuator, который отдаёт `/actuator/health` (liveness/readiness пробы).
- `src/test/java/...` — тесты на JUnit 5 для `/`, `/version`, `/actuator/health`.
- `Dockerfile` — копирует собранный jar (`target/cicd-platform-demo.jar`,
  совпадает с `finalName` в `pom.xml`) в лёгкий JRE-образ; соответствует тому,
  что ожидает `jobs/release_image.yml` (kaniko): `Dockerfile` в корне репозитория, context `.`.
- `.gitlab-ci.yml` — реальная точка входа пайплайна, просто `include:`
  темплейта `templates/maven-service-java-21.yml` из `cicd-platform`, по тому же
  паттерну, что и `examples/consumer-gitlab-ci.yml`.

Своего Helm chart здесь намеренно нет: `jobs/helm_deploy.yml` в `cicd-platform`
уже деплоит любой сервис-потребитель через встроенный chart
`helm/generic-deployment` (сквозная передача `env`, `volumes`, `extraContainers`
и т.д. через `extra_values_yaml`), сам подставляя `--set image=<собранный образ>`.
Свой chart в репозитории сервиса нужен только если ты хочешь что-то переопределить
через `extra_values_yaml`.

## Шаги запуска

1. Запушь/импортируй этот репозиторий в свой GitLab (или добавь его как remote
   и сделай `git push` в новый проект GitLab), где доступны `cicd-platform` и
   его shared runner'ы.
2. В `.gitlab-ci.yml` поправь путь `include.project` на реальный путь
   `cicd-platform` в твоей GitLab-группе (сейчас там плейсхолдер
   `ffinpay/cicd/cicd-platform`, взятый из `examples/consumer-gitlab-ci.yml`
   самой платформы).
3. Убедись, что у проекта есть доступ к тем credentials registry/кластера,
   которые ожидают блоки `cicd-platform` (`.registry_auth`, `.kaniko_auth`,
   `.k8s_set_context`) — они приходят из групповых/инстанс-уровневых CI/CD
   переменных, уже настроенных в самой платформе, а не из этого demo-репозитория.
4. Запусти пайплайн. Стадии из `templates/maven-service-java-21.yml`:
   - `collect-metadata` — вычисляет `APP_VERSION`/`APP_VERSION_SHORT`.
   - `build-binary` — `mvn package` с `-Drevision`/`-Dchangelist`, собирает
     `target/cicd-platform-demo.jar`.
   - `sonar-scan` (если включён выше по пайплайну).
   - `release-image` — kaniko собирает `Dockerfile` и пушит
     `${IMAGE_NAME}:${APP_VERSION}` (и `:latest` на тегах).
   - `deploy-k8s-dev` / `deploy-k8s-test` / `deploy-k8s-prod` —
     `helm upgrade --install` в `helm/generic-deployment`; `dev` разворачивается
     автоматически, `test`/`prod` по умолчанию manual (см. `jobs/helm_deploy.yml`).
5. После деплоя сделай smoke-test Kubernetes-сервиса: через port-forward или
   ingress выполни `curl http://<host>/actuator/health` — должен вернуться
   `{"status":"UP"}`, а `curl http://<host>/version` должен отражать
   `APP_VERSION`, который пайплайн передал (через переменную окружения
   `APP_VERSION`, см. `application.yml`).

## Заметки

- Здесь нет захардкоженных секретов, имён кластеров или путей registry — всё
  берётся из переменных самой `cicd-platform` и настроек твоего GitLab-проекта.
- Если для этого демо-сервиса нужны дополнительные env-переменные, volumes или
  sidecar-контейнер, передай их через `extra_values_yaml` в inputs job'а
  `helm_deploy` в `.gitlab-ci.yml`, по аналогии с примерами
  `examples/multi-cert-gitlab-ci.yml` и `examples/sidecar-container-gitlab-ci.yml`
  из `cicd-platform`.
