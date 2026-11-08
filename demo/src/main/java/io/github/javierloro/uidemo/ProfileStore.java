package io.github.javierloro.uidemo;

import org.bukkit.configuration.file.YamlConfiguration;
import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.nio.file.AtomicMoveNotSupportedException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/** Small local profiles. Disk writes complete before the in-memory state changes. */
public final class ProfileStore {
    private final Path directory;
    private final boolean anchored;
    private final Map<UUID, WorkshopState> profiles = new HashMap<>();
    public ProfileStore(Path directory, boolean anchored) throws IOException {
        this.directory = directory; this.anchored = anchored; Files.createDirectories(directory);
    }
    public WorkshopState get(UUID id) {
        return profiles.computeIfAbsent(id, key -> {
            Path file = directory.resolve(key + ".yml");
            if (!Files.exists(file)) return WorkshopState.initial(anchored);
            try {
                YamlConfiguration y = new YamlConfiguration();
                y.load(file.toFile());
                return new WorkshopState(y.getString("project", "Mi taller"), y.getBoolean("hud", true),
                    y.getBoolean("anchored", anchored), y.getInt("target", 5), y.getInt("crafted", 0),
                    y.getInt("coins", 0), y.getBoolean("claimed", false));
            } catch (Exception e) {
                throw new IllegalStateException("No se ha sobrescrito el perfil inválido " + key, e);
            }
        });
    }
    public void put(UUID id, WorkshopState state) throws IOException {
        YamlConfiguration y = new YamlConfiguration();
        y.set("schema", 1); y.set("project", state.project()); y.set("hud", state.hudVisible());
        y.set("anchored", state.anchored()); y.set("target", state.target());
        y.set("crafted", state.crafted()); y.set("coins", state.coins()); y.set("claimed", state.claimed());
        Path file = directory.resolve(id + ".yml");
        Path temp = directory.resolve(id + ".yml.tmp");
        Files.writeString(temp, y.saveToString());
        try { Files.move(temp, file, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE); }
        catch (AtomicMoveNotSupportedException e) { Files.move(temp, file, StandardCopyOption.REPLACE_EXISTING); }
        profiles.put(id, state);
    }
    public void unload(UUID id) { profiles.remove(id); }
}
