scoreboard players set #errors taller.test 0
scoreboard players set #checks taller.test 0
scoreboard players set #demoA taller.goal 5
scoreboard players set #demoA taller.pieces 0
scoreboard players set #demoA taller.coins 0
scoreboard players set #demoA taller.claimed 0
scoreboard players set #demoA taller.hud 1
scoreboard players set #demoA taller.anchor 0
scoreboard players set #demoB taller.goal 5
scoreboard players set #demoB taller.pieces 0
scoreboard players set #demoB taller.coins 0
scoreboard players set #demoB taller.claimed 0
scoreboard players set #demoB taller.hud 1
scoreboard players set #demoB taller.anchor 0
data modify storage taller:ctx call set value {who:"#demoA"}
function taller:logic/claim with storage taller:ctx call
execute unless score #demoA taller.coins matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
function taller:logic/craft with storage taller:ctx call
execute unless score #demoA taller.pieces matches 5 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoB taller.pieces matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/claim with storage taller:ctx call
execute unless score #demoA taller.coins matches 25 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.claimed matches 1 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/claim with storage taller:ctx call
execute unless score #demoA taller.coins matches 25 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoB taller.coins matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/next with storage taller:ctx call
execute unless score #demoA taller.pieces matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.claimed matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.coins matches 25 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/toggle with storage taller:ctx call
execute unless score #demoA taller.hud matches 0 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
function taller:logic/toggle with storage taller:ctx call
execute unless score #demoA taller.hud matches 1 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 811
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.hud matches 1 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.anchor matches 1 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
execute unless score #demoA taller.coins matches 25 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 0
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 1300
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 9999
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 822
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value 1099
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
scoreboard players set #demoA taller.value -1
function taller:logic/settings with storage taller:ctx call
execute unless score #demoA taller.goal matches 8 run scoreboard players add #errors taller.test 1
scoreboard players add #checks taller.test 1
data modify storage taller:test report set value {checks:0,errors:0}
execute store result storage taller:test report.checks int 1 run scoreboard players get #checks taller.test
execute store result storage taller:test report.errors int 1 run scoreboard players get #errors taller.test
execute if score #errors taller.test matches 1.. run return fail
return 1
