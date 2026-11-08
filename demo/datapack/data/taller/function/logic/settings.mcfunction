# Form payload = goal * 100 + visible * 10 + anchor. Only accept declared ranges.
$scoreboard players operation #goal taller.test = $(who) taller.value
scoreboard players operation #goal taller.test /= #100 taller.const
$scoreboard players operation #flags taller.test = $(who) taller.value
scoreboard players operation #flags taller.test %= #100 taller.const
scoreboard players operation #hud taller.test = #flags taller.test
scoreboard players operation #hud taller.test /= #10 taller.const
scoreboard players operation #anchor taller.test = #flags taller.test
scoreboard players operation #anchor taller.test %= #10 taller.const
execute unless score #goal taller.test matches 1..12 run return fail
execute unless score #hud taller.test matches 0..1 run return fail
execute unless score #anchor taller.test matches 0..1 run return fail
$execute unless score $(who) taller.goal = #goal taller.test run scoreboard players set $(who) taller.pieces 0
$execute unless score $(who) taller.goal = #goal taller.test run scoreboard players set $(who) taller.claimed 0
$scoreboard players operation $(who) taller.goal = #goal taller.test
$scoreboard players operation $(who) taller.hud = #hud taller.test
$scoreboard players operation $(who) taller.anchor = #anchor taller.test
