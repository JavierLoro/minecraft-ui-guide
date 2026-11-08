scoreboard players add #next taller.const 1
scoreboard players operation @s taller.id = #next taller.const
scoreboard players set @s taller.goal 5
scoreboard players set @s taller.pieces 0
scoreboard players set @s taller.coins 0
scoreboard players set @s taller.hud 1
scoreboard players set @s taller.anchor 0
scoreboard players set @s taller.claimed 0
scoreboard players set @s taller.seq 0
scoreboard players set @s taller.ttl 0
scoreboard players set @s taller.mode 0
scoreboard players set @s taller.cd 0
scoreboard players set @s taller.open 0
scoreboard players set @s taller.action 0
scoreboard players set @s taller.form 0
execute unless score @s taller.leave matches 0.. run scoreboard players set @s taller.leave 0
scoreboard players operation @s taller.seen = @s taller.leave
execute store result storage taller:ctx view.id int 1 run scoreboard players get @s taller.id
function taller:hud/create with storage taller:ctx view
function taller:hud/update
tellraw @s {"text":"Abrir taller","color":"aqua","click_event":{"action":"run_command","command":"trigger taller.open"},"hover_event":{"action":"show_text","value":"Abre la demo de interfaces."}}
