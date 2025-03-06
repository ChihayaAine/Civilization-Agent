from agents.base_agent import BaseAgent
from llm.prompt_templates import TURN_NARRATIVE_TEMPLATE, FULL_NARRATIVE_TEMPLATE

class NarrativeConstructorAgent(BaseAgent):
    """将模拟结果转化为历史叙事的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.narrative_style = "historical"  # 可选: historical, dramatic, analytical
        self.narratives = {}  # 存储生成的叙事
        
    def set_narrative_style(self, style):
        """设置叙事风格"""
        valid_styles = ["historical", "dramatic", "analytical", "journalistic"]
        if style in valid_styles:
            self.narrative_style = style
        else:
            print(f"Warning: Invalid narrative style '{style}'. Using default 'historical'.")
    
    def generate_turn_narrative(self, turn_data):
        """生成单回合叙事"""
        if not turn_data:
            return "No data available for this turn."
        
        turn = turn_data.get('world_state', {}).get('current_turn', 0)
        
        # 准备叙事提示
        prompt = TURN_NARRATIVE_TEMPLATE.format(
            turn=turn,
            narrative_style=self.narrative_style,
            civilization_states=turn_data.get('civilization_states', {}),
            decisions=turn_data.get('decisions', {}),
            events=turn_data.get('events', []),
            interaction_results=turn_data.get('interaction_results', {})
        )
        
        # 生成叙事
        narrative = self.generate_decision(prompt)
        
        # 存储叙事
        self.narratives[turn] = narrative
        
        return narrative
    
    def generate_full_narrative(self, history_data):
        """生成完整历史叙事"""
        if not history_data:
            return "No historical data available."
        
        # 准备关键转折点和重要事件
        key_turns = self._identify_key_turns(history_data)
        important_events = self._extract_important_events(history_data)
        civilization_arcs = self._construct_civilization_arcs(history_data)
        
        # 准备叙事提示
        prompt = FULL_NARRATIVE_TEMPLATE.format(
            total_turns=max(history_data.keys()),
            narrative_style=self.narrative_style,
            key_turns=key_turns,
            important_events=important_events,
            civilization_arcs=civilization_arcs
        )
        
        # 生成完整叙事
        full_narrative = self.generate_decision(prompt, context=None)  # 不使用上下文，避免token限制
        
        # 存储完整叙事
        self.narratives['full'] = full_narrative
        
        return full_narrative
    
    def process(self, world_state, **kwargs):
        """处理当前回合的叙事生成"""
        turn_data = kwargs.get('turn_data', {})
        return self.generate_turn_narrative(turn_data)
    
    def _identify_key_turns(self, history_data):
        """识别历史中的关键转折点"""
        key_turns = []
        
        # 简单示例：每10回合选择一个关键回合，以及第一回合和最后回合
        all_turns = sorted(history_data.keys())
        if not all_turns:
            return key_turns
            
        # 添加第一回合
        key_turns.append(all_turns[0])
        
        # 添加每10回合
        for turn in all_turns:
            if turn % 10 == 0:
                key_turns.append(turn)
        
        # 添加最后回合
        if all_turns[-1] not in key_turns:
            key_turns.append(all_turns[-1])
        
        # 去重并排序
        key_turns = sorted(set(key_turns))
        
        # 提取关键回合数据
        key_turn_data = []
        for turn in key_turns:
            turn_data = history_data.get(turn, {})
            key_turn_data.append({
                'turn': turn,
                'civilization_states': turn_data.get('civilization_states', {}),
                'events': turn_data.get('events', [])
            })
        
        return key_turn_data
    
    def _extract_important_events(self, history_data):
        """提取重要历史事件"""
        important_events = []
        
        for turn, turn_data in history_data.items():
            for event in turn_data.get('events', []):
                # 判断事件重要性的逻辑
                if event.get('scale') in ['major', 'crisis'] or 'balance' in event.get('type', ''):
                    event_copy = event.copy()
                    event_copy['turn'] = turn
                    important_events.append(event_copy)
        
        return important_events
    
    def _construct_civilization_arcs(self, history_data):
        """构建各文明的发展轨迹"""
        # 识别所有文明
        all_civs = set()
        for turn_data in history_data.values():
            all_civs.update(turn_data.get('civilization_states', {}).keys())
        
        civilization_arcs = {}
        
        for civ_id in all_civs:
            # 收集该文明在各回合的状态
            civ_states = []
            for turn in sorted(history_data.keys()):
                turn_data = history_data[turn]
                if civ_id in turn_data.get('civilization_states', {}):
                    state = turn_data['civilization_states'][civ_id].copy()
                    state['turn'] = turn
                    civ_states.append(state)
            
            # 如果有足够数据，构建发展轨迹
            if len(civ_states) >= 2:
                start_state = civ_states[0]
                end_state = civ_states[-1]
                
                # 计算关键指标变化
                metrics = ['population', 'military_power', 'economic_power', 'technology_level', 'cultural_influence']
                changes = {}
                
                for metric in metrics:
                    if metric in start_state and metric in end_state:
                        start_value = start_state.get(metric, 0)
                        end_value = end_state.get(metric, 0)
                        if start_value > 0:
                            percent_change = (end_value - start_value) / start_value * 100
                        else:
                            percent_change = 0 if end_value == 0 else 100
                        
                        changes[metric] = {
                            'start': start_value,
                            'end': end_value,
                            'percent_change': percent_change
                        }
                
                # 构建文明轨迹
                civilization_arcs[civ_id] = {
                    'name': start_state.get('name', f'Civilization {civ_id}'),
                    'start_state': start_state,
                    'end_state': end_state,
                    'metric_changes': changes,
                    'total_turns': len(civ_states)
                }
        
        return civilization_arcs 