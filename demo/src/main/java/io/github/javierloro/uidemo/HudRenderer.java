package io.github.javierloro.uidemo;

import net.kyori.adventure.bossbar.BossBar;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.TextColor;
import org.bukkit.entity.Player;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/** The fixed 160px advance is also part of the optional shader contract. */
public final class HudRenderer {
    private static final Key HUD = Key.key("taller:hud");
    private static final Key LABEL = Key.key("taller:label");
    private static final Key VALUE = Key.key("taller:value");
    private static final Key SPACE = Key.key("taller:space");
    private final Map<UUID, BossBar> bars = new HashMap<>();
    public void update(Player player, WorkshopState state, boolean packLoaded) {
        if (!state.hudVisible()) { remove(player); return; }
        Component name = packLoaded ? graphic(state) : Component.text(state.project() + " | Piezas "
            + state.crafted() + "/" + state.target() + " | Saldo " + state.coins(), TextColor.color(0x51d4cb));
        BossBar bar = bars.computeIfAbsent(player.getUniqueId(), id -> {
            BossBar created = BossBar.bossBar(name, 1f, BossBar.Color.WHITE, BossBar.Overlay.PROGRESS);
            player.showBossBar(created); return created;
        });
        bar.name(name);
    }
    private Component graphic(WorkshopState s) {
        TextColor white = TextColor.color(s.anchored() ? 0xfa02f0 : 0xffffff);
        TextColor teal = TextColor.color(s.anchored() ? 0xfa02e0 : 0x51d4cb);
        String detail = "PIEZAS " + s.crafted() + "/" + s.target();
        int width = detail.chars().map(c -> c == ' ' ? 4 : 6).sum();
        int frame = s.crafted() * 5 / s.target();
        return Component.empty()
            .append(Component.text("\uE000", white).font(HUD))
            .append(move(-151))
            .append(Component.text("TALLER", teal).font(LABEL))
            .append(move(-36))
            .append(Component.text(detail, white).font(VALUE))
            .append(move(-width))
            .append(Component.text(String.valueOf((char) (0xe010 + frame)), white).font(HUD))
            .append(move(9));
    }
    private Component move(int pixels) {
        StringBuilder result = new StringBuilder();
        int value = Math.abs(pixels), base = pixels < 0 ? 0xf010 : 0xf000;
        for (int bit = 0; value != 0; bit++, value >>>= 1)
            if ((value & 1) != 0) result.append((char) (base + bit));
        return Component.text(result.toString()).font(SPACE);
    }
    public void remove(Player player) {
        BossBar bar = bars.remove(player.getUniqueId());
        if (bar != null) player.hideBossBar(bar);
    }
}
