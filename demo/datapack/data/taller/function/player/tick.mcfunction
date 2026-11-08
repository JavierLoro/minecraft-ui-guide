execute unless score @s taller.id matches 1.. run function taller:player/init
execute unless score @s taller.seen = @s taller.leave run function taller:player/rejoin
execute if score @s taller.cd matches 1.. run scoreboard players remove @s taller.cd 1
execute if score @s taller.ttl matches 1.. run scoreboard players remove @s taller.ttl 1
execute if score @s taller.open matches 1.. if score @s taller.cd matches 0 run function taller:ui/main
execute if score @s taller.cd matches 0 if score @s taller.action matches 1.. run function taller:input/action
execute if score @s taller.cd matches 0 if score @s taller.form matches 1.. run function taller:input/form
execute if score @s taller.cd matches 0 run scoreboard players enable @s taller.open
execute if score @s taller.cd matches 0 if score @s taller.ttl matches 1.. if score @s taller.mode matches 1 run scoreboard players enable @s taller.action
execute if score @s taller.cd matches 0 if score @s taller.ttl matches 1.. if score @s taller.mode matches 2 run scoreboard players enable @s taller.form
