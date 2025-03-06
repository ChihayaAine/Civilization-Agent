#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多Agent文明碰撞模拟系统
主程序入口
"""

import os
import sys
import argparse
import json
from datetime import datetime
import random

# 导入配置
from config.simulation_config import SimulationConfig
from config.llm_config import LLMConfig

# 导入LLM接口
from llm.llm_interface import LLMInterface

# 导入模型
from models.world_state import WorldState
from models.civilization import Civilization

# 导入文明Agent
from agents.civilization_agents.leader_agent import LeaderAgent
from agents.civilization_agents.diplomatic_agent import DiplomaticAgent
from agents.civilization_agents.military_agent import MilitaryAgent
from agents.civilization_agents.economic_agent import EconomicAgent
from agents.civilization_agents.cultural_agent import CulturalAgent
from agents.civilization_agents.population_agent import PopulationAgent

# 导入系统Agent
from agents.system_agents.world_engine import WorldEngineAgent
from agents.system_agents.historical_arbiter import HistoricalArbiterAgent
from agents.system_agents.balancer import BalancerAgent
from agents.system_agents.event_generator import EventGeneratorAgent
from agents.system_agents.observer import ObserverAgent
from agents.system_agents.narrative_constructor import NarrativeConstructorAgent

# 导入工具
from utils.logger import setup_logger, get_default_log_file

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='多Agent文明碰撞模拟系统')
    
    # 基本参数
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--output', type=str, help='输出目录')
    parser.add_argument('--turns', type=int, help='模拟回合数')
    parser.add_argument('--seed', type=int, help='随机种子')
    parser.add_argument('--verbose', action='store_true', help='详细输出模式')
    
    # 预设场景
    parser.add_argument('--scenario', type=str, choices=['default', 'rome_vs_carthage', 'mongol_conquest'], 
                        help='预设历史场景')
    
    # LLM配置
    parser.add_argument('--api-key', type=str, help='LLM API密钥')
    parser.add_argument('--model', type=str, help='LLM模型名称')
    
    return parser.parse_args()

def create_civilization(civ_config, llm_interface):
    """创建文明及其Agent"""
    civ_id = civ_config['id']
    civ_name = civ_config['name']
    
    # 创建文明对象
    civilization = Civilization(
        id=civ_id,
        name=civ_name
    )
    
    # 创建领导Agent
    leader = LeaderAgent(
        name=f"{civ_name}领导者",
        civilization_id=civ_id,
        leadership_style=civ_config.get('leadership_style', '平衡型'),
        llm_interface=llm_interface
    )
    
    # 创建外交Agent
    diplomat = DiplomaticAgent(
        name=f"{civ_name}外交官",
        civilization_id=civ_id,
        diplomatic_style=civ_config.get('diplomatic_style', '中立型'),
        llm_interface=llm_interface
    )
    
    # 创建军事Agent
    military = MilitaryAgent(
        name=f"{civ_name}军事顾问",
        civilization_id=civ_id,
        military_style=civ_config.get('military_style', '平衡型'),
        llm_interface=llm_interface
    )
    
    # 创建经济Agent
    economic = EconomicAgent(
        name=f"{civ_name}经济顾问",
        civilization_id=civ_id,
        economic_style=civ_config.get('economic_style', '混合型'),
        llm_interface=llm_interface
    )
    
    # 创建文化Agent
    cultural = CulturalAgent(
        name=f"{civ_name}文化顾问",
        civilization_id=civ_id,
        cultural_style=civ_config.get('cultural_style', '传统型'),
        llm_interface=llm_interface
    )
    
    # 创建人口Agent
    population = PopulationAgent(
        name=f"{civ_name}民众",
        civilization_id=civ_id,
        initial_population=civ_config.get('initial_population', 10000),
        llm_interface=llm_interface
    )
    
    # 将Agent添加到文明
    civilization.add_agent('leader', leader)
    civilization.add_agent('diplomat', diplomat)
    civilization.add_agent('military', military)
    civilization.add_agent('economic', economic)
    civilization.add_agent('cultural', cultural)
    civilization.add_agent('population', population)
    
    return civilization

def create_system_agents(config, llm_interface):
    """创建系统级Agent"""
    system_agents = {}
    
    # 创建世界引擎Agent
    world_engine = WorldEngineAgent(
        name="世界引擎",
        llm_interface=llm_interface
    )
    
    # 创建历史仲裁Agent
    if config.historical_accuracy:
        historical_arbiter = HistoricalArbiterAgent(
            name="历史仲裁者",
            llm_interface=llm_interface
        )
        # 加载历史参考数据
        # TODO: 实现历史参考数据加载
        system_agents['historical_arbiter'] = historical_arbiter
    
    # 创建平衡Agent
    if config.balance_enabled:
        balancer = BalancerAgent(
            name="平衡者",
            llm_interface=llm_interface
        )
        system_agents['balancer'] = balancer
    
    # 创建事件生成Agent
    event_generator = EventGeneratorAgent(
        name="事件生成器",
        llm_interface=llm_interface
    )
    
    # 创建观察Agent
    observer = ObserverAgent(
        name="观察者",
        llm_interface=llm_interface
    )
    
    # 创建叙事构建Agent
    narrative_constructor = NarrativeConstructorAgent(
        name="叙事构建者",
        llm_interface=llm_interface
    )
    narrative_constructor.set_narrative_style(config.narrative_style)
    
    # 添加到系统Agent字典
    system_agents['world_engine'] = world_engine
    system_agents['event_generator'] = event_generator
    system_agents['observer'] = observer
    system_agents['narrative_constructor'] = narrative_constructor
    
    return system_agents

def run_simulation(config, llm_interface, logger):
    """运行模拟"""
    logger.info("开始初始化模拟...")
    
    # 创建文明
    civilizations = {}
    for civ_config in config.civilizations:
        civ = create_civilization(civ_config, llm_interface)
        civilizations[civ.id] = civ
        logger.info(f"创建文明: {civ.name} (ID: {civ.id})")
    
    # 创建系统Agent
    system_agents = create_system_agents(config, llm_interface)
    logger.info(f"创建系统Agent: {', '.join(system_agents.keys())}")
    
    # 初始化世界
    world_engine = system_agents['world_engine']
    world_state = world_engine.initialize_world(config)
    logger.info(f"初始化世界状态: 大小 {config.world_size['width']}x{config.world_size['height']}")
    
    # 初始化观察者
    observer = system_agents['observer']
    observer.initialize([civ.id for civ in civilizations.values()])
    
    # 初始化文明状态
    for civ_id, civ in civilizations.items():
        # 设置初始资源
        initial_state = {
            'name': civ.name,
            'population': civ.get_agent('population').population,
            'resources': config.starting_resources.copy(),
            'military_power': 100,  # 初始军事力量
            'economic_power': 100,  # 初始经济力量
            'technology_level': 1,  # 初始技术水平
            'cultural_influence': 50,  # 初始文化影响力
            'happiness': 50,  # 初始幸福度
            'diplomatic_relations': {other_id: 0 for other_id in civilizations if other_id != civ_id}  # 初始外交关系
        }
        world_state.update_civilization_state(civ_id, initial_state)
    
    logger.info("模拟初始化完成，开始运行...")
    
    # 主模拟循环
    for turn in range(1, config.max_turns + 1):
        logger.info(f"===== 回合 {turn}/{config.max_turns} =====")
        
        # 更新世界状态的当前回合
        world_state.current_turn = turn
        
        # 1. 世界引擎更新
        logger.debug("世界引擎更新中...")
        world_state = world_engine.process(world_state)
        
        # 2. 收集各文明顾问的建议
        all_advice = {}
        for civ_id, civ in civilizations.items():
            logger.debug(f"收集 {civ.name} 的顾问建议...")
            
            # 获取各顾问的建议
            diplomatic_advice = civ.get_agent('diplomat').provide_advice(world_state)
            military_advice = civ.get_agent('military').provide_advice(world_state)
            economic_advice = civ.get_agent('economic').provide_advice(world_state)
            cultural_advice = civ.get_agent('cultural').provide_advice(world_state)
            population_feedback = civ.get_agent('population').provide_advice(world_state)
            
            all_advice[civ_id] = {
                'diplomatic': diplomatic_advice,
                'military': military_advice,
                'economic': economic_advice,
                'cultural': cultural_advice,
                'population': population_feedback
            }
        
        # 3. 领导者做出决策
        decisions = {}
        for civ_id, civ in civilizations.items():
            logger.debug(f"{civ.name} 领导者正在决策...")
            
            advice = all_advice[civ_id]
            leader_decision = civ.get_agent('leader').make_decision(
                world_state,
                advice['diplomatic'],
                advice['military'],
                advice['economic'],
                advice['cultural'],
                advice['population']
            )
            
            decisions[civ_id] = leader_decision
            logger.info(f"{civ.name} 决策: {leader_decision.get('summary', '无决策摘要')}")
        
        # 4. 执行决策和文明间互动
        interaction_results = {}
        for civ_id, decision in decisions.items():
            civ = civilizations[civ_id]
            
            # 处理外交互动
            if 'diplomatic_actions' in decision:
                for action in decision['diplomatic_actions']:
                    target_id = action.get('target_civilization')
                    if target_id and target_id in civilizations:
                        logger.debug(f"{civ.name} 与 {civilizations[target_id].name} 进行外交互动")
                        
                        # 执行外交谈判
                        result = civ.get_agent('diplomat').negotiate(
                            world_state,
                            target_id,
                            action.get('topic', '一般关系'),
                            action.get('stance', '中立')
                        )
                        
                        # 记录互动结果
                        if civ_id not in interaction_results:
                            interaction_results[civ_id] = {}
                        
                        interaction_results[civ_id][target_id] = result
            
            # 处理军事行动
            if 'military_actions' in decision:
                for action in decision['military_actions']:
                    action_type = action.get('type')
                    if action_type:
                        logger.debug(f"{civ.name} 执行军事行动: {action_type}")
                        civ.get_agent('military').execute_order(action, world_state)
            
            # 处理经济行动
            if 'economic_actions' in decision:
                for action in decision['economic_actions']:
                    action_type = action.get('type')
                    if action_type:
                        logger.debug(f"{civ.name} 执行经济行动: {action_type}")
                        civ.get_agent('economic').execute_order(action, world_state)
            
            # 处理文化行动
            if 'cultural_actions' in decision:
                for action in decision['cultural_actions']:
                    action_type = action.get('type')
                    if action_type:
                        logger.debug(f"{civ.name} 执行文化行动: {action_type}")
                        civ.get_agent('cultural').execute_order(action, world_state)
        
        # 5. 生成随机事件
        events = system_agents['event_generator'].process(world_state, civilizations=civilizations)
        if events:
            logger.info(f"本回合发生 {len(events)} 个事件")
            for event in events:
                logger.info(f"事件: {event.get('title', '未命名事件')}")
        
        # 6. 应用平衡措施
        if 'balancer' in system_agents:
            logger.debug("应用平衡措施...")
            world_state = system_agents['balancer'].process(world_state)
        
        # 7. 历史评估
        historical_assessment = None
        if 'historical_arbiter' in system_agents:
            logger.debug("进行历史评估...")
            historical_assessment = system_agents['historical_arbiter'].process(world_state)
        
        # 8. 更新人口
        for civ_id, civ in civilizations.items():
            logger.debug(f"更新 {civ.name} 人口...")
            civ.get_agent('population').update_population(world_state)
        
        # 9. 记录本回合数据
        observer.record_turn(
            turn,
            world_state,
            civilizations,
            decisions,
            interaction_results,
            events,
            historical_assessment
        )
        
        # 10. 生成回合叙事
        turn_data = observer.get_turn_data(turn)
        narrative = system_agents['narrative_constructor'].generate_turn_narrative(turn_data)
        logger.info(f"回合叙事:\n{narrative}")
        
        # 11. 定期保存状态
        if turn % config.save_interval == 0 or turn == config.max_turns:
            save_dir = os.path.join(config.output_dir, f"turn_{turn}")
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 保存世界状态
            with open(os.path.join(save_dir, "world_state.json"), 'w', encoding='utf-8') as f:
                json.dump(world_state.to_dict(), f, indent=4)
            
            # 保存回合叙事
            with open(os.path.join(save_dir, "narrative.txt"), 'w', encoding='utf-8') as f:
                f.write(narrative)
            
            logger.info(f"保存回合 {turn} 状态到 {save_dir}")
    
    # 生成完整历史叙事
    logger.info("生成完整历史叙事...")
    full_history = observer.get_full_history()
    full_narrative = system_agents['narrative_constructor'].generate_full_narrative(full_history)
    
    # 保存完整历史叙事
    narrative_file = os.path.join(config.output_dir, "full_narrative.txt")
    with open(narrative_file, 'w', encoding='utf-8') as f:
        f.write(full_narrative)
    
    logger.info(f"模拟完成! 完整历史叙事已保存到 {narrative_file}")
    
    return {
        'world_state': world_state,
        'civilizations': civilizations,
        'history': full_history,
        'narrative': full_narrative
    }

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置输出目录
    output_dir = args.output
    if not output_dir:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join('output', f'simulation_{timestamp}')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 设置日志
    log_file = os.path.join(output_dir, 'simulation.log')
    logger = setup_logger('civilization_sim', log_file, args.verbose)
    
    logger.info("多Agent文明碰撞模拟系统启动")
    
    # 加载配置
    if args.config:
        logger.info(f"从文件加载配置: {args.config}")
        config = SimulationConfig.load_from_file(args.config)
    elif args.scenario:
        logger.info(f"使用预设场景: {args.scenario}")
        if args.scenario == 'default':
            config = SimulationConfig.create_default_config()
        else:
            config = SimulationConfig.create_historical_config(args.scenario)
    else:
        logger.info("使用默认配置")
        config = SimulationConfig()
    
    # 覆盖配置参数
    if args.turns:
        config.max_turns = args.turns
    if args.seed:
        config.seed = args.seed
    if args.output:
        config.output_dir = output_dir
    config.verbose = args.verbose
    
    # 初始化LLM配置
    llm_config = LLMConfig(
        api_key=args.api_key,
        model=args.model
    )
    
    # 创建LLM接口
    llm_interface = LLMInterface(llm_config)
    
    try:
        # 运行模拟
        results = run_simulation(config, llm_interface, logger)
        
        logger.info("模拟成功完成!")
        return 0
    except Exception as e:
        logger.error(f"模拟过程中发生错误: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 