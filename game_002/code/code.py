import pygame #載入pygame
import os #載入os
import random #載入random
import json #載入 json
import datetime #載入 datetime
import time #載入 time
import copy #載入 copy

#初始化
pygame.init() #初始化pygame
pygame.mixer.pre_init() #預初始化pygame播放器
pygame.mixer.init() #初始化pygame播放器
pygame.mixer.set_num_channels(10)
window_width = 1920 #設定視窗寬度
window_height = 1080 #設定視窗高度
FPS = 10000 #設定遊戲偵率
screen = pygame.display.set_mode((window_width, window_height)) #生成視窗
pygame.display.set_caption("BMO.exe") #設定視窗標題
clock = pygame.time.Clock() #遊戲時間使用

#遊戲數值

#玩家數值(基本傷害、基本血量、計算後實際傷害、計算後實際血量、最大血量、暴擊率、金錢數量、經驗值數量、生命數)
player_parameter = {'basic_damage' : 2, 'basic_health' : 15, 'current_damage' : 0, 'current_health' : 0, 'max_health' : 10, 'critical' : 0, 'money' : 0, 'EXP' : 0, 'life' : 0} 

#玩家數值預設值
player_parameter_default = {'basic_damage' : 2, 'basic_health' : 15, 'current_damage' : 0, 'current_health' : 0, 'max_health' : 10, 'critical' : 0, 'money' : 0, 'EXP' : 0, 'life' : 0}

#設定數值(主音量、音樂音量、音效音量)
settings = {'master_volume': 10,'music_volume': 10,'FX_volume': 10}

#設定數值預設值
settings_default = {'master_volume': 10,'music_volume': 10,'FX_volume': 10}

#天賦等級
endowment_level = {'ability' : 0, 'ATK' : 0, 'CD_speedup' : 0,'coin_add' : 0,
                    'critical' : 0, 'damage_limited' : 0, 'EXP_add' : 0, 'fire_damage' : 0,
                    'health_drain' : 0, 'health_for_damage' : 0, 'health_regeneration' : 0, 'HP' : 0,
                      'ice' : 0, 'partner' : 0, 'revive' : 0, 'sale' : 0}

#天賦最大等級
endowment_level_max = {'ability' : 20, 'ATK' : 1000, 'CD_speedup' : 20,'coin_add' : 50,
                    'critical' : 50, 'damage_limited' : 5, 'EXP_add' : 50, 'fire_damage' : 40,
                    'health_drain' : 50, 'health_for_damage' : 20, 'health_regeneration' : 40, 'HP' : 1000,
                      'ice' : 10, 'partner' : 100, 'revive' : 3, 'sale' : 10}

#天賦等級預設值
endowment_level_default = {'ability' : 0, 'ATK' : 0, 'CD_speedup' : 0,'coin_add' : 0,
                    'critical' : 0, 'damage_limited' : 0, 'EXP_add' : 0, 'fire_damage' : 0,
                    'health_drain' : 0, 'health_for_damage' : 0, 'health_regeneration' : 0, 'HP' : 0,
                      'ice' : 0, 'partner' : 0, 'revive' : 0, 'sale' : 0}

#同伴等級
partner_level = {'lv1' : 0, 'lv2' : 0, 'lv3' : 0, 'lv4' : 0, 'lv5' : 0, 'lv6' : 0} 

#同伴等級預設值
partner_level_default = {'lv1' : 0, 'lv2' : 0, 'lv3' : 0, 'lv4' : 0, 'lv5' : 0, 'lv6' : 0} 

