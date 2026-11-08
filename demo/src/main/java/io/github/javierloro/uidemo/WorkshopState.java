package io.github.javierloro.uidemo;

/** Pure demo rules. No inventory, account balance or third-party economy is touched. */
public record WorkshopState(String project, boolean hudVisible, boolean anchored,
                            int target, int crafted, int coins, boolean claimed) {
    public static final int REWARD = 25;
    public WorkshopState {
        if (project == null || project.isBlank() || project.length() > 24
            || project.codePoints().anyMatch(Character::isISOControl))
            throw new IllegalArgumentException("El nombre debe tener entre 1 y 24 caracteres.");
        project = project.strip();
        if (target < 1 || target > 12 || crafted < 0 || crafted > target || coins < 0
            || (claimed && crafted != target)) throw new IllegalArgumentException("Estado de pedido no válido.");
    }
    public static WorkshopState initial(boolean anchored) {
        return new WorkshopState("Mi taller", true, anchored, 5, 0, 0, false);
    }
    public WorkshopState craft() {
        return crafted == target || claimed ? this
            : new WorkshopState(project, hudVisible, anchored, target, crafted + 1, coins, false);
    }
    public WorkshopState claim() {
        return claimed || crafted != target || coins > Integer.MAX_VALUE - REWARD ? this
            : new WorkshopState(project, hudVisible, anchored, target, crafted, coins + REWARD, true);
    }
    public WorkshopState nextOrder() {
        return !claimed ? this : new WorkshopState(project, hudVisible, anchored, target, 0, coins, false);
    }
    public WorkshopState toggleHud() {
        return new WorkshopState(project, !hudVisible, anchored, target, crafted, coins, claimed);
    }
    public WorkshopState settings(String name, boolean visible, boolean anchor, int goal) {
        boolean changed = goal != target;
        return new WorkshopState(name, visible, anchor, goal, changed ? 0 : crafted, coins, changed ? false : claimed);
    }
}
