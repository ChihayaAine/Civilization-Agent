from models.civilization import Civilization
from agents.system_agents.world_engine import WorldEngineAgent
from agents.system_agents.historical_arbiter import HistoricalArbiterAgent
from agents.system_agents.balancer import BalancerAgent
from agents.system_agents.event_generator import EventGeneratorAgent
from agents.system_agents.observer import ObserverAgent
from agents.system_agents.narrative_constructor import NarrativeConstructorAgent

class Simulation:
    """模拟主循环控制器"""
    
    def __init__(self, config):
        self.config = config
        self.current_turn = 0
        self.max_turns = config.max_turns
        self.civilizations = {}
        self.world_state = None
        
        # 初始化系统级Agent
        self.world_engine = WorldEngineAgent("World Engine")
        self.historical_arbiter = HistoricalArbiterAgent("Historical Arbiter")
        self.balancer = BalancerAgent("Balancer")
        self.event_generator = EventGeneratorAgent("Event Generator")
        self.observer = ObserverAgent("Observer")
        self.narrative_constructor = NarrativeConstructorAgent("Narrative Constructor")
        
    def initialize(self):
        """初始化模拟"""
        # 创建初始世界状态
        self.world_state = self.world_engine.initialize_world(self.config)
        
        # 创建文明
        for civ_config in self.config.civilizations:
            civ = Civilization(
                id=civ_config.id,
                name=civ_config.name,
                initial_state=civ_config.initial_state
            )
            self.civilizations[civ.id] = civ
            
        # 初始化观察者
        self.observer.initialize(self.civilizations.keys())
        
    def run(self):
        """运行完整模拟"""
        self.initialize()
        
        while self.current_turn < self.max_turns:
            self.run_turn()
            
        # 生成最终叙事和报告
        final_narrative = self.narrative_constructor.generate_full_narrative(
            self.observer.get_full_history()
        )
        
        return final_narrative
    
    def run_turn(self):
        """运行单个回合"""
        self.current_turn += 1
        print(f"Starting turn {self.current_turn}")
        
        # 1. 世界级Agent更新环境
        self.world_state = self.world_engine.update_environment(self.world_state)
        
        # 2. 生成随机事件
        events = self.event_generator.generate_events(self.world_state, self.civilizations)
        for event in events:
            self.apply_event(event)
        
        # 3. 各文明内部决策
        civilization_decisions = {}
        for civ_id, civ in self.civilizations.items():
            decisions = civ.make_decisions(self.world_state)
            civilization_decisions[civ_id] = decisions
        
        # 4. 文明间交互
        interaction_results = self.process_civilization_interactions(civilization_decisions)
        
        # 5. 执行决策结果
        self.apply_decisions(civilization_decisions, interaction_results)
        
        # 6. 系统级Agent评估并调整
        self.world_state = self.balancer.balance_world(self.world_state)
        historical_assessment = self.historical_arbiter.assess(self.world_state)
        
        # 7. 更新文明状态
        for civ_id, civ in self.civilizations.items():
            civ.update_state(self.world_state)
        
        # 8. 记录历史
        self.observer.record_turn(
            self.current_turn, 
            self.world_state,
            self.civilizations,
            civilization_decisions,
            interaction_results,
            events,
            historical_assessment
        )
        
        # 生成当前回合叙事
        turn_narrative = self.narrative_constructor.generate_turn_narrative(
            self.observer.get_turn_data(self.current_turn)
        )
        
        print(f"Turn {self.current_turn} completed")
        print(turn_narrative)
        
    def apply_event(self, event):
        """应用随机事件到世界和文明"""
        # 实现事件应用逻辑
        pass
        
    def process_civilization_interactions(self, decisions):
        """处理文明间的交互"""
        # 实现文明间交互逻辑
        return {}
        
    def apply_decisions(self, decisions, interaction_results):
        """应用所有决策的结果到世界状态"""
        # 实现决策应用逻辑
        pass 