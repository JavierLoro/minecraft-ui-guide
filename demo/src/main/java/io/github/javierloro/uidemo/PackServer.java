package io.github.javierloro.uidemo;

import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Serves only the embedded pack; never exposes a directory or player data. */
public final class PackServer implements AutoCloseable {
    private final HttpServer server;
    private final ExecutorService executor = Executors.newFixedThreadPool(2);
    private final byte[] sha1;
    public PackServer(String bind, int port, byte[] pack) throws IOException {
        try { sha1 = MessageDigest.getInstance("SHA-1").digest(pack); }
        catch (NoSuchAlgorithmException e) { throw new IllegalStateException(e); }
        server = HttpServer.create(new InetSocketAddress(bind, port), 0);
        server.setExecutor(executor);
        server.createContext("/pack.zip", exchange -> {
            try {
                if (!exchange.getRequestURI().getPath().equals("/pack.zip")) {
                    exchange.sendResponseHeaders(404, -1); return;
                }
                String method = exchange.getRequestMethod();
                if (!method.equals("GET") && !method.equals("HEAD")) {
                    exchange.getResponseHeaders().set("Allow", "GET, HEAD");
                    exchange.sendResponseHeaders(405, -1); return;
                }
                exchange.getResponseHeaders().set("Content-Type", "application/zip");
                exchange.getResponseHeaders().set("Cache-Control", "no-cache");
                if (method.equals("HEAD")) {
                    exchange.getResponseHeaders().set("Content-Length", Integer.toString(pack.length));
                    exchange.sendResponseHeaders(200, -1);
                } else {
                    exchange.sendResponseHeaders(200, pack.length);
                    exchange.getResponseBody().write(pack);
                }
            } finally { exchange.close(); }
        });
        server.start();
    }
    int port() { return server.getAddress().getPort(); }
    public byte[] sha1() { return sha1.clone(); }
    @Override public void close() { server.stop(0); executor.shutdownNow(); }
}
