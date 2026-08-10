# cicd-platform-demo

Минимальный Maven/Spring Boot сервис для тестирования GitLab CI пайплайнов
[Neerols/cicd-platform](https://github.com/Neerols/cicd-platform) от начала до конца:
build → test → release (Docker-образ через kaniko) → деплой в Kubernetes
через встроенный Helm chart платформы.

Как подключить это к своему реальному GitLab-проекту — см. [INSTRUCTIONS.md](./INSTRUCTIONS.md).

## Быстрый запуск локально

```bash
mvn package
java -jar target/cicd-platform-demo.jar
curl http://localhost:8080/actuator/health
curl http://localhost:8080/version
```

## Локальная сборка в Docker

```bash
mvn package
docker build -t cicd-platform-demo:local .
docker run --rm -p 8080:8080 -e APP_VERSION=local cicd-platform-demo:local
```
