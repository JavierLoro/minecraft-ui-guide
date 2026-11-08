scoreboard objectives add taller.id dummy
scoreboard objectives add taller.goal dummy
scoreboard objectives add taller.pieces dummy
scoreboard objectives add taller.coins dummy
scoreboard objectives add taller.hud dummy
scoreboard objectives add taller.anchor dummy
scoreboard objectives add taller.claimed dummy
scoreboard objectives add taller.seq dummy
scoreboard objectives add taller.ttl dummy
scoreboard objectives add taller.mode dummy
scoreboard objectives add taller.cd dummy
scoreboard objectives add taller.value dummy
scoreboard objectives add taller.code dummy
scoreboard objectives add taller.seen dummy
scoreboard objectives add taller.test dummy
scoreboard objectives add taller.const dummy
scoreboard objectives add taller.open trigger
scoreboard objectives add taller.action trigger
scoreboard objectives add taller.form trigger
scoreboard objectives add taller.leave minecraft.custom:minecraft.leave_game
execute unless score #next taller.const matches 0.. run scoreboard players set #next taller.const 0
scoreboard players set #5 taller.const 5
scoreboard players set #10 taller.const 10
scoreboard players set #25 taller.const 25
scoreboard players set #100 taller.const 100
scoreboard players set #1000 taller.const 1000
scoreboard players set #2 taller.const 2