#能力和技能等級
ability_level = {'ATK' : 0, 'HP' : 0, 'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#能力和技能等級預設值
ability_level_default = {'ATK' : 0, 'HP' : 0, 'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#能力和技能等級最大值
ability_level_max = {'fireball' : 21, 'heal' : 21, 'freeze' : 21, 'self_hurt' : 21}

#天賦經驗值花費
endowment_cost = {'ability' : 30, 'ATK' : 2, 'CD_speedup' : 30,'coin_add' : 20,
                    'critical' : 8, 'damage_limited' : 50, 'EXP_add' : 20, 'fire_damage' : 12,
                    'health_drain' : 15, 'health_for_damage' : 40, 'health_regeneration' : 10, 'HP' : 4,
                      'ice' : 30, 'partner' : 6, 'revive' : 100, 'sale' : 50}

#天賦經驗值花費預設值
endowment_cost_default = {'ability' : 30, 'ATK' : 2, 'CD_speedup' : 30,'coin_add' : 20,
                    'critical' : 8, 'damage_limited' : 50, 'EXP_add' : 20, 'fire_damage' : 12,
                    'health_drain' : 15, 'health_for_damage' : 40, 'health_regeneration' : 10, 'HP' : 4,
                      'ice' : 30, 'partner' : 6, 'revive' : 100, 'sale' : 50}

#同伴金錢花費
partner_cost = {'lv1' : 1, 'lv2' : 30, 'lv3' : 600, 'lv4' : 36000, 'lv5' : 1080000, 'lv6' : 30000000}

#同伴金錢花費預設值
partner_cost_default = {'lv1' : 1, 'lv2' : 30, 'lv3' : 600, 'lv4' : 36000, 'lv5' : 1080000, 'lv6' : 30000000}

#同伴參數
partner_parameter = {'lv1' : 0, 'lv2' : 0, 'lv3' : 0, 'lv4' : 0, 'lv5' : 0, 'lv6' : 0}

#同伴參數預設值
partner_parameter_default = {'lv1' : 0, 'lv2' : 0, 'lv3' : 0, 'lv4' : 0, 'lv5' : 0, 'lv6' : 0}

#能力和技能金錢花費
ability_cost = {'ATK' : 15, 'HP' : 15, 'fireball' : 100, 'heal' : 100, 'freeze' : 100, 'self_hurt' : 100} 

#能力和技能金錢花費預設值
ability_cost_default = {'ATK' : 15, 'HP' : 15, 'fireball' : 100, 'heal' : 100, 'freeze' : 100, 'self_hurt' : 100} 

#技能冷卻時間
ability_CD = {'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#技能冷卻時間預設值
ability_CD_default = {'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#當前選擇的天賦
endowment_select = {'select' : 0}

#天賦參數(下一階)
endowment_parameter = {'ability' : 5, 'ATK' : 20, 'CD_speedup' : 2,'coin_add' : 10,   
                    'critical' : 2, 'damage_limited' : 50, 'EXP_add' : 10, 'fire_damage' : 10,
                    'health_drain' : 1, 'health_for_damage' : 10, 'health_regeneration' : 0.2, 'HP' : 20,
                      'ice' : 0.5, 'partner' : 20, 'revive' : 1, 'sale' : 5}

#天賦參數(實際)
current_endowment_parameter = {'ability' : 0, 'ATK' : 0, 'CD_speedup' : 0,'coin_add' : 0,   
                    'critical' : 0, 'damage_limited' : 100, 'EXP_add' : 0, 'fire_damage' : 0,
                    'health_drain' : 0, 'health_for_damage' : 0, 'health_regeneration' : 0, 'HP' : 0,
                      'ice' : 0, 'partner' : 0, 'revive' : 0, 'sale' : 0}

#天賦參數(實際)預設值
current_endowment_parameter_default = {'ability' : 0, 'ATK' : 0, 'CD_speedup' : 0,'coin_add' : 0,   
                    'critical' : 0, 'damage_limited' : 100, 'EXP_add' : 0, 'fire_damage' : 0,
                    'health_drain' : 0, 'health_for_damage' : 0, 'health_regeneration' : 0, 'HP' : 0,
                      'ice' : 0, 'partner' : 0, 'revive' : 0, 'sale' : 0}

#天賦參數(下一階)預設值
endowment_parameter_default = {'ability' : 5, 'ATK' : 20, 'CD_speedup' : 2,'coin_add' : 10,
                    'critical' : 2, 'damage_limited' : 50, 'EXP_add' : 10, 'fire_damage' : 10,
                    'health_drain' : 1, 'health_for_damage' : 10, 'health_regeneration' : 0.2, 'HP' : 20,
                      'ice' : 0.5, 'partner' : 20, 'revive' : 1, 'sale' : 5}

#能力和技能參數(實際)
current_ability_parameter = {'ATK' : 0, 'HP' : 0, 'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#能力和技能參數(實際)預設值
current_ability_parameter_default = {'ATK' : 0, 'HP' : 0, 'fireball' : 0, 'heal' : 0, 'freeze' : 0, 'self_hurt' : 0}

#能力和技能參數(下一階)
ability_parameter = {'ATK' : 0, 'HP' : 0, 'fireball' : 10, 'heal' : 20, 'freeze' : 1, 'self_hurt' : 5000}

#能力和技能參數(下一階)預設值
ability_parameter_default = {'ATK' : 0, 'HP' : 0, 'fireball' : 10, 'heal' : 20, 'freeze' : 1, 'self_hurt' : 5000}

#敵人類型(0 : 小怪，1 : BOSS)
enemy_type = {'type' : 0}

#敵人數值(最大血量、攻擊傷害、金錢掉落量、經驗值掉落量、攻擊間隔、實際血量、當前敵人序數、是否燃燒)
enemy = {'max_health' : 10, 'attack_damage' : 1, 'reward_money' : 4, "reward_EXP" : 1, 'attack_interval' : 3, 'current_health' : 10, 'number' : 1, 'fire' : 0}

#敵人數值預設值
enemy_default = {'max_health' : 10, 'attack_damage' : 1, 'reward_money' : 4, "reward_EXP" : 1, 'attack_interval' : 3, 'current_health' : 10,'number' : 1, 'fire' : 0}

damage = {'damage': 0 , 'time' : 0,'combo' : 0}
damage_default = {'damage': 0 , 'time' : 0,'combo' : 0}

#當前周目
round = 1

#當前周目預設值
round_default = 1

#敵人數值加強倍率
enemy_strength_increase = 1.09

#金錢及經驗值掉落倍率
reward_coin_increase = 1.07
reward_EXP_increase = 1.06

#當前場景(主場景、子場景)
scene = {'main' : 0, 'sub' : 0}

#存檔存取對象
saving = {'save' : 0}

#檔案是否空白
no_data = {'save_1' : 0,'save_2' : 0,'save_3' : 0}

#檔案時間紀錄
saving_1_time = {'year': 0,'month': 0,'day': 0,'hour': 0,'minute': 0,'second': 0}
saving_2_time = {'year': 0,'month': 0,'day': 0,'hour': 0,'minute': 0,'second': 0}
saving_3_time = {'year': 0,'month': 0,'day': 0,'hour': 0,'minute': 0,'second': 0}


#遊戲時間偵測
enemy_last_attack_time = time.time()
game_time = time.time()
damage_time = time.time()

#載入圖片素材
#範例:圖片_img = pygame.image.load(os.path.join('資料夾路徑', '圖片.png')).convert()
ability_attack_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_attack_upgrade.png'))
ability_health_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_health_upgrade.png'))
ability_fireball_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_fireball_upgrade.png'))
ability_heal_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_heal_upgrade.png'))
ability_freeze_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_freeze_upgrade.png'))
ability_self_hurt_upgrade_img = pygame.image.load(os.path.join('item','ability', 'ability_self_hurt_upgrade.png'))
background_main_img = pygame.image.load(os.path.join('item','background', 'background_main.png'))
background_setting_img = pygame.image.load(os.path.join('item','background', 'background_setting.png'))
background_saving_img = pygame.image.load(os.path.join('item','background', 'background_saving.png'))
background_endowment_img = pygame.image.load(os.path.join('item','background', 'background_endowment.png'))
background_game_img = pygame.image.load(os.path.join('item','background', 'background_game.png'))
background_complete_img = pygame.image.load(os.path.join('item','background', 'background_complete.png'))
button_back_img = pygame.image.load(os.path.join('item','button', 'button_back.png'))
button_leave_img = pygame.image.load(os.path.join('item','button', 'button_leave.png'))
button_minus_img = pygame.image.load(os.path.join('item','button', 'button_minus.png'))
button_no_upgrade_img = pygame.image.load(os.path.join('item','button', 'button_no_upgrade.png'))
button_option_img = pygame.image.load(os.path.join('item','button', 'button_option.png'))
button_plus_img = pygame.image.load(os.path.join('item','button', 'button_plus.png'))
button_start_img = pygame.image.load(os.path.join('item','button', 'button_start.png'))
button_upgrade_img = pygame.image.load(os.path.join('item','button', 'button_upgrade.png'))
button_save_img = pygame.image.load(os.path.join('item','button', 'button_save.png'))
enemy_boss_cuber_img = pygame.image.load(os.path.join('item','enemy','boss', 'enemy_boss_cuber.png'))
enemy_boss_demon_img = pygame.image.load(os.path.join('item','enemy','boss', 'enemy_boss_demon.png'))
enemy_boss_destroyer_img = pygame.image.load(os.path.join('item','enemy','boss', 'enemy_boss_destroyer.png'))
enemy_boss_observer_img = pygame.image.load(os.path.join('item','enemy','boss', 'enemy_boss_observer.png'))
enemy_normal_1_img = pygame.image.load(os.path.join('item','enemy','normal', 'enemy_normal_1.png'))
partner_lv1_img = pygame.image.load(os.path.join('item','partner', 'partner_lv1.png'))
partner_lv2_img = pygame.image.load(os.path.join('item','partner', 'partner_lv2.png'))
partner_lv3_img = pygame.image.load(os.path.join('item','partner', 'partner_lv3.png'))
partner_lv4_img = pygame.image.load(os.path.join('item','partner', 'partner_lv4.png'))
partner_lv5_img = pygame.image.load(os.path.join('item','partner', 'partner_lv5.png'))
partner_lv6_img = pygame.image.load(os.path.join('item','partner', 'partner_lv6.png'))
picture_ATK_img = pygame.image.load(os.path.join('item','picture', 'picture_ATK.png'))
picture_HP_img = pygame.image.load(os.path.join('item','picture', 'picture_HP.png'))
picture_coin_img = pygame.image.load(os.path.join('item','picture', 'picture_coin.png'))
picture_EXP_img = pygame.image.load(os.path.join('item','picture', 'picture_EXP.png'))
skill_ability_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_ability_upgrade.png'))
skill_ATK_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_ATK_upgrade.png'))
skill_CD_speedup_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_CD_speedup_upgrade.png'))
skill_coin_add_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_coin_add_upgrade.png'))
skill_critical_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_critical_upgrade.png'))
skill_damage_limited_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_damage_limited_upgrade.png'))
skill_EXP_add_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_EXP_add_upgrade.png'))
skill_fire_damage_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_fire_damage_upgrade.png'))
skill_health_drain_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_health_drain_upgrade.png'))
skill_health_for_damage_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_health_for_damage_upgrade.png'))
skill_health_regeneration_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_health_regeneration_upgrade.png'))
skill_HP_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_HP_upgrade.png'))
skill_ice_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_ice_upgrade.png'))
skill_partner_stronger_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_partner_stronger_upgrade.png'))
skill_revive_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_revive_upgrade.png'))
skill_sale_upgrade_img = pygame.image.load(os.path.join('item','skill', 'skill_sale_upgrade.png'))
skill_select_img = pygame.image.load(os.path.join('item','skill', 'skill_select.png'))

#調整圖片大小
#範例:圖片_img = pygame.transform.scale(圖片_img, (長, 寬))
ability_attack_upgrade_img = pygame.transform.scale(ability_attack_upgrade_img,(120,120))
ability_health_upgrade_img = pygame.transform.scale(ability_health_upgrade_img,(120,120))
ability_fireball_upgrade_img = pygame.transform.scale(ability_fireball_upgrade_img,(120,120))
ability_heal_upgrade_img = pygame.transform.scale(ability_heal_upgrade_img,(120,120))
ability_freeze_upgrade_img = pygame.transform.scale(ability_freeze_upgrade_img,(120,120))
ability_self_hurt_upgrade_img = pygame.transform.scale(ability_self_hurt_upgrade_img,(120,120))
background_complete_img = pygame.transform.scale(background_complete_img,(1920,1080))
background_endowment_img = pygame.transform.scale(background_endowment_img,(1920,1080))
background_game_img = pygame.transform.scale(background_game_img,(1920,1080))
background_main_img = pygame.transform.scale(background_main_img,(1920,1080))
background_saving_img = pygame.transform.scale(background_saving_img,(1920,1080))
background_setting_img = pygame.transform.scale(background_setting_img,(1920,1080))
button_back_img = pygame.transform.scale(button_back_img,(240,98))
button_leave_img = pygame.transform.scale(button_leave_img,(300,98))
button_minus_img = pygame.transform.scale(button_minus_img,(92,32))
button_no_upgrade_img = pygame.transform.scale(button_no_upgrade_img,(330,98))
button_option_img = pygame.transform.scale(button_option_img,(300,98))
button_plus_img = pygame.transform.scale(button_plus_img,(92,92))
button_start_img = pygame.transform.scale(button_start_img,(300,98))
button_upgrade_img = pygame.transform.scale(button_upgrade_img,(330,98))
button_save_img = pygame.transform.scale(button_save_img,(435,641))
button_no_upgrade_game_img = pygame.transform.scale(button_no_upgrade_img,(165,49))
button_upgrade_game_img = pygame.transform.scale(button_upgrade_img,(165,49))
enemy_boss_cuber_img = pygame.transform.scale(enemy_boss_cuber_img,(400,400))
enemy_boss_demon_img = pygame.transform.scale(enemy_boss_demon_img,(400,400))
enemy_boss_destroyer_img = pygame.transform.scale(enemy_boss_destroyer_img,(400,450))
enemy_boss_observer_img = pygame.transform.scale(enemy_boss_observer_img,(400,450))
enemy_normal_1_img = pygame.transform.scale(enemy_normal_1_img,(240,240))
partner_lv1_img = pygame.transform.scale(partner_lv1_img,(120,120))
partner_lv2_img = pygame.transform.scale(partner_lv2_img,(120,120))
partner_lv3_img = pygame.transform.scale(partner_lv3_img,(120,120))
partner_lv4_img = pygame.transform.scale(partner_lv4_img,(120,120))
partner_lv5_img = pygame.transform.scale(partner_lv5_img,(120,120))
partner_lv6_img = pygame.transform.scale(partner_lv6_img,(120,120))
picture_ATK_img = pygame.transform.scale(picture_ATK_img,(79,79))
picture_HP_img = pygame.transform.scale(picture_HP_img,(64,75))
picture_coin_img = pygame.transform.scale(picture_coin_img,(53,53))
picture_EXP_img = pygame.transform.scale(picture_EXP_img,(34,79))
skill_ability_upgrade_select_img = pygame.transform.scale(skill_ability_upgrade_img,(240,240))
skill_ATK_upgrade_select_img = pygame.transform.scale(skill_ATK_upgrade_img,(240,240))
skill_CD_speedup_upgrade_select_img = pygame.transform.scale(skill_CD_speedup_upgrade_img,(240,240))
skill_coin_add_upgrade_select_img = pygame.transform.scale(skill_coin_add_upgrade_img,(240,240))
skill_critical_upgrade_select_img = pygame.transform.scale(skill_critical_upgrade_img,(240,240))
skill_damage_limited_upgrade_select_img = pygame.transform.scale(skill_damage_limited_upgrade_img,(240,240))
skill_EXP_add_upgrade_select_img = pygame.transform.scale(skill_EXP_add_upgrade_img,(240,240))
skill_fire_damage_upgrade_select_img = pygame.transform.scale(skill_fire_damage_upgrade_img,(240,240))
skill_health_drain_upgrade_select_img = pygame.transform.scale(skill_health_drain_upgrade_img,(240,240))
skill_health_for_damage_upgrade_select_img = pygame.transform.scale(skill_health_for_damage_upgrade_img,(240,240))
skill_health_regeneration_upgrade_select_img = pygame.transform.scale(skill_health_regeneration_upgrade_img,(240,240))
skill_HP_upgrade_select_img = pygame.transform.scale(skill_HP_upgrade_img,(240,240))
skill_ice_upgrade_select_img = pygame.transform.scale(skill_ice_upgrade_img,(240,240))
skill_partner_stronger_upgrade_select_img = pygame.transform.scale(skill_partner_stronger_upgrade_img,(240,240))
skill_revive_upgrade_select_img = pygame.transform.scale(skill_revive_upgrade_img,(240,240))
skill_sale_upgrade_select_img = pygame.transform.scale(skill_sale_upgrade_img,(240,240))
skill_ability_upgrade_img = pygame.transform.scale(skill_ability_upgrade_img,(120,120))
skill_ATK_upgrade_img = pygame.transform.scale(skill_ATK_upgrade_img,(120,120))
skill_CD_speedup_upgrade_img = pygame.transform.scale(skill_CD_speedup_upgrade_img,(120,120))
skill_coin_add_upgrade_img = pygame.transform.scale(skill_coin_add_upgrade_img,(120,120))
skill_critical_upgrade_img = pygame.transform.scale(skill_critical_upgrade_img,(120,120))
skill_damage_limited_upgrade_img = pygame.transform.scale(skill_damage_limited_upgrade_img,(120,120))
skill_EXP_add_upgrade_img = pygame.transform.scale(skill_EXP_add_upgrade_img,(120,120))
skill_fire_damage_upgrade_img = pygame.transform.scale(skill_fire_damage_upgrade_img,(120,120))
skill_health_drain_upgrade_img = pygame.transform.scale(skill_health_drain_upgrade_img,(120,120))
skill_health_for_damage_upgrade_img = pygame.transform.scale(skill_health_for_damage_upgrade_img,(120,120))
skill_health_regeneration_upgrade_img = pygame.transform.scale(skill_health_regeneration_upgrade_img,(120,120))
skill_HP_upgrade_img = pygame.transform.scale(skill_HP_upgrade_img,(120,120))
skill_ice_upgrade_img = pygame.transform.scale(skill_ice_upgrade_img,(120,120))
skill_partner_stronger_upgrade_img = pygame.transform.scale(skill_partner_stronger_upgrade_img,(120,120))
skill_revive_upgrade_img = pygame.transform.scale(skill_revive_upgrade_img,(120,120))
skill_sale_upgrade_img = pygame.transform.scale(skill_sale_upgrade_img,(120,120))
skill_select_img = pygame.transform.scale(skill_select_img,(140,140))
#圖片位置設定
#範例:圖片_img_rect = 圖片_img.get_rect(center=(x, y))
ability_attack_upgrade_img_rect = ability_attack_upgrade_img.get_rect(center=(1350 , 60))
ability_health_upgrade_img_rect = ability_health_upgrade_img.get_rect(center=(1350 , 241))
ability_fireball_upgrade_img_rect = ability_fireball_upgrade_img.get_rect(center=(1350 , 421))
ability_heal_upgrade_img_rect = ability_heal_upgrade_img.get_rect(center=(1350 , 600))
ability_freeze_upgrade_img_rect = ability_freeze_upgrade_img.get_rect(center=(1350 , 780))
ability_self_hurt_upgrade_img_rect = ability_self_hurt_upgrade_img.get_rect(center=(1350 , 960))
background_main_img_rect = background_main_img.get_rect(center=(window_width/2 , window_height/2))
background_setting_img_rect = background_setting_img.get_rect(center=(window_width/2 , window_height/2))
background_saving_img_rect = background_saving_img.get_rect(center=(window_width/2 , window_height/2))
background_endowment_img_rect = background_endowment_img.get_rect(center=(window_width/2 , window_height/2))
background_game_img_rect = background_game_img.get_rect(center=(window_width/2 , window_height/2))
background_complete_img_rect = background_complete_img.get_rect(center=(window_width/2 , window_height/2))
button_leave_img_rect = button_leave_img.get_rect(center=(window_width*3/4 , window_height*5/6))
button_option_img_rect = button_option_img.get_rect(center=(window_width*3/4 , window_height*2/3))
button_start_img_rect = button_start_img.get_rect(center=(window_width*3/4 , window_height/2))
button_start_endowment_img_rect = button_start_img.get_rect(center=(window_width*9/10 , window_height/16))
button_back_img_rect = button_back_img.get_rect(center=(window_width/10 , window_height/16))
button_back_img_complete_rect = button_back_img.get_rect(center=(window_width*10/11 , window_height*15/16))
button_upgrade_img_endowment_rect = button_upgrade_img.get_rect(center=(1451 , 1020))
button_upgrade_img_ability_1_rect = button_upgrade_img.get_rect(center=(1459 , 173))
button_upgrade_img_ability_2_rect = button_upgrade_img.get_rect(center=(1459 , 353))
button_upgrade_img_ability_3_rect = button_upgrade_img.get_rect(center=(1459 , 533))
button_upgrade_img_ability_4_rect = button_upgrade_img.get_rect(center=(1459 , 713))
button_upgrade_img_ability_5_rect = button_upgrade_img.get_rect(center=(1459 , 893))
button_upgrade_img_ability_6_rect = button_upgrade_img.get_rect(center=(1459 , 1073))
button_upgrade_img_partner_1_rect = button_upgrade_img.get_rect(center=(165 , 173))
button_upgrade_img_partner_2_rect = button_upgrade_img.get_rect(center=(165 , 353))
button_upgrade_img_partner_3_rect = button_upgrade_img.get_rect(center=(165 , 533))
button_upgrade_img_partner_4_rect = button_upgrade_img.get_rect(center=(165 , 713))
button_upgrade_img_partner_5_rect = button_upgrade_img.get_rect(center=(165 , 893))
button_upgrade_img_partner_6_rect = button_upgrade_img.get_rect(center=(165 , 1073))
button_save_1_img_rect = button_save_img.get_rect(center=(window_width/4-6, 636))
button_save_2_img_rect = button_save_img.get_rect(center=(window_width/2, 636))
button_save_3_img_rect = button_save_img.get_rect(center=(window_width*3/4+6, 636))
button_minus_master_img_rect = button_minus_img.get_rect(center=(1035 , 446))
button_minus_music_img_rect = button_minus_img.get_rect(center=(1035 , 581))
button_minus_FX_img_rect = button_minus_img.get_rect(center=(1035 , 731))
button_plus_master_img_rect = button_plus_img.get_rect(center=(1725 , 446))
button_plus_music_img_rect = button_plus_img.get_rect(center=(1725 , 581))
button_plus_FX_img_rect = button_plus_img.get_rect(center=(1725 , 731))
enemy_boss_cuber_img_rect = enemy_boss_cuber_img.get_rect(center=(window_width/2 , window_height/3))
enemy_boss_demon_img_rect = enemy_boss_demon_img.get_rect(center=(window_width/2 , window_height/3))
enemy_boss_destroyer_img_rect = enemy_boss_destroyer_img.get_rect(center=(window_width/2 , window_height/3))
enemy_boss_observer_img_rect = enemy_boss_observer_img.get_rect(center=(window_width/2 , window_height/3))
enemy_normal_1_img_rect = enemy_normal_1_img.get_rect(center=(window_width/2 , window_height/3))
partner_lv1_img_rect = partner_lv1_img.get_rect(center=(60 , 60))
partner_lv2_img_rect = partner_lv2_img.get_rect(center=(60 , 241))
partner_lv3_img_rect = partner_lv3_img.get_rect(center=(60 , 421))
partner_lv4_img_rect = partner_lv4_img.get_rect(center=(60 , 600))
partner_lv5_img_rect = partner_lv5_img.get_rect(center=(60 , 780))
partner_lv6_img_rect = partner_lv6_img.get_rect(center=(60 , 960))
picture_ATK_img_rect = picture_ATK_img.get_rect(center=(690 , 780))
picture_HP_img_rect = picture_HP_img.get_rect(center=(1020 , 780))
picture_coin_img_rect = picture_coin_img.get_rect(center=(690 , 960))
picture_EXP_img_rect = picture_EXP_img.get_rect(center=(1020 , 960))
picture_EXP_img_endowment_rect = picture_EXP_img.get_rect(center=(1550 , 170))
skill_ATK_upgrade_img_rect = skill_ATK_upgrade_img.get_rect(center=(120 , 240))
skill_critical_upgrade_img_rect = skill_critical_upgrade_img.get_rect(center=(360 , 240))
skill_fire_damage_upgrade_img_rect = skill_fire_damage_upgrade_img.get_rect(center=(600 , 240))
skill_ice_upgrade_img_rect = skill_ice_upgrade_img.get_rect(center=(840 , 240))
skill_HP_upgrade_img_rect = skill_HP_upgrade_img.get_rect(center=(120 , 480))
skill_health_drain_upgrade_img_rect = skill_health_drain_upgrade_img.get_rect(center=(360 , 480))
skill_EXP_add_upgrade_img_rect = skill_EXP_add_upgrade_img.get_rect(center=(600 , 480))
skill_health_for_damage_upgrade_img_rect = skill_health_for_damage_upgrade_img.get_rect(center=(840 , 480))
skill_health_regeneration_upgrade_img_rect = skill_health_regeneration_upgrade_img.get_rect(center=(120 , 720))
skill_coin_add_upgrade_img_rect = skill_coin_add_upgrade_img.get_rect(center=(360 , 720))
skill_partner_stronger_upgrade_img_rect = skill_partner_stronger_upgrade_img.get_rect(center=(600 , 725))
skill_ability_upgrade_img_rect = skill_ability_upgrade_img.get_rect(center=(840 , 720))
skill_revive_upgrade_img_rect = skill_revive_upgrade_img.get_rect(center=(120 , 960))
skill_sale_upgrade_img_rect = skill_sale_upgrade_img.get_rect(center=(360 , 960))
skill_CD_speedup_upgrade_img_rect = skill_CD_speedup_upgrade_img.get_rect(center=(600 , 960))
skill_damage_limited_upgrade_img_rect = skill_damage_limited_upgrade_img.get_rect(center=(840 , 960))
skill_select_rect = skill_ability_upgrade_select_img.get_rect(center=(1155,300))

#載入音樂素材
#範例:音樂_music = pygame.mixer.Sound(os.path.join('資料夾路徑','音樂.mp3'))
game_main_music = pygame.mixer.Sound(os.path.join('music', 'game_main.MP3'))
game_normal_music = pygame.mixer.Sound(os.path.join('music', 'game_normal.MP3'))
game_boss_music = pygame.mixer.Sound(os.path.join('music', 'game_boss.MP3'))

#音效素材載入
#範例:音效_sound = pygame.mixer.Sound(os.path.join("資料夾路徑", "音效.mp3"))
game_button_sound = pygame.mixer.Sound(os.path.join('music', 'game_button.MP3'))
game_no_button_sound = pygame.mixer.Sound(os.path.join('music', 'game_no_button.MP3'))
game_player_attack_sound = pygame.mixer.Sound(os.path.join('music', 'game_player_attack.MP3'))
game_player_damaged_sound = pygame.mixer.Sound(os.path.join('music', 'game_player_damaged.MP3'))
game_enemy_death_sound = pygame.mixer.Sound(os.path.join('music', 'game_enemy_death.MP3'))


#音量大小設定
#範例:音樂_music.set_volume(0~1)
game_main_music.set_volume(1)
game_normal_music.set_volume(1)
game_boss_music.set_volume(1)
game_button_sound.set_volume(1)
game_no_button_sound.set_volume(1)
game_player_attack_sound.set_volume(1)
game_player_damaged_sound.set_volume(1)
game_enemy_death_sound.set_volume(1)


def update(): #遊戲主迴圈
    if scene['main'] == "main": #主場景 : 主畫面
        main_item_display()
        main_music_display()
        main_motion_detect()

    elif scene['main'] == "option": #主場景 : 設定畫面
        option_item_display()
        option_music_display()
        option_motion_detect()

    elif scene['main'] == "game": #主場景 : 遊戲相關畫面
        
        if scene['sub'] == "saving": #子場景 : 存檔畫面
            game_1_item_display()
            game_1_music_display()
            game_1_motion_detect()
        elif scene['sub'] == "endowment": #子場景 : 天賦畫面
            game_2_item_display()
            game_2_music_display()
            game_2_motion_detect()
        elif scene['sub'] == "gaming": #子場景 : 遊戲畫面
            game_parameter_caculate_keep()
            game_parameter_detect()
            game_3_item_display()
            game_3_music_display()
            game_3_motion_detect()
        elif scene['sub'] == "complete":#子場景 : 通關畫面
            game_4_item_display()
            game_4_music_display()
            game_4_motion_detect()
        elif scene['sub'] == "game_over":#子場景 : 死亡畫面
            game_over_item_display()
            game_over_music_display()
            game_over_motion_detect()
    
#執行動作的函式
def main_item_display(): #主畫面物件顯示
    screen.blit(background_main_img, background_main_img_rect)
    screen.blit(button_start_img, button_start_img_rect)
    screen.blit(button_option_img, button_option_img_rect)
    screen.blit(button_leave_img, button_leave_img_rect)

def main_music_display(): #主畫面聲音播放
    if not pygame.mixer.get_busy():
        game_main_music.play(-1)

def main_motion_detect(): #主畫面動作偵測

    for event in pygame.event.get(): #獲取pygame事件

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #按下滑鼠左鍵

            if button_start_img_rect.collidepoint(event.pos): #按下start按鈕
                scene['main'] = "game" #主場景切換至"遊戲相關畫面"
                scene['sub'] = "saving" #子場景切換至"存檔畫面"
                game_button_sound.play(0) #播放按鍵聲
                saving_date_load()
            
            elif button_option_img_rect.collidepoint(event.pos): 
                scene['main'] = "option" #主場景切換至"設定畫面"
                game_button_sound.play(0) #播放按鍵聲
            
            elif button_leave_img_rect.collidepoint(event.pos): 
                game_button_sound.play(0) #播放按鍵聲
                pygame.quit() #關閉pygame
                exit() #關閉程式

def option_item_display(): #設定畫面物件顯示s

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 100) #載入字體 & 大小

    master_volume_text = font.render(str(settings['master_volume']) ,True, (255,255,255), None)
    music_volume_text = font.render(str(settings['music_volume']) ,True, (255,255,255), None)
    FX_volume_text = font.render(str(settings['FX_volume']) ,True, (255,255,255), None)

    screen.blit(background_setting_img, background_setting_img_rect)
    screen.blit(button_back_img, button_back_img_rect)
    screen.blit(button_minus_img, button_minus_master_img_rect)
    screen.blit(button_minus_img, button_minus_music_img_rect)
    screen.blit(button_minus_img, button_minus_FX_img_rect)
    screen.blit(button_plus_img, button_plus_master_img_rect)
    screen.blit(button_plus_img, button_plus_music_img_rect)
    screen.blit(button_plus_img, button_plus_FX_img_rect)

    screen.blit(master_volume_text , (window_width*11/16, 366))
    screen.blit(music_volume_text , (window_width*11/16, 501))
    screen.blit(FX_volume_text , (window_width*11/16, 651))

def option_music_display(): #設定畫面聲音播放
    if not pygame.mixer.get_busy():
        game_main_music.play(-1)
    
def option_motion_detect(): #設定畫面動作偵測

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if button_back_img_rect.collidepoint(event.pos):
                scene['main'] = "main"
                game_button_sound.play(0)

            elif button_minus_master_img_rect.collidepoint(event.pos):
                if settings['master_volume'] > 0:
                    settings['master_volume'] -= 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)
            
            elif button_plus_master_img_rect.collidepoint(event.pos):
                if settings['master_volume'] < 10:
                    settings['master_volume'] += 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            elif button_minus_music_img_rect.collidepoint(event.pos):
                if settings['music_volume'] > 0:
                    settings['music_volume'] -= 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)
            
            elif button_plus_music_img_rect.collidepoint(event.pos):
                if settings['music_volume'] < 10:
                    settings['music_volume'] += 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            elif button_minus_FX_img_rect.collidepoint(event.pos):
                if settings['FX_volume'] > 0:
                    settings['FX_volume'] -= 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)
            
            elif button_plus_FX_img_rect.collidepoint(event.pos):
                if settings['FX_volume'] < 10:
                    settings['FX_volume'] += 1
                    game_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)
            
            #聲音音量設定
            game_main_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10)) 
            game_normal_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10))
            game_boss_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10))
            game_button_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
            game_no_button_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
            game_player_attack_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
            game_player_damaged_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
            game_enemy_death_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))

            volume_write()

