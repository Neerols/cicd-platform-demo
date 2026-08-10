{{- define "cicd-platform-demo.fullname" -}}
{{- .Release.Name -}}
{{- end -}}

{{- define "cicd-platform-demo.labels" -}}
app.kubernetes.io/name: cicd-platform-demo
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
