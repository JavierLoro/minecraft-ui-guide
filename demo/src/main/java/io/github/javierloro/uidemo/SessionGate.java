package io.github.javierloro.uidemo;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.time.Duration;

/** Called on the server thread. Each accepted click consumes its screen session. */
public final class SessionGate {
    private record Session(long token, long expiresAt) {}
    private static final long LIFETIME = Duration.ofMinutes(2).toNanos();
    private static final long COOLDOWN = Duration.ofMillis(250).toNanos();
    private final Map<UUID, Session> sessions = new HashMap<>();
    private final Map<UUID, Long> lastAccepted = new HashMap<>();
    private long sequence;
    public long open(UUID player, long now) {
        long token = ++sequence;
        sessions.put(player, new Session(token, now + LIFETIME));
        return token;
    }
    public boolean accept(UUID player, long token, long now) {
        Session s = sessions.get(player);
        Long previous = lastAccepted.get(player);
        if (s == null || s.token != token || now > s.expiresAt
            || (previous != null && now - previous < COOLDOWN)) return false;
        sessions.remove(player);
        lastAccepted.put(player, now);
        return true;
    }
    public void remove(UUID player) { sessions.remove(player); lastAccepted.remove(player); }
    public void clear() { sessions.clear(); lastAccepted.clear(); }
}
