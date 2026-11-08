scoreboard players operation @s taller.code = @s taller.action
scoreboard players operation @s taller.code %= #100 taller.const
scoreboard players operation @s taller.value = @s taller.action
scoreboard players operation @s taller.value /= #100 taller.const
scoreboard players set @s taller.action 0
execute unless score @s taller.cd matches 0 run return fail
execute unless score @s taller.mode matches 1 run return fail
execute unless score @s taller.ttl matches 1.. run return fail
execute unless score @s taller.value = @s taller.seq run return fail
execute unless score @s taller.code matches 1..6 run return fail
scoreboard players set @s taller.cd 5
scoreboard players set @s taller.mode 0
data modify storage taller:ctx call set value {who:"@s"}
execute if score @s taller.code matches 1 run function taller:logic/craft with storage taller:ctx call
execute if score @s taller.code matches 2 run function taller:logic/claim with storage taller:ctx call
execute if score @s taller.code matches 3 run function taller:logic/next with storage taller:ctx call
execute if score @s taller.code matches 4 run function taller:logic/toggle with storage taller:ctx call
execute if score @s taller.code matches 6 run return run function taller:ui/close
function taller:hud/update
execute if score @s taller.code matches 5 run return run function taller:ui/settings
function taller:ui/main
