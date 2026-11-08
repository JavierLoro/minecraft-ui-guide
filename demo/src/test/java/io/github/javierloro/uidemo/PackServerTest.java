package io.github.javierloro.uidemo;
import org.junit.jupiter.api.Test;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.security.MessageDigest;
import static org.junit.jupiter.api.Assertions.*;
class PackServerTest {
    @Test void servesOnlyThePackAndReturnsItsDigest() throws Exception {
        byte[] payload = {80, 75, 3, 4};
        try (var server = new PackServer("127.0.0.1", 0, payload); var client = HttpClient.newHttpClient()) {
            String base = "http://127.0.0.1:" + server.port();
            var good = client.send(HttpRequest.newBuilder(URI.create(base + "/pack.zip")).build(), HttpResponse.BodyHandlers.ofByteArray());
            assertEquals(200, good.statusCode()); assertArrayEquals(payload, good.body());
            assertEquals("application/zip", good.headers().firstValue("Content-Type").orElseThrow());
            assertArrayEquals(MessageDigest.getInstance("SHA-1").digest(payload), server.sha1());
            byte[] copy = server.sha1(); copy[0] ^= 1;
            assertArrayEquals(MessageDigest.getInstance("SHA-1").digest(payload), server.sha1());
            var invalid = client.send(HttpRequest.newBuilder(URI.create(base + "/pack.zip/private")).build(), HttpResponse.BodyHandlers.ofByteArray());
            assertEquals(404, invalid.statusCode());
            var post = client.send(HttpRequest.newBuilder(URI.create(base + "/pack.zip")).POST(HttpRequest.BodyPublishers.noBody()).build(), HttpResponse.BodyHandlers.ofByteArray());
            assertEquals(405, post.statusCode());
            var head = client.send(HttpRequest.newBuilder(URI.create(base + "/pack.zip")).method("HEAD", HttpRequest.BodyPublishers.noBody()).build(), HttpResponse.BodyHandlers.ofByteArray());
            assertEquals(200, head.statusCode()); assertEquals(0, head.body().length);
        }
    }
}