def game_1_item_display(): #存檔畫面物件顯示
        
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 100)
    
    save_1_text = font.render("save 1", True, (255,255,255), None)
    save_2_text = font.render("save 2", True, (255,255,255), None)
    save_3_text = font.render("save 3", True, (255,255,255), None)
    
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 50)
    
    save_1_date_text = font.render(f"{saving_1_time['year']} / {saving_1_time['month']} / {saving_1_time['day']}", True, (255,255,255), None)
    save_2_date_text = font.render(f"{saving_2_time['year']} / {saving_2_time['month']} / {saving_2_time['day']}", True, (255,255,255), None)
    save_3_date_text = font.render(f"{saving_3_time['year']} / {saving_3_time['month']} / {saving_3_time['day']}", True, (255,255,255), None)
    save_1_time_text = font.render(f"{saving_1_time['hour']} : {saving_1_time['minute']} : {saving_1_time['second']}", True, (255,255,255), None)
    save_2_time_text = font.render(f"{saving_2_time['hour']} : {saving_2_time['minute']} : {saving_2_time['second']}", True, (255,255,255), None)
    save_3_time_text = font.render(f"{saving_3_time['hour']} : {saving_3_time['minute']} : {saving_3_time['second']}", True, (255,255,255), None)
    no_data_text = font.render("NO DATA ", True, (255,0,0), None)
    
    screen.blit(background_saving_img, background_saving_img_rect)
    screen.blit(button_back_img, button_back_img_rect)
    screen.blit(button_save_img, button_save_1_img_rect)
    screen.blit(button_save_img, button_save_2_img_rect)
    screen.blit(button_save_img, button_save_3_img_rect)

    screen.blit(save_1_text, (window_width/4-170, 366))
    screen.blit(save_2_text, (window_width/2-180, 366))
    screen.blit(save_3_text, (window_width*3/4-165, 366))
    
    if no_data['save_1'] == 0:
        screen.blit(save_1_date_text, (window_width/4-170, 666))
        screen.blit(save_1_time_text, (window_width/4-170, 766))
    else:
        screen.blit(no_data_text, (window_width/4-170, 666))
        
    if no_data['save_2'] == 0:
        screen.blit(save_2_date_text, (window_width/2-180, 666))
        screen.blit(save_2_time_text, (window_width/2-180, 766))
    else:
        screen.blit(no_data_text, (window_width/2-180, 666))
        
    if no_data['save_3'] == 0:
        screen.blit(save_3_date_text, (window_width*3/4-165, 666))
        screen.blit(save_3_time_text, (window_width*3/4-165, 766))
    else:
        screen.blit(no_data_text, (window_width*3/4-165, 666))

def game_1_music_display(): #存檔畫面聲音播放
    if not pygame.mixer.get_busy():
        game_main_music.play(-1)
    
def game_1_motion_detect(): #存檔畫面動作偵測

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if button_back_img_rect.collidepoint(event.pos):
                scene['main'] = "main"
                scene['sub'] = -1
                game_button_sound.play(0)

            if button_save_1_img_rect.collidepoint(event.pos):
                saving_load_1()
                saving['save'] = 1
                scene['sub'] = "endowment"
                endowment_select['select'] = 1
                game_button_sound.play(0)

            elif button_save_2_img_rect.collidepoint(event.pos):
                saving_load_2()
                saving['save'] = 2
                scene['sub'] = "endowment"
                endowment_select['select'] = 1
                game_button_sound.play(0)

            elif button_save_3_img_rect.collidepoint(event.pos):
                saving_load_3()
                saving['save'] = 3
                scene['sub'] = "endowment"
                endowment_select['select'] = 1
                game_button_sound.play(0)
  
