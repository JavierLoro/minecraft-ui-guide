function taller:ui/context
execute if score @s taller.hud matches 0 run return run function taller:hud/hide with storage taller:ctx view
scoreboard players operation #frame taller.test = @s taller.pieces
scoreboard players operation #frame taller.test *= #5 taller.const
scoreboard players operation #frame taller.test /= @s taller.goal
data modify storage taller:ctx view.back set value ""
execute if score @s taller.pieces matches 10.. run data modify storage taller:ctx view.back set value ""
execute if score @s taller.goal matches 10.. run data modify storage taller:ctx view.back set value ""
execute if score @s taller.pieces matches 10.. if score @s taller.goal matches 10.. run data modify storage taller:ctx view.back set value ""
data modify storage taller:ctx view.white set value "#ffffff"
data modify storage taller:ctx view.teal set value "#51d4cb"
execute if score @s taller.anchor matches 1 run data modify storage taller:ctx view.white set value "#fa02f0"
execute if score @s taller.anchor matches 1 run data modify storage taller:ctx view.teal set value "#fa02e0"
execute if score #frame taller.test matches 0 run data modify storage taller:ctx view.bar set value ""
execute if score #frame taller.test matches 1 run data modify storage taller:ctx view.bar set value ""
execute if score #frame taller.test matches 2 run data modify storage taller:ctx view.bar set value ""
execute if score #frame taller.test matches 3 run data modify storage taller:ctx view.bar set value ""
execute if score #frame taller.test matches 4 run data modify storage taller:ctx view.bar set value ""
execute if score #frame taller.test matches 5 run data modify storage taller:ctx view.bar set value ""
function taller:hud/apply with storage taller:ctx view
