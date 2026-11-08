package io.github.javierloro.uidemo;

import io.papermc.paper.dialog.Dialog;
import io.papermc.paper.dialog.DialogResponseView;
import io.papermc.paper.registry.data.dialog.ActionButton;
import io.papermc.paper.registry.data.dialog.DialogBase;
import io.papermc.paper.registry.data.dialog.body.DialogBody;
import io.papermc.paper.registry.data.dialog.input.DialogInput;
import io.papermc.paper.registry.data.dialog.input.SingleOptionDialogInput.OptionEntry;
import io.papermc.paper.registry.data.dialog.type.DialogType;
import io.papermc.paper.registry.data.dialog.action.DialogAction;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.event.ClickCallback;
import net.kyori.adventure.text.event.HoverEvent;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.entity.Player;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.function.BiConsumer;

public final class DemoDialogs {
    private final UiDemoPlugin plugin;
    public DemoDialogs(UiDemoPlugin plugin) { this.plugin = plugin; }
    private Component text(String value) { return Component.text(value); }
    private ActionButton button(Player owner, long token, Component label, String tooltip,
                                BiConsumer<Player, DialogResponseView> action) {
        var ownerId = owner.getUniqueId();
        return ActionButton.create(label, text(tooltip), 150, DialogAction.customClick((view, audience) -> {
            if (audience instanceof Player player && player.getUniqueId().equals(ownerId))
                plugin.route(player, token, () -> action.accept(player, view));
        }, ClickCallback.Options.builder().uses(1).lifetime(Duration.ofMinutes(2)).build()));
    }
    private ActionButton exit() { return ActionButton.create(text("Cerrar"), null, 150, null); }
    public void main(Player player) {
        WorkshopState s = plugin.state(player);
        long token = plugin.openSession(player);
        List<ActionButton> actions = new ArrayList<>();
        if (s.claimed()) actions.add(button(player, token, text("Nuevo pedido"), "Empieza otro pedido; conserva el saldo.",
            (p, view) -> plugin.change(p, WorkshopState::nextOrder)));
        else if (s.crafted() == s.target()) actions.add(button(player, token, text("Cobrar 25"), "Cobra este pedido una sola vez.",
            (p, view) -> plugin.change(p, WorkshopState::claim)));
        else actions.add(button(player, token, text("Fabricar pieza"), "Añade una pieza al pedido de demostración.",
            (p, view) -> plugin.change(p, WorkshopState::craft)));
        Component toggle = text(s.hudVisible() ? "Ocultar HUD" : "Mostrar HUD");
        if (plugin.packLoaded(player)) toggle = Component.text(s.hudVisible() ? "\uE101 " : "\uE102 ")
            .font(Key.key("taller:icons")).append(toggle.font(Key.key("minecraft:default")));
        actions.add(button(player, token, toggle, "Cambia la visibilidad del panel y guarda la preferencia.",
            (p, view) -> plugin.change(p, WorkshopState::toggleHud)));
        actions.add(button(player, token, text("Ajustes"), "Nombre del proyecto, tamaño del pedido y presentación del HUD.",
            (p, view) -> settings(p)));
        Component summary = text(s.project()).color(NamedTextColor.AQUA)
            .append(Component.newline()).append(text("Piezas " + s.crafted() + "/" + s.target()).color(NamedTextColor.WHITE))
            .append(Component.newline()).append(text("Saldo " + s.coins()).color(NamedTextColor.GOLD)
                .hoverEvent(HoverEvent.showText(text("Saldo propio de esta demo. No modifica ninguna economía externa."))));
        player.showDialog(Dialog.create(b -> b.empty()
            .base(DialogBase.builder(text("Taller")).canCloseWithEscape(true).pause(false)
                .afterAction(DialogBase.DialogAfterAction.WAIT_FOR_RESPONSE)
                .body(List.of(DialogBody.plainMessage(summary, 320))).build())
            .type(DialogType.multiAction(actions).columns(2).exitAction(exit()).build())));
    }
    public void settings(Player player) {
        WorkshopState s = plugin.state(player);
        long token = plugin.openSession(player);
        var options = List.of(OptionEntry.create("native", text("Centrado"), !s.anchored()),
            OptionEntry.create("anchored", text("Esquina izquierda"), s.anchored()));
        ActionButton save = button(player, token, text("Guardar"), "Aplica y guarda los ajustes del taller.", (p, view) -> {
            if (view == null) { main(p); return; }
            String name = view.getText("project");
            Boolean hud = view.getBoolean("hud");
            Float goal = view.getFloat("target");
            String mode = view.getText("mode");
            if (name == null || hud == null || goal == null || !Float.isFinite(goal)
                || goal != Math.rint(goal) || !("native".equals(mode) || "anchored".equals(mode))) {
                p.sendMessage(text("No se han podido leer los ajustes.").color(NamedTextColor.RED)); main(p); return;
            }
            plugin.change(p, current -> current.settings(name, hud, mode.equals("anchored"), goal.intValue()));
        });
        player.showDialog(Dialog.create(b -> b.empty()
            .base(DialogBase.builder(text("Ajustes del taller")).canCloseWithEscape(true).pause(false)
                .afterAction(DialogBase.DialogAfterAction.WAIT_FOR_RESPONSE)
                .inputs(List.of(
                    DialogInput.text("project", text("Nombre")).initial(s.project()).maxLength(24).width(300).build(),
                    DialogInput.bool("hud", text("Mostrar HUD")).initial(s.hudVisible()).build(),
                    DialogInput.singleOption("mode", text("Posición del HUD"), options).build(),
                    DialogInput.numberRange("target", text("Piezas por pedido"), 1, 12)
                        .step(1f).initial((float) s.target()).width(300).build()))
                .build())
            .type(DialogType.confirmation(save, ActionButton.create(text("Cancelar"), null, 150, null)))));
    }
}