def game_2_item_display(): #天賦畫面物件顯示

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 50)

    skill_ability_text = font.render('skill enhancement', True, (255,255,255), None)
    skill_ATK_text = font.render('attack increase', True, (255,255,255), None)
    skill_CD_speedup_text = font.render('cooldown reduce', True, (255,255,255), None)
    skill_coin_add_text = font.render('coin gain increase', True, (255,255,255), None)
    skill_critical_text = font.render('critical hit', True, (255,255,255), None)
    skill_damage_limited_text = font.render('damage limite', True, (255,255,255), None)
    skill_EXP_add_text = font.render('EXP gain increase', True, (255,255,255), None)
    skill_fire_damage_text = font.render('flame', True, (255,255,255), None)
    skill_health_drain_text = font.render('life steal', True, (255,255,255), None)
    skill_health_for_damage_text = font.render('not give up', True, (255,255,255), None)
    skill_health_regeneration_text = font.render('health regeneration', True, (255,255,255), None)
    skill_HP_text = font.render('health increase', True, (255,255,255), None)
    skill_ice_text = font.render('enemy freeze', True, (255,255,255), None)
    skill_partner_stronger_text = font.render('partner reinforce', True, (255,255,255), None)
    skill_revive_text = font.render('revive', True, (255,255,255), None)
    skill_sale_text = font.render('sale', True, (255,255,255), None)

    skill_ability_cost_text = font.render(str(endowment_cost['ability']), True, (255,100,255), None)
    skill_ATK_cost_text = font.render(str(endowment_cost['ATK']), True, (255,100,255), None)
    skill_CD_speedup_cost_text = font.render(str(endowment_cost['CD_speedup']), True, (255,100,255), None)
    skill_coin_add_cost_text = font.render(str(endowment_cost['coin_add']), True, (255,100,255), None)
    skill_critical_cost_text = font.render(str(endowment_cost['critical']), True, (255,100,255), None)
    skill_damage_limited_cost_text = font.render(str(endowment_cost['damage_limited']), True, (255,100,255), None)
    skill_EXP_add_cost_text = font.render(str(endowment_cost['EXP_add']), True, (255,100,255), None)
    skill_fire_damage_cost_text = font.render(str(endowment_cost['fire_damage']), True, (255,100,255), None)
    skill_health_drain_cost_text = font.render(str(endowment_cost['health_drain']), True, (255,100,255), None)
    skill_health_for_damage_cost_text = font.render(str(endowment_cost['health_for_damage']), True, (255,100,255), None)
    skill_health_regeneration_cost_text = font.render(str(endowment_cost['health_regeneration']), True, (255,100,255), None)
    skill_HP_cost_text = font.render(str(endowment_cost['HP']), True, (255,100,255), None)
    skill_ice_cost_text = font.render(str(endowment_cost['ice']), True, (255,100,255), None)
    skill_partner_stronger_cost_text = font.render(str(endowment_cost['partner']), True, (255,100,255), None)
    skill_revive_cost_text = font.render(str(endowment_cost['revive']), True, (255,100,255), None)
    skill_sale_cost_text = font.render(str(endowment_cost['sale']), True, (255,100,255), None)

    skill_ability_level_text = font.render(f"Lv {endowment_level['ability']}", True, (255,255,255), None)
    skill_ATK_level_text = font.render(f"Lv {endowment_level['ATK']}", True, (255,255,255), None)
    skill_CD_speedup_level_text = font.render(f"Lv {endowment_level['CD_speedup']}", True, (255,255,255), None)
    skill_coin_add_level_text = font.render(f"Lv {endowment_level['coin_add']}", True, (255,255,255), None)
    skill_critical_level_text = font.render(f"Lv {endowment_level['critical']}", True, (255,255,255), None)
    skill_damage_limited_level_text = font.render(f"Lv {endowment_level['damage_limited']}", True, (255,255,255), None)
    skill_EXP_add_level_text = font.render(f"Lv {endowment_level['EXP_add']}", True, (255,255,255), None)
    skill_fire_damage_level_text = font.render(f"Lv {endowment_level['fire_damage']}", True, (255,255,255), None)
    skill_health_drain_level_text = font.render(f"Lv {endowment_level['health_drain']}", True, (255,255,255), None)
    skill_health_for_damage_level_text = font.render(f"Lv {endowment_level['health_for_damage']}", True, (255,255,255), None)
    skill_health_regeneration_level_text = font.render(f"Lv {endowment_level['health_regeneration']}", True, (255,255,255), None)
    skill_HP_level_text = font.render(f"Lv {endowment_level['HP']}", True, (255,255,255), None)
    skill_ice_level_text = font.render(f"Lv {endowment_level['ice']}", True, (255,255,255), None)
    skill_partner_stronger_level_text = font.render(f"Lv {endowment_level['partner']}", True, (255,255,255), None)
    skill_revive_level_text = font.render(f"Lv {endowment_level['revive']}", True, (255,255,255), None)
    skill_sale_level_text = font.render(f"Lv {endowment_level['sale']}", True, (255,255,255), None)

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 70)

    EXP_text = font.render(f"{int(player_parameter['EXP'])}", True, (255,120,255), None)
    level_max_text = font.render("LEVEL MAX", True, (255,255,0), None)

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 25)

    skill_ability_caption_text = font.render(f"+{endowment_parameter['ability']}%({current_endowment_parameter['ability']}%) skill effect", True, (255,255,255), None)
    skill_ATK_caption_text = font.render(f"+{endowment_parameter['ATK']}%({current_endowment_parameter['ATK']}%) damage", True, (255,255,255), None)
    skill_CD_speedup_caption_text = font.render(f"cooldown time -{endowment_parameter['CD_speedup']}%({current_endowment_parameter['CD_speedup']}%)", True, (255,255,255), None)
    skill_coin_add_caption_text = font.render(f"coin will gain {endowment_parameter['coin_add']}%({current_endowment_parameter['coin_add']}%) more", True, (255,255,255), None)
    skill_critical_caption_text = font.render(f"{endowment_parameter['critical']}%({current_endowment_parameter['critical']}%) chance to critical hit", True, (255,255,255), None)
    skill_damage_limited_caption_text = font.render(f"damage suffered won't exceed {endowment_parameter['damage_limited']}%({current_endowment_parameter['damage_limited']}%) of max health", True, (255,255,255), None)
    skill_EXP_add_caption_text = font.render(f"EXP will gain {endowment_parameter['EXP_add']}%({current_endowment_parameter['EXP_add']}%) more", True, (255,255,255), None)
    skill_fire_damage_caption_text = font.render(f"deal {endowment_parameter['fire_damage']}%({current_endowment_parameter['fire_damage']}%) of damage in last 3 seconds", True, (255,255,255), None)
    skill_health_drain_caption_text = font.render(f"gain {endowment_parameter['health_drain']}%({current_endowment_parameter['health_drain']}%) damage for health", True, (255,255,255), None)
    skill_health_for_damage_caption_text = font.render(f"when health below 50%, +{endowment_parameter['health_for_damage']}%({current_endowment_parameter['health_for_damage']}%) of damage", True, (255,255,255), None)
    skill_health_regeneration_caption_text = font.render(f"heal {format(endowment_parameter['health_regeneration'], '.1f')}%({format(current_endowment_parameter['health_regeneration'], '.1f')}%) of max health in every second", True, (255,255,255), None)
    skill_HP_caption_text = font.render(f"+{endowment_parameter['HP']}%({current_endowment_parameter['HP']}%) health", True, (255,255,255), None)
    skill_ice_caption_text = font.render(f"enemy's attack interval +{format(endowment_parameter['ice'], '.1f')}({format(current_endowment_parameter['ice'], '.1f')}) second(s)", True, (255,255,255), None)
    skill_partner_stronger_caption_text = font.render(f"partner's damage +{endowment_parameter['partner']}%({current_endowment_parameter['partner']}%)", True, (255,255,255), None)
    skill_revive_caption_text = font.render(f"you can revive {endowment_parameter['revive']}({current_endowment_parameter['revive']}) time(s)", True, (255,255,255), None)
    skill_sale_caption_text = font.render(f"price -{endowment_parameter['sale']}%({current_endowment_parameter['sale']}%)", True, (255,255,255), None)

    screen.blit(background_endowment_img, background_endowment_img_rect)
    screen.blit(button_back_img, button_back_img_rect)
    screen.blit(button_start_img, button_start_endowment_img_rect)
    screen.blit(skill_ability_upgrade_img, skill_ability_upgrade_img_rect)
    screen.blit(skill_ATK_upgrade_img, skill_ATK_upgrade_img_rect)
    screen.blit(skill_CD_speedup_upgrade_img, skill_CD_speedup_upgrade_img_rect)
    screen.blit(skill_coin_add_upgrade_img, skill_coin_add_upgrade_img_rect)
    screen.blit(skill_critical_upgrade_img, skill_critical_upgrade_img_rect)
    screen.blit(skill_damage_limited_upgrade_img, skill_damage_limited_upgrade_img_rect)
    screen.blit(skill_EXP_add_upgrade_img, skill_EXP_add_upgrade_img_rect)
    screen.blit(skill_fire_damage_upgrade_img, skill_fire_damage_upgrade_img_rect)
    screen.blit(skill_health_drain_upgrade_img, skill_health_drain_upgrade_img_rect)
    screen.blit(skill_health_for_damage_upgrade_img, skill_health_for_damage_upgrade_img_rect)
    screen.blit(skill_health_regeneration_upgrade_img, skill_health_regeneration_upgrade_img_rect)
    screen.blit(skill_HP_upgrade_img, skill_HP_upgrade_img_rect) 
    screen.blit(skill_ice_upgrade_img, skill_ice_upgrade_img_rect)
    screen.blit(skill_partner_stronger_upgrade_img, skill_partner_stronger_upgrade_img_rect)
    screen.blit(skill_revive_upgrade_img, skill_revive_upgrade_img_rect)
    screen.blit(skill_sale_upgrade_img, skill_sale_upgrade_img_rect)
    screen.blit(picture_EXP_img, picture_EXP_img_endowment_rect)
    screen.blit(EXP_text, (1600,110))

    if endowment_select['select'] == 1:
        screen.blit(skill_ATK_upgrade_select_img, skill_select_rect)
        screen.blit(skill_ATK_text, (1300,230))
        screen.blit(skill_ATK_caption_text, (1050,430))
        screen.blit(skill_ATK_level_text,(1300, 330))
        screen.blit(skill_select_img, (50 , 170))
        if endowment_level['ATK'] < endowment_level_max['ATK']:
            screen.blit(skill_ATK_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['ATK']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 2:
        screen.blit(skill_critical_upgrade_select_img, skill_select_rect)
        screen.blit(skill_critical_text, (1300,230))
        screen.blit(skill_critical_caption_text, (1050,430))
        screen.blit(skill_critical_level_text,(1300, 330))
        screen.blit(skill_select_img, (290 , 170))
        if endowment_level['critical'] < endowment_level_max['critical']:
            screen.blit(skill_critical_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['critical']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   
    elif endowment_select['select'] == 3:
        screen.blit(skill_fire_damage_upgrade_select_img, skill_select_rect)
        screen.blit(skill_fire_damage_text, (1300,230))
        screen.blit(skill_fire_damage_caption_text, (1050,430))
        screen.blit(skill_fire_damage_level_text,(1300, 330))
        screen.blit(skill_select_img, (530 , 170))
        if endowment_level['fire_damage'] < endowment_level_max['fire_damage']:
            screen.blit(skill_fire_damage_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['fire_damage']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 4:
        screen.blit(skill_ice_upgrade_select_img, skill_select_rect)
        screen.blit(skill_ice_text, (1300,230))
        screen.blit(skill_ice_caption_text, (1050,430))
        screen.blit(skill_ice_level_text,(1300, 330))
        screen.blit(skill_select_img, (770 , 170))
        if endowment_level['ice'] < endowment_level_max['ice']:
            screen.blit(skill_ice_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['ice']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   
    elif endowment_select['select'] == 5:
        screen.blit(skill_HP_upgrade_select_img, skill_select_rect)
        screen.blit(skill_HP_text, (1300,230))
        screen.blit(skill_HP_caption_text, (1050,430))
        screen.blit(skill_HP_level_text,(1300, 330))
        screen.blit(skill_select_img, (50 , 410))
        if endowment_level['HP'] < endowment_level_max['HP']:
            screen.blit(skill_HP_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['HP']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 6:
        screen.blit(skill_health_drain_upgrade_select_img, skill_select_rect)
        screen.blit(skill_health_drain_text, (1300,230))
        screen.blit(skill_health_drain_caption_text, (1050,430))
        screen.blit(skill_health_drain_level_text,(1300, 330))
        screen.blit(skill_select_img, (290 , 410))
        if endowment_level['health_drain'] < endowment_level_max['health_drain']:
            screen.blit(skill_health_drain_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['health_drain']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 7:
        screen.blit(skill_EXP_add_upgrade_select_img, skill_select_rect)
        screen.blit(skill_EXP_add_text, (1300,230))
        screen.blit(skill_EXP_add_caption_text, (1050,430))
        screen.blit(skill_EXP_add_level_text,(1300, 330))
        screen.blit(skill_select_img, (530 , 410))
        if endowment_level['EXP_add'] < endowment_level_max['EXP_add']:
            screen.blit(skill_EXP_add_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['EXP_add']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 8:
        screen.blit(skill_health_for_damage_upgrade_select_img, skill_select_rect)
        screen.blit(skill_health_for_damage_text, (1300,230))
        screen.blit(skill_health_for_damage_caption_text, (1050,430))
        screen.blit(skill_health_for_damage_level_text,(1300, 330))
        screen.blit(skill_select_img, (770 , 410))
        if endowment_level['health_for_damage'] < endowment_level_max['health_for_damage']:
            screen.blit(skill_health_for_damage_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['health_for_damage']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 9:
        screen.blit(skill_health_regeneration_upgrade_select_img, skill_select_rect)
        screen.blit(skill_health_regeneration_text, (1300,230))
        screen.blit(skill_health_regeneration_caption_text, (1050,430))
        screen.blit(skill_health_regeneration_level_text,(1300, 330))
        screen.blit(skill_select_img, (50 , 650))
        if endowment_level['health_regeneration'] < endowment_level_max['health_regeneration']:
            screen.blit(skill_health_regeneration_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['health_regeneration']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 10:
        screen.blit(skill_coin_add_upgrade_select_img, skill_select_rect)
        screen.blit(skill_coin_add_text, (1300,230))
        screen.blit(skill_coin_add_caption_text, (1050,430))
        screen.blit(skill_coin_add_level_text,(1300, 330))
        screen.blit(skill_select_img, (290 , 650))
        if endowment_level['coin_add'] < endowment_level_max['coin_add']:
            screen.blit(skill_coin_add_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['coin_add']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 11:
        screen.blit(skill_partner_stronger_upgrade_select_img, skill_select_rect)
        screen.blit(skill_partner_stronger_text, (1300,230))
        screen.blit(skill_partner_stronger_caption_text, (1050,430))
        screen.blit(skill_partner_stronger_level_text,(1300, 330))
        screen.blit(skill_select_img, (530 , 650))
        if endowment_level['partner'] < endowment_level_max['partner']:
            screen.blit(skill_partner_stronger_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['partner']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 12:
        screen.blit(skill_ability_upgrade_select_img, skill_select_rect)
        screen.blit(skill_ability_text, (1300,230))
        screen.blit(skill_ability_caption_text, (1050,430))
        screen.blit(skill_ability_level_text,(1300, 330))
        screen.blit(skill_select_img, (770 , 650))
        if endowment_level['ability'] < endowment_level_max['ability']:
            screen.blit(skill_ability_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['ability']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 13:
        screen.blit(skill_revive_upgrade_select_img, skill_select_rect)
        screen.blit(skill_revive_text, (1300,230))
        screen.blit(skill_revive_caption_text, (1050,430))
        screen.blit(skill_revive_level_text,(1300, 330))
        screen.blit(skill_select_img, (50 , 890))
        if endowment_level['revive'] < endowment_level_max['revive']:
            screen.blit(skill_revive_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['revive']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 14:
        screen.blit(skill_sale_upgrade_select_img, skill_select_rect)
        screen.blit(skill_sale_text, (1300,230))
        screen.blit(skill_sale_caption_text, (1050,430))
        screen.blit(skill_sale_level_text,(1300, 330))
        screen.blit(skill_select_img, (290 , 890))
        if endowment_level['sale'] < endowment_level_max['sale']:
            screen.blit(skill_sale_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['sale']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 15:
        screen.blit(skill_CD_speedup_upgrade_select_img, skill_select_rect)
        screen.blit(skill_CD_speedup_text, (1300,230))
        screen.blit(skill_CD_speedup_caption_text, (1050,430))
        screen.blit(skill_CD_speedup_level_text,(1300, 330))
        screen.blit(skill_select_img, (530 , 890))
        if endowment_level['CD_speedup'] < endowment_level_max['CD_speedup']:
            screen.blit(skill_CD_speedup_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['CD_speedup']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

    elif endowment_select['select'] == 16:
        screen.blit(skill_damage_limited_upgrade_select_img, skill_select_rect)
        screen.blit(skill_damage_limited_text, (1300,230))
        screen.blit(skill_damage_limited_caption_text, (1050,430))
        screen.blit(skill_damage_limited_level_text,(1300, 330))
        screen.blit(skill_select_img, (770 , 890))
        if endowment_level['damage_limited'] < endowment_level_max['damage_limited']:
            screen.blit(skill_damage_limited_cost_text,(1300,900))
            if player_parameter['EXP'] < endowment_cost['damage_limited']:
                screen.blit(button_no_upgrade_img, button_upgrade_img_endowment_rect)
            else:
                screen.blit(button_upgrade_img, button_upgrade_img_endowment_rect)
        else:
            screen.blit(level_max_text, (1250,970))   

def game_2_music_display(): #天賦畫面聲音播放
    if not pygame.mixer.get_busy():
        game_main_music.play(-1) 

def game_2_motion_detect(): #天賦畫面動作偵測

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if button_back_img_rect.collidepoint(event.pos):
                scene['sub'] = "saving"
                game_button_sound.play(0)
                if saving['save'] == 1:
                    saving_write_1()
                    game_2_parameter_initialize()
                
                elif saving['save'] == 2:
                    saving_write_2()
                    game_2_parameter_initialize()
                    
                elif saving['save'] == 3:
                    saving_write_3()
                    game_2_parameter_initialize()
                    
                saving_date_load()

            if button_upgrade_img_endowment_rect.collidepoint(event.pos):
                game_button_sound.play(0)
                    
                if endowment_select['select'] == 1:

                    if player_parameter['EXP'] >= endowment_cost['ATK'] and endowment_level['ATK'] < endowment_level_max['ATK']:
                        player_parameter['EXP'] -= endowment_cost['ATK']
                        endowment_ATK_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 2:

                    if player_parameter['EXP'] >= endowment_cost['critical'] and endowment_level['critical'] < endowment_level_max['critical']:
                        player_parameter['EXP'] -= endowment_cost['critical']
                        endowment_critical_upgrade()
                    else:
                        game_no_button_sound.play(0)
                
                if endowment_select['select'] == 3:

                    if player_parameter['EXP'] >= endowment_cost['fire_damage'] and endowment_level['fire_damage'] < endowment_level_max['fire_damage']:
                        player_parameter['EXP'] -= endowment_cost['fire_damage']
                        endowment_fire_damage_upgrade()
                    else:
                        game_no_button_sound.play(0)
                
                if endowment_select['select'] == 4:

                    if player_parameter['EXP'] >= endowment_cost['ice'] and endowment_level['ice'] < endowment_level_max['ice']:
                        player_parameter['EXP'] -= endowment_cost['ice']
                        endowment_ice_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 5:

                    if player_parameter['EXP'] >= endowment_cost['HP'] and endowment_level['HP'] < endowment_level_max['HP']:
                        player_parameter['EXP'] -= endowment_cost['HP']
                        endowment_HP_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 6:

                    if player_parameter['EXP'] >= endowment_cost['health_drain'] and endowment_level['health_drain'] < endowment_level_max['health_drain']:
                        player_parameter['EXP'] -= endowment_cost['health_drain']
                        endowment_health_drain_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 7:

                    if player_parameter['EXP'] >= endowment_cost['EXP_add'] and endowment_level['EXP_add'] < endowment_level_max['EXP_add']:
                        player_parameter['EXP'] -= endowment_cost['EXP_add']
                        endowment_EXP_add_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 8:

                    if player_parameter['EXP'] >= endowment_cost['health_for_damage'] and endowment_level['health_for_damage'] < endowment_level_max['health_for_damage']:
                        player_parameter['EXP'] -= endowment_cost['health_for_damage']
                        endowment_health_for_damage_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 9:

                    if player_parameter['EXP'] >= endowment_cost['health_regeneration'] and endowment_level['health_regeneration'] < endowment_level_max['health_regeneration']:
                        player_parameter['EXP'] -= endowment_cost['health_regeneration']
                        endowment_health_regeneration_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 10:

                    if player_parameter['EXP'] >= endowment_cost['coin_add']and endowment_level['coin_add'] < endowment_level_max['coin_add']:
                        player_parameter['EXP'] -= endowment_cost['coin_add']
                        endowment_coin_add_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 11:

                    if player_parameter['EXP'] >= endowment_cost['partner'] and endowment_level['partner'] < endowment_level_max['partner']:
                        player_parameter['EXP'] -= endowment_cost['partner']
                        endowment_partner_upgrade()
                    else:
                        game_no_button_sound.play(0)
                        
                if endowment_select['select'] == 12:

                    if player_parameter['EXP'] >= endowment_cost['ability'] and endowment_level['ability'] < endowment_level_max['ability']:
                        player_parameter['EXP'] -= endowment_cost['ability']
                        endowment_ability_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 13:

                    if player_parameter['EXP'] >= endowment_cost['revive'] and endowment_level['revive'] < endowment_level_max['revive']:
                        player_parameter['EXP'] -= endowment_cost['revive']
                        endowment_revive_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 14:

                    if player_parameter['EXP'] >= endowment_cost['sale'] and endowment_level['sale'] < endowment_level_max['sale']:
                        player_parameter['EXP'] -= endowment_cost['sale']
                        endowment_sale_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if endowment_select['select'] == 15:

                    if player_parameter['EXP'] >= endowment_cost['CD_speedup'] and endowment_level['CD_speedup'] < endowment_level_max['CD_speedup']:
                        player_parameter['EXP'] -= endowment_cost['CD_speedup']
                        endowment_CD_speedup_upgrade()
                    else:
                        game_no_button_sound.play(0)

                if  endowment_select['select'] == 16:

                    if player_parameter['EXP'] >= endowment_cost['damage_limited'] and endowment_level['damage_limited'] < endowment_level_max['damage_limited']:
                        player_parameter['EXP'] -= endowment_cost['damage_limited']
                        endowment_damage_limited_upgrade()
                    else:
                        game_no_button_sound.play(0)

                    
            if button_start_endowment_img_rect.collidepoint(event.pos):
                scene['sub'] = "gaming"
                game_3_parameter_initialize()
                game_parameter_caculate()
                game_button_sound.play(0)
                pygame.mixer.stop()

            if skill_ATK_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 1
                game_button_sound.play(0)

            if skill_critical_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 2
                game_button_sound.play(0)

            if skill_fire_damage_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 3
                game_button_sound.play(0)

            if skill_ice_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 4
                game_button_sound.play(0)

            if skill_HP_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 5
                game_button_sound.play(0)

            if skill_health_drain_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 6
                game_button_sound.play(0)

            if skill_EXP_add_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 7
                game_button_sound.play(0)

            if skill_health_for_damage_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 8
                game_button_sound.play(0)

            if skill_health_regeneration_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 9
                game_button_sound.play(0)

            if skill_coin_add_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 10
                game_button_sound.play(0)
            
            if skill_partner_stronger_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 11
                game_button_sound.play(0)

            if skill_ability_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 12
                game_button_sound.play(0)

            if skill_revive_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 13
                game_button_sound.play(0)

            if skill_sale_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 14
                game_button_sound.play(0)

            if skill_CD_speedup_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 15
                game_button_sound.play(0)

            if skill_damage_limited_upgrade_img_rect.collidepoint(event.pos):
                endowment_select['select'] = 16
                game_button_sound.play(0)
            
def game_3_item_display(): #遊戲畫面物件顯示

    global round
    
    screen.blit(background_game_img, background_game_img_rect)

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 20)

    ability_ATK_cost_text = font.render(f"{format(ability_cost['ATK'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)
    ability_HP_cost_text = font.render(f"{format(ability_cost['HP'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)
    ability_fireball_cost_text = font.render(f"{format(ability_cost['fireball'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)
    ability_heal_cost_text = font.render(f"{format(ability_cost['heal'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)
    ability_freeze_cost_text = font.render(f"{format(ability_cost['freeze'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)
    ability_self_hurt_cost_text = font.render(f"{format(ability_cost['self_hurt'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0), None)

    ability_ATK_level_text = font.render(f"Lv {ability_level['ATK']}", True, (255,255,255), None)
    ability_HP_level_text = font.render(f"Lv {ability_level['HP']}", True, (255,255,255), None)
    ability_fireball_level_text = font.render(f"Lv {ability_level['fireball']}", True, (255,255,255), None)
    ability_heal_level_text = font.render(f"Lv {ability_level['heal']}", True, (255,255,255), None)
    ability_freeze_level_text = font.render(f"Lv {ability_level['freeze']}", True, (255,255,255), None)
    ability_self_hurt_level_text = font.render(f"Lv {ability_level['self_hurt']}", True, (255,255,255), None)

    ability_ATK_caption_text = font.render(f"basic damage +{current_ability_parameter['ATK']}", True, (255,255,255), None)
    ability_HP_caption_text = font.render(f"basic health +{current_ability_parameter['HP']}", True, (255,255,255), None)
    ability_fireball_caption_text = font.render(f"deal damage by {format(current_ability_parameter['fireball'] * ((100+current_endowment_parameter['ability'])/100), '.1f')}% of enemy's maximun health", True, (255,255,255), None)
    ability_heal_caption_text = font.render(f"heal {format(current_ability_parameter['heal'] * ((100+current_endowment_parameter['ability'])/100), '.1f')}% of health", True, (255,255,255), None)
    ability_freeze_caption_text_1 = font.render(f"increase {format(current_ability_parameter['freeze'] * ((100+current_endowment_parameter['ability'])/100), '.1f')} seconds of attack interval", True, (255,255,255), None)
    ability_freeze_caption_text_2 = font.render(f"of enermy", True, (255,255,255), None)
    ability_self_hurt_caption_text_1 = font.render(f"decrease 10% of health deal damage by {format(current_ability_parameter['self_hurt'] * ((100+current_endowment_parameter['ability'])/100), '.1f')}%", True, (255,255,255), None)
    ability_self_hurt_caption_text_2 = font.render(f"of it", True, (255,255,255), None)

    All_player_parameter_ATK_text = font.render(f"{format(player_parameter['current_damage'], '.1f')}", True, (255,255,255), None)
    All_player_parameter_HP_text = font.render(f"{format(player_parameter['current_health'],'.1f')}/{format(player_parameter['max_health'],'.1f')}", True, (255,255,255), None)
    player_parameter_coin_text = font.render(f"{format(player_parameter['money'], '.1f')}", True, (255,255,255), None)
    player_parameter_EXP_text = font.render(f"{int(player_parameter['EXP'])}", True, (255,255,255), None)

    partner_damage_lv1_text = font.render(f"{format(partner_parameter['lv1'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)
    partner_damage_lv2_text = font.render(f"{format(partner_parameter['lv2'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)
    partner_damage_lv3_text = font.render(f"{format(partner_parameter['lv3'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)
    partner_damage_lv4_text = font.render(f"{format(partner_parameter['lv4'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)
    partner_damage_lv5_text = font.render(f"{format(partner_parameter['lv5'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)
    partner_damage_lv6_text = font.render(f"{format(partner_parameter['lv6'] * ((100+current_endowment_parameter['partner']) / 100), '.1f')} dmg / sec", True, (255,255,255),None)

    partner_level_lv1_text = font.render(f"Lv {partner_level['lv1']}", True, (255,255,255),None)
    partner_level_lv2_text = font.render(f"Lv {partner_level['lv2']}", True, (255,255,255),None)
    partner_level_lv3_text = font.render(f"Lv {partner_level['lv3']}", True, (255,255,255),None)
    partner_level_lv4_text = font.render(f"Lv {partner_level['lv4']}", True, (255,255,255),None)
    partner_level_lv5_text = font.render(f"Lv {partner_level['lv5']}", True, (255,255,255),None)
    partner_level_lv6_text = font.render(f"Lv {partner_level['lv6']}", True, (255,255,255),None)

    partner_cost_lv1_text = font.render(f"{format(partner_cost['lv1'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    partner_cost_lv2_text = font.render(f"{format(partner_cost['lv2'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    partner_cost_lv3_text = font.render(f"{format(partner_cost['lv3'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    partner_cost_lv4_text = font.render(f"{format(partner_cost['lv4'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    partner_cost_lv5_text = font.render(f"{format(partner_cost['lv5'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    partner_cost_lv6_text = font.render(f"{format(partner_cost['lv6'] * ((100 - current_endowment_parameter['sale']) / 100), '.1f')}", True, (255,255,0),None)
    
    enemy_health_text = font.render(f"HP: {format(enemy['current_health'],'.1f')}", True, (255, 0, 0), None)
    attack_damage_text = font.render(f"ATK: {format(enemy['attack_damage'],'.1f')}", True, (255, 255, 255), None)
    number_text = font.render(f"{int(enemy['number'])}", True, (255, 0, 255), None)
    round_text = font.render(f"round:{round}", True, (255, 0, 0), None)

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 30)

    level_max_text = font.render("LEVEL MAX", True, (255,255,0), None)
    player_parameter_life_text = font.render(f"life:{int(player_parameter['life'])+1}", True, (255,0,0), None)
    damage_deal_text = font.render(f"-{format(damage['damage'],'.1f')}", True, (255,0,0), None)
    combo_text = font.render(f"{damage['combo']} combo", True, (255,127,0), None)

    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 50)
    
    fireball_CD_text = font.render(f"{int(ability_CD['fireball'])}", True, (255,0,0),None)
    heal_CD_text = font.render(f"{int(ability_CD['heal'])}", True, (255,0,0),None)
    freeze_CD_text = font.render(f"{int(ability_CD['freeze'])}", True, (255,0,0),None)
    self_hurt_CD_text = font.render(f"{int(ability_CD['self_hurt'])}", True, (255,0,0),None)

    screen.blit(partner_lv1_img, partner_lv1_img_rect)
    screen.blit(partner_damage_lv1_text,(123,0))
    screen.blit(partner_level_lv1_text,(123,93))
    screen.blit(partner_cost_lv1_text,(173,133))
    if player_parameter['money'] < partner_cost['lv1'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_1_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_1_rect)

    screen.blit(partner_lv2_img, partner_lv2_img_rect)
    screen.blit(partner_damage_lv2_text,(123,180))
    screen.blit(partner_level_lv2_text,(123,273))
    screen.blit(partner_cost_lv2_text,(173,313))
    if player_parameter['money'] < partner_cost['lv2'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_2_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_2_rect)

    screen.blit(partner_lv3_img, partner_lv3_img_rect)
    screen.blit(partner_damage_lv3_text,(123,360))
    screen.blit(partner_level_lv3_text,(123,453))
    screen.blit(partner_cost_lv3_text,(173,493))
    if player_parameter['money'] < partner_cost['lv3'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_3_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_3_rect)

    screen.blit(partner_lv4_img, partner_lv4_img_rect)
    screen.blit(partner_damage_lv4_text,(123,540))
    screen.blit(partner_level_lv4_text,(123,633))
    screen.blit(partner_cost_lv4_text,(173,673))
    if player_parameter['money'] < partner_cost['lv4'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_4_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_4_rect)

    screen.blit(partner_lv5_img, partner_lv5_img_rect)
    screen.blit(partner_damage_lv5_text,(123,720))
    screen.blit(partner_level_lv5_text,(123,813))
    screen.blit(partner_cost_lv5_text,(173,853))
    if player_parameter['money'] < partner_cost['lv5'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_5_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_5_rect)

    screen.blit(partner_lv6_img, partner_lv6_img_rect)
    screen.blit(partner_damage_lv6_text,(123,900))
    screen.blit(partner_level_lv6_text,(123,993))
    screen.blit(partner_cost_lv6_text,(173,1033))
    
    if player_parameter['money'] < partner_cost['lv6'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_partner_6_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_partner_6_rect)

    screen.blit(ability_attack_upgrade_img, ability_attack_upgrade_img_rect)
    if player_parameter['money'] < ability_cost['ATK'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_1_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_ability_1_rect)

    screen.blit(ability_ATK_cost_text, (1464,133))
    screen.blit(ability_ATK_level_text, (1414,93))
    screen.blit(ability_ATK_caption_text, (1414,0))
    
    screen.blit(ability_health_upgrade_img, ability_health_upgrade_img_rect)
    if player_parameter['money'] < ability_cost['HP'] * ((100 - current_endowment_parameter['sale']) / 100):
        screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_2_rect)
    else:
        screen.blit(button_upgrade_game_img, button_upgrade_img_ability_2_rect)

    screen.blit(ability_HP_cost_text, (1464,313))
    screen.blit(ability_HP_level_text, (1414,273))
    screen.blit(ability_HP_caption_text, (1414,180))
    
    screen.blit(ability_fireball_upgrade_img, ability_fireball_upgrade_img_rect)
    if ability_level['fireball'] < ability_level_max['fireball']:
        screen.blit(ability_fireball_cost_text, (1464,493))
        if player_parameter['money'] < ability_cost['fireball'] * ((100 - current_endowment_parameter['sale']) / 100):
            screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_3_rect)
        else:
            screen.blit(button_upgrade_game_img, button_upgrade_img_ability_3_rect)
    else:
        screen.blit(level_max_text, (1300 , 490))
    screen.blit(ability_fireball_level_text, (1414,453))
    screen.blit(ability_fireball_caption_text, (1414,360))

    screen.blit(ability_heal_upgrade_img, ability_heal_upgrade_img_rect)
    if ability_level['heal'] < ability_level_max['heal']:
        screen.blit(ability_heal_cost_text, (1464,673))
        if player_parameter['money'] < ability_cost['heal'] * ((100 - current_endowment_parameter['sale']) / 100):
            screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_4_rect)
        else:
            screen.blit(button_upgrade_game_img, button_upgrade_img_ability_4_rect)
    else:
        screen.blit(level_max_text, (1300 , 670))
    screen.blit(ability_heal_level_text, (1414,633))
    screen.blit(ability_heal_caption_text, (1414,540))
    
    screen.blit(ability_freeze_upgrade_img, ability_freeze_upgrade_img_rect)
    if ability_level['freeze'] < ability_level_max['freeze']:
        screen.blit(ability_freeze_cost_text, (1464,853))
        if player_parameter['money'] < ability_cost['freeze'] * ((100 - current_endowment_parameter['sale']) / 100):
            screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_5_rect)
        else:
            screen.blit(button_upgrade_game_img, button_upgrade_img_ability_5_rect)
    else:
        screen.blit(level_max_text, (1300 , 850))
    screen.blit(ability_freeze_level_text, (1414,813))
    screen.blit(ability_freeze_caption_text_1, (1414,720))
    screen.blit(ability_freeze_caption_text_2, (1414,740))
    
    screen.blit(ability_self_hurt_upgrade_img, ability_self_hurt_upgrade_img_rect)
    if ability_level['self_hurt'] < ability_level_max['self_hurt']:
        screen.blit(ability_self_hurt_cost_text, (1464,1033))
        if player_parameter['money'] < ability_cost['self_hurt'] * ((100 - current_endowment_parameter['sale']) / 100):
            screen.blit(button_no_upgrade_game_img, button_upgrade_img_ability_6_rect)
        else:
            screen.blit(button_upgrade_game_img, button_upgrade_img_ability_6_rect)
    else:
        screen.blit(level_max_text, (100 , 1030))
    screen.blit(ability_self_hurt_level_text, (1414,993))
    screen.blit(ability_self_hurt_caption_text_1, (1414,900))
    screen.blit(ability_self_hurt_caption_text_2, (1414,920))

    screen.blit(picture_ATK_img, picture_ATK_img_rect)
    screen.blit(All_player_parameter_ATK_text,(770,780))

    screen.blit(picture_HP_img, picture_HP_img_rect)
    screen.blit(All_player_parameter_HP_text,(1100,780))
    screen.blit(player_parameter_life_text,(1100,820))

    screen.blit(picture_coin_img, picture_coin_img_rect)
    screen.blit(player_parameter_coin_text,(770,980))

    screen.blit(picture_EXP_img, picture_EXP_img_rect)
    screen.blit(player_parameter_EXP_text,(1100,980))

    if enemy_type['type'] == 0:
        screen.blit(enemy_normal_1_img, enemy_normal_1_img_rect)
    else:
        if enemy['number'] == 50:
            screen.blit(enemy_boss_cuber_img, enemy_boss_cuber_img_rect)
        elif enemy['number'] == 100:
            screen.blit(enemy_boss_demon_img, enemy_boss_demon_img_rect)
        if enemy['number'] == 150:
            screen.blit(enemy_boss_observer_img, enemy_boss_observer_img_rect)
        elif enemy['number'] == 200:
            screen.blit(enemy_boss_destroyer_img, enemy_boss_destroyer_img_rect)
            
    if ability_CD['fireball'] > 0:
        screen.blit(fireball_CD_text, (1300,400))
    
    if ability_CD['heal'] > 0:
        screen.blit(heal_CD_text, (1300,579))
    
    if ability_CD['freeze'] > 0:
        screen.blit(freeze_CD_text, (1300,758))
    
    if ability_CD['self_hurt'] > 0:
        screen.blit(self_hurt_CD_text, (1300,937))
        
            
    # 顯示敵人血量
    screen.blit(enemy_health_text, (940,50))
    
    # 顯示敵人攻擊力
    screen.blit(attack_damage_text, (940, 550))

    #顯示關卡
    screen.blit(number_text, (635, 0))

    #顯示周目
    screen.blit(round_text,(635,25))
    
    if damage['time'] > 0:
        screen.blit(damage_deal_text, (860, 100))
        screen.blit(combo_text, (860, 140))

def game_3_music_display(): #遊戲畫面聲音播放

    if enemy_type['type'] == 0:
        if not pygame.mixer.get_busy():
            game_normal_music.play(-1) 

    elif enemy_type['type'] == 1:
        if not pygame.mixer.get_busy():
            game_boss_music.play(-1) 

def game_3_motion_detect(): #遊戲畫面動作偵測
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_button_sound.play(0)
            game_3_parameter_initialize()
            scene['sub'] = "endowment"
            pygame.mixer.stop()


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if button_upgrade_img_ability_1_rect.collidepoint(event.pos):
                if player_parameter['money'] >= ability_cost['ATK'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= ability_cost['ATK'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    ability_ATK_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_ability_2_rect.collidepoint(event.pos):
                if player_parameter['money'] >= ability_cost['HP'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= ability_cost['HP'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    ability_HP_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_ability_3_rect.collidepoint(event.pos):
                if ability_level['fireball'] < ability_level_max['fireball']:
                    if player_parameter['money'] >= ability_cost['fireball'] * ((100 - current_endowment_parameter['sale']) / 100):
                        player_parameter['money'] -= ability_cost['fireball'] * ((100 - current_endowment_parameter['sale']) / 100)
                        game_button_sound.play(0)
                        ability_fireball_upgrade()
                    else:
                        game_no_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_ability_4_rect.collidepoint(event.pos):
                if ability_level['heal'] < ability_level_max['heal']:
                    if player_parameter['money'] >= ability_cost['heal'] * ((100 - current_endowment_parameter['sale']) / 100):
                        player_parameter['money'] -= ability_cost['heal'] * ((100 - current_endowment_parameter['sale']) / 100)
                        game_button_sound.play(0)
                        ability_heal_upgrade()
                    else:
                        game_no_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_ability_5_rect.collidepoint(event.pos):
                if ability_level['freeze'] < ability_level_max['freeze']:
                    if player_parameter['money'] >= ability_cost['freeze'] * ((100 - current_endowment_parameter['sale']) / 100):
                        player_parameter['money'] -= ability_cost['freeze'] * ((100 - current_endowment_parameter['sale']) / 100)
                        game_button_sound.play(0)
                        ability_freeze_upgrade()
                    else:
                        game_no_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_ability_6_rect.collidepoint(event.pos):
                if ability_level['self_hurt'] < ability_level_max['self_hurt']:
                    if player_parameter['money'] >= ability_cost['self_hurt'] * ((100 - current_endowment_parameter['sale']) / 100):
                        player_parameter['money'] -= ability_cost['self_hurt'] * ((100 - current_endowment_parameter['sale']) / 100)
                        game_button_sound.play(0)
                        ability_self_hurt_upgrade()
                    else:
                        game_no_button_sound.play(0)
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_1_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv1'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv1'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv1_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_2_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv2'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv2'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv2_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_3_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv3'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv3'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv3_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_4_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv4'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv4'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv4_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_5_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv5'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv5'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv5_upgrade()
                else:
                    game_no_button_sound.play(0)

            if button_upgrade_img_partner_6_rect.collidepoint(event.pos):
                if player_parameter['money'] >= partner_cost['lv6'] * ((100 - current_endowment_parameter['sale']) / 100):
                    player_parameter['money'] -= partner_cost['lv6'] * ((100 - current_endowment_parameter['sale']) / 100)
                    game_button_sound.play(0)
                    partner_lv6_upgrade()
                else:
                    game_no_button_sound.play(0)
                    
            if ability_fireball_upgrade_img_rect.collidepoint(event.pos):
                if ability_level['fireball'] > 0:
                    if ability_CD['fireball'] == 0:
                        game_button_sound.play(0)
                        skill_fireball()
                    else:
                        game_no_button_sound.play(0)
                
                else:
                    game_no_button_sound.play(0)
                    
            if ability_heal_upgrade_img_rect.collidepoint(event.pos):
                if ability_level['heal'] > 0:
                    if ability_CD['heal'] == 0:
                        game_button_sound.play(0)
                        skill_heal()
                    else:
                        game_no_button_sound.play(0)
                
                else:
                    game_no_button_sound.play(0)
                    
            if ability_freeze_upgrade_img_rect.collidepoint(event.pos):
                if ability_level['freeze'] > 0:
                    if ability_CD['freeze'] == 0:
                        game_button_sound.play(0)
                        skill_freeze()
                    else:
                        game_no_button_sound.play(0)
                
                else:
                    game_no_button_sound.play(0)
                    
            if ability_self_hurt_upgrade_img_rect.collidepoint(event.pos):
                if ability_level['self_hurt'] > 0:
                    if ability_CD['self_hurt'] == 0:
                        game_button_sound.play(0)
                        skill_self_hurt()
                    else:
                        game_no_button_sound.play(0)
                
                else:
                    game_no_button_sound.play(0)
            
            if enemy_normal_1_img_rect.collidepoint(event.pos):  # 點擊敵人
                player_attack()
                game_player_attack_sound.play(0)
                
    enemy_attack()
     
def game_4_item_display(): #通關畫面物件顯示
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 60)
    thank_list1_text = font.render("game designer:Spongenotcake", True, ( 255, 255, 255))
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 60)
    thank_list2_text = font.render("music designer:Spongenotcake", True, (255, 255, 255))

    
    screen.blit(background_complete_img, background_complete_img_rect)
    screen.blit(button_back_img, button_back_img_complete_rect)
    screen.blit(thank_list1_text,(300,400))
    screen.blit(thank_list2_text,(300,500))
    
def game_4_music_display(): #通關畫面聲音播放
    if enemy_type['type'] == 0:
        if not pygame.mixer.get_busy():
            game_normal_music.play(-1) 
    elif enemy_type['type'] == 1:
        if not pygame.mixer.get_busy():
            game_boss_music.play(-1) 
    
def game_4_motion_detect(): #通關畫面動作偵測
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if button_back_img_complete_rect.collidepoint(event.pos):
                game_button_sound.play(0)
                scene['sub'] = "endowment"
                game_3_parameter_initialize()
                pygame.mixer.stop()
    
def game_over_item_display(): #死亡畫面物件顯示
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 150)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 30)
    restart_text = font.render("Press ESC to return", True, (255, 255, 255))
    best_progress_text = font.render(f"progress : {enemy['number']}", True, (255, 255, 255))
    
    screen.fill((0, 0, 0))
    screen.blit(game_over_text,(670,300))
    screen.blit(restart_text,(800,1000))
    screen.blit(best_progress_text, (800,800))
       
def game_over_music_display(): #死亡畫面聲音播放
    if enemy_type['type'] == 0:
        if not pygame.mixer.get_busy():
            game_normal_music.play(-1) 

    elif enemy_type['type'] == 1:
        if not pygame.mixer.get_busy():
            game_boss_music.play(-1) 
    
def game_over_motion_detect():# 死亡畫面動作偵測
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        game_button_sound.play(0)
        game_3_parameter_initialize()
        scene['sub'] = "endowment"
        pygame.mixer.stop()
    
def volume_load(): #讀取音量設定
    global settings
    
    try:
        with open(os.path.join(os.getcwd(), 'settings', 'settings.json'), 'r') as f:
            setting = json.load(f)
            settings = setting
    except (FileNotFoundError, json.JSONDecodeError):
        volume_write()
        volume_load()
        
def volume_write(): #保存音量設定
    global settings    

    with open(os.path.join(os.getcwd(), 'settings','settings.json'), 'w') as f:
        json.dump(settings, f)
        
def saving_date_load(): #讀取存檔存取時間
    global saving_1_time
    global saving_2_time
    global saving_3_time
    
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_1.json'), 'r') as f:
            player_profile = json.load(f)
            saving_1_time = player_profile[0]
            if not isinstance(player_profile, list) or len(player_profile) < 6:
                no_data['save_1'] = 1

    except (FileNotFoundError, json.JSONDecodeError):
        no_data['save_1'] = 1
        
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_2.json'), 'r') as f:
            player_profile = json.load(f)
            saving_2_time = player_profile[0]
            if not isinstance(player_profile, list) or len(player_profile) < 6:
                no_data['save_2'] = 1

    except (FileNotFoundError, json.JSONDecodeError):
        no_data['save_2'] = 1
        
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_3.json'), 'r') as f:
            player_profile = json.load(f)
            saving_3_time = player_profile[0]
            if not isinstance(player_profile, list) or len(player_profile) < 6:
                no_data['save_3'] = 1

    except (FileNotFoundError, json.JSONDecodeError):
        no_data['save_3'] = 1
        
def saving_load_1(): #讀取存檔_1
    
    global player_parameter
    global endowment_level
    global endowment_cost
    global endowment_parameter
    global current_endowment_parameter
    global round
    
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_1.json'), 'r') as f:
            player_profile = json.load(f)
            if not isinstance(player_profile, list) or len(player_profile) < 6:
                 saving_write_1()
                 saving_load_1()
            player_parameter['EXP'] = player_profile[1]
            endowment_level = player_profile[2]
            endowment_cost = player_profile[3]
            endowment_parameter = player_profile[4]
            current_endowment_parameter = player_profile[5]
            round = player_profile[6]
    except (FileNotFoundError, json.JSONDecodeError):
        saving_write_1()
        saving_load_1()
        
def saving_load_2(): #讀取存檔_2
    
    global player_parameter
    global endowment_level
    global endowment_cost
    global endowment_parameter
    global current_endowment_parameter
    global round
    
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_2.json'), 'r') as f:
            player_profile = json.load(f)
            if not isinstance(player_profile, list) or len(player_profile) < 5:
                saving_write_2()
                saving_load_2()
            player_parameter['EXP'] = player_profile[1]
            endowment_level = player_profile[2]
            endowment_cost = player_profile[3]
            endowment_parameter = player_profile[4]
            current_endowment_parameter = player_profile[5]
            round = player_profile[6]
    except (FileNotFoundError, json.JSONDecodeError):
        saving_write_2()
        saving_load_2()
    
def saving_load_3(): #讀取存檔_3
    global player_parameter
    global endowment_level
    global endowment_cost
    global endowment_parameter
    global current_endowment_parameter
    global round
    
    try:
        with open(os.path.join(os.getcwd(), 'data', 'save_3.json'), 'r') as f:
            player_profile = json.load(f)
            if not isinstance(player_profile, list) or len(player_profile) < 5:
                 saving_write_3()
                 saving_load_3()
            player_parameter['EXP'] = player_profile[1]
            endowment_level = player_profile[2]
            endowment_cost = player_profile[3]
            endowment_parameter = player_profile[4]
            current_endowment_parameter = player_profile[5]
            round = player_profile[6]
    except (FileNotFoundError, json.JSONDecodeError):
        saving_write_3()
        saving_load_3()

def saving_write_1(): #寫入存檔_1
    with open(os.path.join(os.getcwd(), 'data', 'save_1.json'), 'w') as f:
        today = datetime.datetime.today()
        date = {
        'year': today.year,
        'month': today.month,
        'day': today.day,
        'hour': today.hour,
        'minute': today.minute,
        'second': today.second
        }
        if no_data['save_1'] == 1:
            no_data['save_1'] = 0
            
        player_profile = [date,player_parameter['EXP'],endowment_level,endowment_cost,endowment_parameter,current_endowment_parameter,round]
        json.dump(player_profile,f)

def saving_write_2(): #寫入存檔_2
    with open(os.path.join(os.getcwd(), 'data', 'save_2.json'), 'w') as f:
        today = datetime.datetime.today()
        date = {
        'year': today.year,
        'month': today.month,
        'day': today.day,
        'hour': today.hour,
        'minute': today.minute,
        'second': today.second
        }
        
        if no_data['save_2'] == 1:
            no_data['save_2'] = 0

        player_profile = [date,player_parameter['EXP'],endowment_level,endowment_cost,endowment_parameter,current_endowment_parameter,round]
        json.dump(player_profile,f)

def saving_write_3(): #寫入存檔_3
    with open(os.path.join(os.getcwd(), 'data', 'save_3.json'), 'w') as f:
        today = datetime.datetime.today()
        date = {
        'year': today.year,
        'month': today.month,
        'day': today.day,
        'hour': today.hour,
        'minute': today.minute,
        'second': today.second
        }
        
        if no_data['save_3'] == 1:
            no_data['save_3'] = 0
            
        player_profile = [date,player_parameter['EXP'],endowment_level,endowment_cost,endowment_parameter,current_endowment_parameter,round]
        json.dump(player_profile,f)
        
def game_2_parameter_initialize(): #天賦相關數值初始化
    global player_parameter, endowment_level, endowment_cost, endowment_parameter, current_endowment_parameter, round
    
    player_parameter = copy.deepcopy(player_parameter_default)
    endowment_level = copy.deepcopy(endowment_level_default)
    endowment_cost = copy.deepcopy(endowment_cost_default)
    endowment_parameter = copy.deepcopy(endowment_parameter_default)
    current_endowment_parameter = copy.deepcopy(current_endowment_parameter_default)
    round = copy.deepcopy(round_default)

def game_3_parameter_initialize(): #遊戲相關數值初始化
    global player_parameter, endowment_level, partner_level, ability_level, ability_cost, ability_parameter, partner_cost, partner_parameter, enemy, ability_CD, current_ability_parameter, damage
    
    player_parameter.update({k: copy.deepcopy(v) for k, v in player_parameter_default.items() if k != 'EXP'})
    enemy_type['type'] = 0
    if player_parameter['EXP'] > 999999:
        player_parameter['EXP'] = 999999
    
    partner_level = copy.deepcopy(partner_level_default)
    partner_cost = copy.deepcopy(partner_cost_default)
    partner_parameter = copy.deepcopy(partner_parameter_default)
    ability_cost = copy.deepcopy(ability_cost_default)
    ability_level = copy.deepcopy(ability_level_default)
    ability_parameter = copy.deepcopy(ability_parameter_default)
    ability_CD = copy.deepcopy(ability_CD_default)
    current_ability_parameter = copy.deepcopy(current_ability_parameter_default)
    enemy = copy.deepcopy(enemy_default)
    damage = copy.deepcopy(damage_default)
    
def player_attack(): #玩家攻擊
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 30)
    if_critical = random.randint(1,100)
    critical = player_parameter['critical']
    enemy['fire'] = 3
    
    if if_critical <= critical:
        if player_parameter['current_health'] <= player_parameter['max_health'] / 2:
            total_damage = player_parameter['current_damage'] * 1.5 * ((100+current_endowment_parameter['health_for_damage'])/100)  
            damage_dealed_text = font.render(f"-{format(total_damage, '.1f')}", True, (255, 0, 0))        
            screen.blit(damage_dealed_text,(860,60))
        else:
            total_damage = player_parameter['current_damage'] * 1.5   
            damage_dealed_text = font.render(f"-{format(total_damage, '.1f')}", True, (255, 0, 0))        
            screen.blit(damage_dealed_text,(860,60))
    else:
        if player_parameter['current_health'] <= player_parameter['max_health'] / 2:
            total_damage =  player_parameter['current_damage'] * ((100+current_endowment_parameter['health_for_damage'])/100)       
            damage_dealed_text = font.render(f"-{format(total_damage, '.1f')}", True, (255, 255, 255))        
            screen.blit(damage_dealed_text,(860,60))
        else:
            total_damage =  player_parameter['current_damage']      
            damage_dealed_text = font.render(f"-{format(total_damage, '.1f')}", True, (255, 255, 255))        
            screen.blit(damage_dealed_text,(860,60))
    
    enemy['current_health'] -= total_damage
    damage['damage'] += total_damage
    damage['combo'] += 1
    damage['time'] = 1
    
    if player_parameter['current_health'] >= 0:
        player_parameter['current_health'] += player_parameter['current_damage'] * (current_endowment_parameter['health_drain'] / 100)
    
def partner_attack(): #同伴攻擊
    enemy['current_health'] -= (partner_parameter['lv1']+partner_parameter['lv2']+partner_parameter['lv3']+partner_parameter['lv4']+partner_parameter['lv5']+partner_parameter['lv6']) * ((100+current_endowment_parameter['partner']) / 100)
    
def game_parameter_caculate(): #遊戲開始時參數計算
    global enemy_last_attack_time, enemy_strength_increase, reward_EXP_increase, reward_coin_increase, round
    
    enemy_last_attack_time = time.time()
    player_parameter['current_damage'] = player_parameter['basic_damage']*((100+current_endowment_parameter['ATK'])/100)
    player_parameter['max_health'] = player_parameter['basic_health']*((100+current_endowment_parameter['HP'])/100)
    player_parameter['current_health'] = player_parameter['max_health']
    player_parameter['critical'] = current_endowment_parameter['critical']
    player_parameter['life'] = current_endowment_parameter['revive']
    enemy_strength_increase = 1.1 + 0.1 * (round - 1)
    reward_EXP_increase = 1.04 +0.02 * (round - 1)
    enemy['attack_interval'] += current_endowment_parameter['ice']
    
def game_parameter_caculate_keep(): #遊戲開始後持續參數計算
    global game_time
    global damage_time
    
    player_parameter['current_damage'] = player_parameter['basic_damage']*((100+current_endowment_parameter['ATK'])/100)
    player_parameter['max_health'] = player_parameter['basic_health']*((100+current_endowment_parameter['HP'])/100)
    player_parameter['critical'] = current_endowment_parameter['critical']
    
    
    if player_parameter['EXP'] > 999999:
        player_parameter['EXP'] = 999999
        
    current_time = time.time()
    if current_time - game_time >= 1:
        game_time = current_time
        partner_attack()
        player_parameter['current_health'] += player_parameter['max_health'] * (current_endowment_parameter['health_regeneration'] / 100)
        
        if ability_CD['fireball'] > 0:
            ability_CD['fireball'] -= 1
            
        if ability_CD['heal'] > 0:
            ability_CD['heal'] -= 1
            
        if ability_CD['freeze'] > 0:
            ability_CD['freeze'] -= 1
            
        if ability_CD['self_hurt'] > 0:
            ability_CD['self_hurt'] -= 1
        
        if endowment_level['fire_damage'] > 0:
            if enemy['fire'] <= 0:
                pass
            else:
                enemy['fire'] -= 1
                fire_damage = player_parameter['current_damage'] * (current_endowment_parameter['fire_damage'] / 100)
                enemy['current_health'] -= fire_damage
                font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 30)
                fire_damage_text = font.render(f"-{format(fire_damage, '.1f')}", True, (255, 128, 0))
                screen.blit(fire_damage_text,(1060,100))
                
    if current_time - game_time >= 0.1:
        damage_time = current_time
        if damage['time'] > 0:
            damage['time'] -= 0.1
        else:
            damage['damage'] = 0
            damage['combo'] = 0
          
def game_parameter_detect(): #遊戲參數偵測
    global round
    
    if player_parameter['current_health'] >= player_parameter['max_health']:
        player_parameter['current_health'] = player_parameter['max_health']
    
    if enemy['current_health'] <= 0:  # 擊敗敵人
        enemy['current_health'] = 0  # 確保不會變成負數
        player_parameter['money'] += enemy['reward_money'] * ((100 + current_endowment_parameter['coin_add']) / 100)
        player_parameter['EXP'] += enemy['reward_EXP'] * ((100 + current_endowment_parameter['EXP_add']) / 100)
        game_enemy_death_sound.play(0)
        
        if enemy['number'] == 200:
            round += 1
            scene['sub'] = "complete" 
        else:    
            spawn_enemy()
    
def ability_ATK_upgrade(): #升級能力"基礎攻擊力"
        ability_level['ATK'] += 1
        player_parameter['basic_damage'] += ability_level['ATK']
        current_ability_parameter['ATK'] += ability_level['ATK']
        ability_cost['ATK'] += 15

def ability_HP_upgrade(): #升級能力"基礎生命力"
        ability_level['HP'] += 1
        player_parameter['basic_health'] += ability_level['HP'] * 2
        current_ability_parameter['HP'] += ability_level['HP'] * 2
        health_lost = player_parameter['max_health'] - player_parameter['current_health'] 
        player_parameter['max_health'] = player_parameter['basic_health']*((100+current_endowment_parameter['HP'])/100)
        player_parameter['current_health'] = player_parameter['max_health'] - health_lost
        ability_cost['HP'] += 15

def ability_fireball_upgrade(): #升級技能"火球"

    ability_level['fireball'] += 1
    ability_cost['fireball'] += 200
    current_ability_parameter['fireball'] = ability_parameter['fireball']
    ability_parameter['fireball'] += 1

def ability_heal_upgrade(): #升級技能"回復"

    ability_level['heal'] += 1
    ability_cost['heal'] += 200
    current_ability_parameter['heal'] = ability_parameter['heal']
    ability_parameter['heal'] += 1

def ability_freeze_upgrade(): #升級技能"冰凍"
    
    ability_level['freeze'] += 1
    ability_cost['freeze'] += 200
    current_ability_parameter['freeze'] = ability_parameter['freeze']
    ability_parameter['freeze'] += 0.2

def ability_self_hurt_upgrade(): #升級技能"自傷"
    
    ability_level['self_hurt'] += 1
    ability_cost['self_hurt'] += 200
    current_ability_parameter['self_hurt'] = ability_parameter['self_hurt']
    ability_parameter['self_hurt'] += 100

def partner_lv1_upgrade(): #升級同伴"lv 1"

    partner_level['lv1'] += 1
    partner_cost['lv1'] += 1
    partner_parameter['lv1'] += 1
    
def partner_lv2_upgrade(): #升級同伴"lv 2"

    partner_level['lv2'] += 1
    partner_cost['lv2'] += 30
    partner_parameter['lv2'] += 30

def partner_lv3_upgrade(): #升級同伴"lv 3"

    partner_level['lv3'] += 1
    partner_cost['lv3'] += 600
    partner_parameter['lv3'] += 600

def partner_lv4_upgrade(): #升級同伴"lv 4"

    partner_level['lv4'] += 1
    partner_cost['lv4'] += 36000
    partner_parameter['lv4'] += 36000

def partner_lv5_upgrade(): #升級同伴"lv 5"

    partner_level['lv5'] += 1
    partner_cost['lv5'] += 1080000
    partner_parameter['lv5'] += 1080000

def partner_lv6_upgrade(): #升級同伴"lv 6"

    partner_level['lv6'] += 1
    partner_cost['lv6'] += 30000000
    partner_parameter['lv6'] += 30000000

def endowment_ability_upgrade(): #升級天賦"技能效果增強"

    endowment_level['ability'] += 1
    endowment_cost['ability'] += 30
    current_endowment_parameter['ability'] = endowment_parameter['ability']
    endowment_parameter['ability'] += 5

def endowment_coin_add_upgrade(): #升級天賦"金錢掉落增加"

    endowment_level['coin_add'] += 1
    endowment_cost['coin_add'] += 10
    current_endowment_parameter['coin_add'] = endowment_parameter['coin_add']
    endowment_parameter['coin_add'] += 10

def endowment_CD_speedup_upgrade(): #升級天賦"技能冷卻縮短"

    endowment_level['CD_speedup'] += 1
    endowment_cost['CD_speedup']  += 30
    current_endowment_parameter['CD_speedup'] = endowment_parameter['CD_speedup']
    endowment_parameter['CD_speedup'] += 2

def endowment_ATK_upgrade(): #升級天賦"傷害增加"
    
    endowment_level['ATK'] += 1
    endowment_cost['ATK'] += 2
    current_endowment_parameter['ATK'] = endowment_parameter['ATK']
    endowment_parameter['ATK'] += 20

def endowment_critical_upgrade(): #升級天賦"精準暴擊"

    endowment_level['critical'] += 1
    endowment_cost['critical'] += 8
    current_endowment_parameter['critical'] = endowment_parameter['critical']
    endowment_parameter['critical'] += 2

def endowment_damage_limited_upgrade(): #升級天賦"傷害限制"

    endowment_level['damage_limited'] += 1
    endowment_cost['damage_limited'] *= 5
    current_endowment_parameter['damage_limited'] = endowment_parameter['damage_limited']
    endowment_parameter['damage_limited'] -= 10

def endowment_EXP_add_upgrade(): #升級天賦"經驗值掉落增加"

    endowment_level['EXP_add'] += 1
    endowment_cost['EXP_add'] += 10
    current_endowment_parameter['EXP_add'] = endowment_parameter['EXP_add']
    endowment_parameter['EXP_add'] += 10

def endowment_fire_damage_upgrade(): #升級天賦"火焰附加"

    endowment_level['fire_damage'] += 1
    endowment_cost['fire_damage'] += 12
    current_endowment_parameter['fire_damage'] = endowment_parameter['fire_damage']
    endowment_parameter['fire_damage'] += 2

def endowment_health_drain_upgrade(): #升級天賦"吸血"

    endowment_level['health_drain'] += 1
    endowment_cost['health_drain'] += 15
    current_endowment_parameter['health_drain'] = endowment_parameter['health_drain']
    endowment_parameter['health_drain'] += 1

def endowment_health_for_damage_upgrade(): #升級天賦"愈挫愈勇"

    endowment_level['health_for_damage'] += 1
    endowment_cost['health_for_damage'] *= 1.1
    current_endowment_parameter['health_for_damage'] = endowment_parameter['health_for_damage']
    endowment_parameter['health_for_damage'] += 10

def endowment_health_regeneration_upgrade(): #升級天賦"自愈"

    endowment_level['health_regeneration'] += 1
    endowment_cost['health_regeneration'] += 15
    current_endowment_parameter['health_regeneration'] = endowment_parameter['health_regeneration']
    endowment_parameter['health_regeneration'] += 0.2

def endowment_HP_upgrade(): #升級天賦"血量增加"

    endowment_level['HP'] += 1
    endowment_cost['HP'] += 4
    current_endowment_parameter['HP'] = endowment_parameter['HP']
    endowment_parameter['HP'] += 20

def endowment_ice_upgrade(): #升級天賦"凍結"

    endowment_level['ice'] += 1
    endowment_cost['ice'] *= 2
    current_endowment_parameter['ice'] = endowment_parameter['ice']
    endowment_parameter['ice'] += 0.5

def endowment_partner_upgrade(): #升級天賦"同伴強化"

    endowment_level['partner'] += 1
    endowment_cost['partner'] += 6
    current_endowment_parameter['partner'] = endowment_parameter['partner']
    endowment_parameter['partner'] += 20

def endowment_revive_upgrade(): #升級天賦"復甦"

    endowment_level['revive'] += 1
    endowment_cost['revive'] *= 20
    current_endowment_parameter['revive'] = endowment_parameter['revive']
    endowment_parameter['revive'] += 1

def endowment_sale_upgrade(): #升級天賦"特價優惠"
    endowment_level['sale'] += 1
    endowment_cost['sale'] += 50
    current_endowment_parameter['sale'] = endowment_parameter['sale']
    endowment_parameter['sale'] += 5
    
def enemy_attack(): #敵人攻擊
    global enemy_last_attack_time
    current_time = time.time()
    font = pygame.font.Font('item/text/Grand9K Pixel.ttf', 30)
    attack_countdown_text = font.render(f"{format(enemy['attack_interval']-(current_time - enemy_last_attack_time), '.1f')}", True, (255, 0, 0))
    screen.blit(attack_countdown_text,(1160,300))
    if current_time - enemy_last_attack_time >= enemy['attack_interval']:  # 使用變數來控制攻擊間隔
        
        damage = enemy['attack_damage']
        
        if damage > player_parameter['max_health'] * (current_endowment_parameter['damage_limited'] / 100):
            damage = player_parameter['max_health'] * (current_endowment_parameter['damage_limited'] / 100)
            
        player_parameter['current_health'] -= damage
        game_player_damaged_sound.play(0)
        if player_parameter['current_health'] <= 0:
            player_parameter['life'] -= 1
            player_parameter['current_health'] = player_parameter['max_health']
        if player_parameter['life'] < 0:
            scene['sub'] = "game_over"
        enemy_last_attack_time = current_time
        
def spawn_enemy(): #生成敵人
    global enemy_last_attack_time
    enemy_last_attack_time = time.time()
    enemy['number'] += 1
    
    if enemy['number']%50 != 0: #生成小怪
        enemy_type['type'] = 0
        enemy['max_health'] = float(enemy['max_health'] * enemy_strength_increase)  # 增加血量
        enemy['current_health'] = enemy['max_health']
        enemy['attack_damage'] = float(enemy['attack_damage'] * enemy_strength_increase)  # 增加攻擊力
        enemy['reward_money'] = float(enemy['reward_money'] * reward_coin_increase)  # 增加獎勵金幣
        enemy['reward_EXP'] = float(enemy['reward_EXP'] * reward_EXP_increase)  # 增加獎勵經驗值
        
        if (enemy['number']-1)%50 == 0: #確認上個階段是否不同，如果是，則切換音樂並回正強度趨勢線
            enemy['max_health'] = float(enemy['max_health'] * enemy_strength_increase / 50) 
            enemy['current_health']=enemy['max_health']
            enemy['attack_damage'] = float(enemy['attack_damage'] * enemy_strength_increase / 25)  
            enemy['reward_money'] = float(enemy['reward_money'] * reward_coin_increase / 20) 
            enemy['reward_EXP'] = float(enemy['reward_EXP'] * reward_EXP_increase / 20)
            enemy['attack_interval'] -= 7
            pygame.mixer.stop()
    else:
        enemy_type['type'] = 1
        enemy['max_health'] = float(enemy['max_health'] * enemy_strength_increase * 50)  # 增加血量
        enemy['current_health']=enemy['max_health']
        enemy['attack_damage'] = float(enemy['attack_damage'] * enemy_strength_increase * 25)  # 增加攻擊力
        enemy['reward_money'] = float(enemy['reward_money'] * reward_coin_increase * 20)  # 增加獎勵金幣
        enemy['reward_EXP'] = float(enemy['reward_EXP'] * reward_EXP_increase * 20)  # 增加獎勵經驗值
        enemy['attack_interval'] += 7
        pygame.mixer.stop()
        
def skill_fireball(): #施放技能"火球"
    damage = enemy['max_health']*(current_ability_parameter['fireball'] / 100) * ((100+current_endowment_parameter['ability'])/100)
    if damage > player_parameter['current_damage'] * 100:
        damage = player_parameter['current_damage'] * 100
    
    enemy['current_health'] -= damage
    
    ability_CD['fireball'] = 30 * ((100-current_endowment_parameter['CD_speedup'])/100)
    
def skill_heal(): #施放技能"回復"
    player_parameter['current_health'] += player_parameter['max_health'] * (current_ability_parameter['heal'] / 100) * ((100+current_endowment_parameter['ability'])/100)


    ability_CD['heal'] = 30 * ((100-current_endowment_parameter['CD_speedup'])/100)

def skill_freeze(): #施放技能"冰凍"
    global enemy_last_attack_time
    enemy_last_attack_time += current_ability_parameter['freeze'] * ((100+current_endowment_parameter['ability'])/100)

    ability_CD['freeze'] = 30 * ((100-current_endowment_parameter['CD_speedup'])/100)

def skill_self_hurt(): #施放技能"自傷"
    damage = player_parameter['current_health'] * (10 / 100) * (current_ability_parameter['self_hurt'] / 100) * ((100+current_endowment_parameter['ability'])/100)
    player_parameter['current_health'] -= player_parameter['current_health'] * (10 / 100)
    enemy['current_health'] -= damage
    ability_CD['self_hurt'] = 30 * ((100-current_endowment_parameter['CD_speedup'])/100)
    
#場景初始化
scene['main'] = "main"
scene['sub'] = -1

#聲音音量初始化
volume_load()
game_main_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10))
game_normal_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10))
game_boss_music.set_volume((settings['master_volume']/10)*(settings['music_volume']/10))
game_button_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
game_no_button_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
game_player_attack_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
game_player_damaged_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))
game_enemy_death_sound.set_volume((settings['master_volume']/10) * (settings['FX_volume'] / 10))

#程式迴圈
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # 避免 `pygame.quit()` 後繼續執行

    screen.fill((0, 0, 0))

    update()  # 確保變數更新

    pygame.display.flip()