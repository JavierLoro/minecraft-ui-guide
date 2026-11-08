scoreboard players operation @s taller.seen = @s taller.leave
scoreboard players add @s taller.seq 1
scoreboard players set @s taller.ttl 0
scoreboard players set @s taller.mode 0
scoreboard players set @s taller.open 0
scoreboard players set @s taller.action 0
scoreboard players set @s taller.form 0
function taller:hud/update
