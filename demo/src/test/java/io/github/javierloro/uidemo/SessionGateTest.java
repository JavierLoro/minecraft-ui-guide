package io.github.javierloro.uidemo;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class SessionGateTest {
    @Test void rejectsWrongPlayerReplayedAndStaleScreens() {
        var gate = new SessionGate(); var id = UUID.randomUUID();
        long old = gate.open(id, 0), current = gate.open(id, 1);
        assertFalse(gate.accept(id, old, 2));
        assertFalse(gate.accept(UUID.randomUUID(), current, 2));
        assertTrue(gate.accept(id, current, 2));
        assertFalse(gate.accept(id, current, 3));
    }
    @Test void expiresAndThrottlesWithoutConsumingTheNewScreen() {
        var gate = new SessionGate(); var id = UUID.randomUUID();
        long a = gate.open(id, 0); assertFalse(gate.accept(id, a, 121_000_000_000L));
        long b = gate.open(id, 122_000_000_000L); assertTrue(gate.accept(id, b, 122_000_000_001L));
        long c = gate.open(id, 122_000_000_002L);
        assertFalse(gate.accept(id, c, 122_000_000_003L));
        assertTrue(gate.accept(id, c, 122_300_000_003L));
    }
    @Test void disconnectInvalidatesTheScreen() {
        var gate = new SessionGate(); var id = UUID.randomUUID();
        long token = gate.open(id, 0); gate.remove(id); assertFalse(gate.accept(id, token, 1));
    }
}
