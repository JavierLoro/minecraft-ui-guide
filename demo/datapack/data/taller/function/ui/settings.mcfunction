scoreboard players set @s taller.mode 2
scoreboard players set @s taller.ttl 2400
scoreboard players add @s taller.seq 1
scoreboard players set @s taller.action 0
scoreboard players set @s taller.form 0
function taller:ui/context
function taller:ui/show_settings with storage taller:ctx view
scoreboard players enable @s taller.form
scoreboard players enable @s taller.open
