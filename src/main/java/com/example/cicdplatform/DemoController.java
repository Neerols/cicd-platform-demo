package com.example.cicdplatform;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class DemoController {

    @Value("${app.version:dev}")
    private String appVersion;

    @GetMapping("/")
    public Map<String, String> index() {
        return Map.of(
                "message", "cicd-platform-demo is running",
                "version", appVersion
        );
    }

    @GetMapping("/version")
    public Map<String, String> version() {
        return Map.of("version", appVersion);
    }
}
