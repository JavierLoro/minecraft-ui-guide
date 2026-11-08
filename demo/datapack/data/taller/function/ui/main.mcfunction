scoreboard players set @s taller.open 0
scoreboard players set @s taller.mode 1
scoreboard players set @s taller.ttl 2400
scoreboard players add @s taller.seq 1
execute if score @s taller.seq matches 1000000.. run scoreboard players set @s taller.seq 1
function taller:ui/context
scoreboard players operation #token taller.test = @s taller.seq
scoreboard players operation #token taller.test *= #100 taller.const
scoreboard players add #token taller.test 1
data modify storage taller:ctx view.primary_label set value "Fabricar pieza"
execute if score @s taller.pieces = @s taller.goal run data modify storage taller:ctx view.primary_label set value "Cobrar 25"
execute if score @s taller.pieces = @s taller.goal run scoreboard players add #token taller.test 1
execute if score @s taller.claimed matches 1 run data modify storage taller:ctx view.primary_label set value "Nuevo pedido"
execute if score @s taller.claimed matches 1 run scoreboard players add #token taller.test 1
execute store result storage taller:ctx view.primary int 1 run scoreboard players get #token taller.test
scoreboard players operation #token taller.test = @s taller.seq
scoreboard players operation #token taller.test *= #100 taller.const
scoreboard players add #token taller.test 4
execute store result storage taller:ctx view.toggle int 1 run scoreboard players get #token taller.test
scoreboard players add #token taller.test 1
execute store result storage taller:ctx view.settings int 1 run scoreboard players get #token taller.test
data modify storage taller:ctx view.toggle_label set value "Ocultar HUD"
execute if score @s taller.hud matches 0 run data modify storage taller:ctx view.toggle_label set value "Mostrar HUD"
scoreboard players add #token taller.test 1
execute store result storage taller:ctx view.close int 1 run scoreboard players get #token taller.test
scoreboard players enable @s taller.action
scoreboard players enable @s taller.open
function taller:ui/show with storage taller:ctx view
