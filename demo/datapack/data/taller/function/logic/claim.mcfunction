$execute unless score $(who) taller.claimed matches 0 run return fail
$execute unless score $(who) taller.pieces = $(who) taller.goal run return fail
$execute unless score $(who) taller.coins matches 0..2147483622 run return fail
$scoreboard players add $(who) taller.coins 25
$scoreboard players set $(who) taller.claimed 1
