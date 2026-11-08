package io.github.javierloro.uidemo;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class WorkshopStateTest {
    @Test void cannotClaimAnUnfinishedOrder() {
        var s = WorkshopState.initial(false);
        assertEquals(s, s.claim());
    }
    @Test void craftingIsBoundedAndPaymentIsIdempotent() {
        var s = WorkshopState.initial(false);
        for (int i = 0; i < 100; i++) s = s.craft();
        assertEquals(5, s.crafted());
        s = s.claim();
        for (int i = 0; i < 100; i++) s = s.claim();
        assertEquals(25, s.coins());
        assertTrue(s.claimed());
    }
    @Test void nextOrderKeepsPreferencesAndBalance() {
        var s = WorkshopState.initial(true).settings("Proyecto", false, true, 1).craft().claim().nextOrder();
        assertEquals(25, s.coins()); assertEquals(0, s.crafted());
        assertFalse(s.hudVisible()); assertTrue(s.anchored()); assertFalse(s.claimed());
    }
    @Test void changingTheGoalResetsOnlyTheOrder() {
        var s = WorkshopState.initial(false).settings("Proyecto", true, false, 1).craft().claim();
        var changed = s.settings("Proyecto", true, true, 8);
        assertEquals(25, changed.coins()); assertEquals(0, changed.crafted()); assertFalse(changed.claimed());
    }
    @Test void rejectsMalformedClientSettings() {
        var s = WorkshopState.initial(false);
        assertThrows(IllegalArgumentException.class, () -> s.settings("", true, false, 5));
        assertThrows(IllegalArgumentException.class, () -> s.settings("Taller", true, false, 0));
        assertThrows(IllegalArgumentException.class, () -> s.settings("Taller", true, false, 13));
    }
}
