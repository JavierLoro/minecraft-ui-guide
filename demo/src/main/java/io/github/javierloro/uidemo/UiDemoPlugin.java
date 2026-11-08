package io.github.javierloro.uidemo;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.player.PlayerResourcePackStatusEvent;
import org.bukkit.plugin.java.JavaPlugin;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import java.util.List;
import java.util.function.UnaryOperator;
import java.io.IOException;
import java.io.InputStream;

public final class UiDemoPlugin extends JavaPlugin implements Listener {
    public static final UUID PACK_ID = UUID.fromString("be12b564-2603-4244-9178-070a58d1cbaf");
    private final SessionGate sessions = new SessionGate();
    private final HudRenderer hud = new HudRenderer();
    private final Set<UUID> loadedPacks = new HashSet<>();
    private ProfileStore profiles;
    private DemoDialogs dialogs;
    private PackServer packServer;
    @Override public void onEnable() {
        saveDefaultConfig();
        try {
            profiles = new ProfileStore(getDataFolder().toPath().resolve("players"),
                getConfig().getBoolean("hud.anchored-by-default", false));
        } catch (IOException e) { throw new IllegalStateException("No se pueden guardar los perfiles.", e); }
        dialogs = new DemoDialogs(this);
        try (InputStream resource = getResource("pack.zip")) {
            if (resource == null) throw new IOException("Falta pack.zip en el plugin.");
            packServer = new PackServer(getConfig().getString("resource-pack.bind", "127.0.0.1"),
                getConfig().getInt("resource-pack.port", 8127), resource.readAllBytes());
        } catch (IOException e) { getLogger().warning("Paquete no disponible; se usará la vista nativa: " + e.getMessage()); }
        getServer().getPluginManager().registerEvents(this, this);
        for (Player p : Bukkit.getOnlinePlayers()) connect(p);
        getLogger().info("Taller listo. /uidemo abre la demo; no modifica inventarios ni economías externas.");
    }
    @Override public void onDisable() {
        for (Player p : Bukkit.getOnlinePlayers()) {
            hud.remove(p); p.removeResourcePack(PACK_ID);
        }
        sessions.clear(); loadedPacks.clear();
        if (packServer != null) packServer.close();
    }
    public WorkshopState state(Player player) { return profiles.get(player.getUniqueId()); }
    public boolean packLoaded(Player player) { return loadedPacks.contains(player.getUniqueId()); }
    public long openSession(Player player) { return sessions.open(player.getUniqueId(), System.nanoTime()); }
    public void route(Player player, long token, Runnable action) {
        if (!isEnabled()) return;
        UUID id = player.getUniqueId();
        Bukkit.getScheduler().runTask(this, () -> {
            if (!player.isOnline() || !player.hasPermission("uidemo.use")) return;
            if (!sessions.accept(id, token, System.nanoTime())) {
                dialogs.main(player); return;
            }
            try { action.run(); }
            catch (IllegalArgumentException e) {
                player.sendMessage(Component.text(e.getMessage(), NamedTextColor.RED)); dialogs.main(player);
            }
        });
    }
    public void change(Player player, UnaryOperator<WorkshopState> operation) {
        WorkshopState next = operation.apply(state(player));
        try {
            profiles.put(player.getUniqueId(), next);
            hud.update(player, next, packLoaded(player)); dialogs.main(player);
        } catch (IOException e) {
            getLogger().severe("No se ha guardado el cambio: " + e.getMessage());
            player.sendMessage(Component.text("No se ha podido guardar el cambio.", NamedTextColor.RED));
            dialogs.main(player);
        }
    }
    private void connect(Player player) {
        try { hud.update(player, state(player), false); }
        catch (IllegalStateException e) { getLogger().severe(e.getMessage()); return; }
        Bukkit.getScheduler().runTaskLater(this, () -> { if (player.isOnline()) offerPack(player); }, 20L);
        player.sendMessage(Component.text("/uidemo", NamedTextColor.AQUA)
            .clickEvent(net.kyori.adventure.text.event.ClickEvent.runCommand("/uidemo")));
    }
    private void offerPack(Player p) {
        if (packServer == null) {
            p.sendMessage(Component.text("El paquete no está disponible; puedes usar el menú nativo.", NamedTextColor.YELLOW)); return;
        }
        loadedPacks.remove(p.getUniqueId());
        p.setResourcePack(PACK_ID, getConfig().getString("resource-pack.public-url"), packServer.sha1(),
            Component.text("Recursos gráficos del taller de demostración"), false);
    }
    @EventHandler public void joined(PlayerJoinEvent event) { connect(event.getPlayer()); }
    @EventHandler public void quit(PlayerQuitEvent event) {
        Player p = event.getPlayer(); hud.remove(p); sessions.remove(p.getUniqueId());
        loadedPacks.remove(p.getUniqueId()); profiles.unload(p.getUniqueId());
    }
    @EventHandler public void resourcePack(PlayerResourcePackStatusEvent event) {
        if (!event.getID().equals(PACK_ID)) return;
        Player p = event.getPlayer();
        switch (event.getStatus()) {
            case SUCCESSFULLY_LOADED -> { loadedPacks.add(p.getUniqueId()); hud.update(p, state(p), true); }
            case DECLINED, FAILED_DOWNLOAD, FAILED_RELOAD, DISCARDED, INVALID_URL -> {
                loadedPacks.remove(p.getUniqueId()); hud.update(p, state(p), false);
            }
            default -> { }
        }
    }
    @Override public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player player)) { sender.sendMessage("Abre /uidemo desde Minecraft."); return true; }
        if (!player.hasPermission("uidemo.use")) return true;
        switch (args.length == 0 ? "menu" : args[0].toLowerCase(java.util.Locale.ROOT)) {
            case "menu" -> dialogs.main(player);
            case "ajustes" -> dialogs.settings(player);
            case "hud" -> change(player, WorkshopState::toggleHud);
            case "nativo", "anclado" -> change(player, s -> s.settings(s.project(), s.hudVisible(), args[0].equalsIgnoreCase("anclado"), s.target()));
            case "pack" -> offerPack(player);
            default -> player.sendMessage(Component.text("/uidemo [menu|ajustes|hud|nativo|anclado|pack]"));
        }
        return true;
    }
    @Override public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        return args.length == 1 ? List.of("menu", "ajustes", "hud", "nativo", "anclado", "pack").stream()
            .filter(s -> s.startsWith(args[0].toLowerCase(java.util.Locale.ROOT))).toList() : List.of();
    }
}
