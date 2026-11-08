scoreboard players operation @s taller.value = @s taller.form
scoreboard players set @s taller.form 0
execute unless score @s taller.cd matches 0 run return fail
execute unless score @s taller.mode matches 2 run return fail
execute unless score @s taller.ttl matches 1.. run return fail
scoreboard players set @s taller.cd 5
scoreboard players set @s taller.mode 0
data modify storage taller:ctx call set value {who:"@s"}
function taller:logic/settings with storage taller:ctx call
function taller:hud/update
function taller:ui/main
