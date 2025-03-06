from agents.civilization_agents.leader_agent import LeaderAgent
from agents.civilization_agents.diplomatic_agent import DiplomaticAgent
from agents.civilization_agents.military_agent import MilitaryAgent
from agents.civilization_agents.economic_agent import EconomicAgent
from agents.civilization_agents.cultural_agent import CulturalAgent
from agents.civilization_agents.population_agent import PopulationAgent

class Civilization:
    """文明模型，包含所有文明级Agent"""
    
    def __init__(self, id, name, initial_state):
        self.id = id
        self.name = name
        self.state = initial_state
        
        # 创建文明内部Agent
        self.leader = LeaderAgent(
            name=initial_state.get("leader_name", f"{name} Leader"),
            civilization_id=id,
            leadership_style=initial_state.get("leadership_style", "balanced")
        )
        
        self.diplomatic_agent = DiplomaticAgent(
            name=initial_state.get("diplomat_name", f"{name} Diplomat"),
            civilization_id=id,
            diplomatic_style=initial_state.get("diplomatic_style", "balanced")
        )
        
        self.military_agent = MilitaryAgent(
            name=initial_state.get("military_leader_name", f"{name} General"),
            civilization_id=id,
            military_style=initial_state.get("military_style", "balanced")
        )
        
        self.economic_agent = EconomicAgent(
            name=initial_state.get("economic_leader_name", f"{name} Treasurer"),
            civilization_id=id,
            economic_style=initial_state.get("economic_style", "balanced")
        )
        
        self.cultural_agent = CulturalAgent(
            name=initial_state.get("cultural_leader_name", f"{name} Cultural Minister"),
            civilization_id=id,
            cultural_style=initial_state.get("cultural_style", "balanced")
        )
        
        self.population_agent = PopulationAgent(
            name=f"{name} Population",
            civilization_id=id,
            initial_population=initial_state.get("population", 1000000)
        )
        
        # 注册顾问到领导Agent
        self.leader.register_advisor("diplomatic", self.diplomatic_agent)
        self.leader.register_advisor("military", self.military_agent)
        self.leader.register_advisor("economic", self.economic_agent)
        self.leader.register_advisor("cultural", self.cultural_agent)
        self.leader.register_advisor("population", self.population_agent)
        
    def make_decisions(self, world_state):
        """文明内部决策过程"""
        # 领导Agent做出决策
        leader_decision = self.leader.process(world_state)
        
        # 基于领导决策，各专业Agent执行具体行动
        diplomatic_actions = self.diplomatic_agent.process(world_state, leader_decision=leader_decision)
        military_actions = self.military_agent.process(world_state, leader_decision=leader_decision)
        economic_actions = self.economic_agent.process(world_state, leader_decision=leader_decision)
        cultural_actions = self.cultural_agent.process(world_state, leader_decision=leader_decision)
        
        # 收集所有决策和行动
        decisions = {
            "leader": leader_decision,
            "diplomatic": diplomatic_actions,
            "military": military_actions,
            "economic": economic_actions,
            "cultural": cultural_actions
        }
        
        return decisions
        
    def update_state(self, world_state):
        """更新文明状态"""
        # 从世界状态中提取与本文明相关的更新
        civ_state = world_state.get_civilization_state(self.id)
        if civ_state:
            self.state.update(civ_state)
            
        # 更新人口状态
        self.population_agent.update_population(self.state, world_state) 