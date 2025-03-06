from agents.base_agent import BaseAgent
import random

class BalancerAgent(BaseAgent):
    """平衡文明间力量差距的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.balance_threshold = 2.0  # 力量差距阈值，超过此值触发平衡
        self.balance_intensity = 0.2  # 平衡强度，0-1之间
        self.balance_history = []  # 平衡历史记录
        
    def balance_world(self, world_state):
        """平衡世界状态"""
        # 分析文明力量差距
        power_analysis = self._analyze_civilization_power(world_state)
        
        # 检查是否需要平衡
        if power_analysis['max_power_ratio'] > self.balance_threshold:
            # 执行平衡操作
            balanced_state = self._apply_balance_measures(world_state, power_analysis)
            
            # 记录平衡操作
            self.balance_history.append({
                'turn': world_state.current_turn,
                'before': power_analysis,
                'measures_applied': True,
                'after': self._analyze_civilization_power(balanced_state)
            })
            
            return balanced_state
        else:
            # 记录无需平衡
            self.balance_history.append({
                'turn': world_state.current_turn,
                'analysis': power_analysis,
                'measures_applied': False
            })
            
            return world_state
    
    def process(self, world_state, **kwargs):
        """处理当前回合的平衡操作"""
        return self.balance_world(world_state)
    
    def _analyze_civilization_power(self, world_state):
        """分析各文明的力量"""
        power_scores = {}
        
        for civ_id, state in world_state.civilization_states.items():
            # 计算综合力量分数
            military = state.get('military_power', 0)
            economy = state.get('economic_power', 0)
            technology = state.get('technology_level', 0)
            population = state.get('population', 0) / 10000  # 归一化人口
            
            # 简单加权计算
            power_score = (military * 0.4 + economy * 0.3 + technology * 0.2 + population * 0.1)
            power_scores[civ_id] = power_score
        
        # 找出最强和最弱的文明
        if not power_scores:
            return {
                'power_scores': {},
                'strongest': None,
                'weakest': None,
                'max_power_ratio': 1.0
            }
            
        strongest = max(power_scores.items(), key=lambda x: x[1])
        weakest = min(power_scores.items(), key=lambda x: x[1])
        
        # 计算最大力量比率
        max_power_ratio = strongest[1] / max(weakest[1], 1)  # 避免除以零
        
        return {
            'power_scores': power_scores,
            'strongest': strongest[0],
            'weakest': weakest[0],
            'max_power_ratio': max_power_ratio
        }
    
    def _apply_balance_measures(self, world_state, power_analysis):
        """应用平衡措施"""
        strongest_civ = power_analysis['strongest']
        weakest_civ = power_analysis['weakest']
        
        if strongest_civ is None or weakest_civ is None:
            return world_state
        
        # 获取文明状态
        strongest_state = world_state.get_civilization_state(strongest_civ)
        weakest_state = world_state.get_civilization_state(weakest_civ)
        
        # 平衡措施1: 减弱最强文明的军事力量
        if 'military_power' in strongest_state:
            reduction = strongest_state['military_power'] * self.balance_intensity
            strongest_state['military_power'] -= reduction
            
            # 添加平衡事件
            world_state.add_event({
                'type': 'balance',
                'subtype': 'military_reduction',
                'target': strongest_civ,
                'amount': reduction,
                'reason': 'Internal conflicts weakened military'
            })
        
        # 平衡措施2: 增强最弱文明的资源
        if 'resources' in weakest_state:
            for resource, amount in weakest_state['resources'].items():
                increase = amount * self.balance_intensity
                weakest_state['resources'][resource] += increase
            
            # 添加平衡事件
            world_state.add_event({
                'type': 'balance',
                'subtype': 'resource_boost',
                'target': weakest_civ,
                'reason': 'Discovery of new resource deposits'
            })
        
        # 平衡措施3: 随机技术突破给最弱文明
        if random.random() < 0.3:  # 30%几率
            if 'technology_level' in weakest_state:
                tech_boost = weakest_state['technology_level'] * 0.1
                weakest_state['technology_level'] += tech_boost
                
                # 添加平衡事件
                world_state.add_event({
                    'type': 'balance',
                    'subtype': 'technology_breakthrough',
                    'target': weakest_civ,
                    'amount': tech_boost,
                    'reason': 'Unexpected technological breakthrough'
                })
        
        # 更新文明状态
        world_state.update_civilization_state(strongest_civ, strongest_state)
        world_state.update_civilization_state(weakest_civ, weakest_state)
        
        return world_state 