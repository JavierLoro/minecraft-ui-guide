plugins { java }
group = "io.github.javierloro"
version = "0.1.0"
repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
}
dependencies {
    compileOnly("io.papermc.paper:paper-api:26.3.build.244-stable")
    testImplementation(platform("org.junit:junit-bom:5.13.4"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
java { toolchain.languageVersion.set(JavaLanguageVersion.of(25)) }
tasks.withType<JavaCompile>().configureEach { options.encoding = "UTF-8" }
tasks.test { useJUnitPlatform() }
val resourcePack by tasks.registering(Zip::class) {
    from("pack")
    archiveFileName.set("taller-pack.zip")
    destinationDirectory.set(layout.buildDirectory.dir("pack"))
    isPreserveFileTimestamps = false
    isReproducibleFileOrder = true
}
val pluginVersion = project.version.toString()
tasks.processResources {
    inputs.property("pluginVersion", pluginVersion)
    dependsOn(resourcePack)
    from(resourcePack) { rename { "pack.zip" } }
    filesMatching("plugin.yml") { expand("version" to pluginVersion) }
}
tasks.jar {
    archiveFileName.set("minecraft-ui-demo.jar")
    isPreserveFileTimestamps = false
    isReproducibleFileOrder = true
}
