from agents.base_agent import BaseAgent

class ObserverAgent(BaseAgent):
    """收集数据并生成分析报告的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.history = {}  # 按回合存储的历史数据
        self.metrics = {}  # 按文明ID存储的指标数据
        self.tracked_civilizations = set()  # 跟踪的文明ID集合
        
    def initialize(self, civilization_ids):
        """初始化观察者，设置要跟踪的文明"""
        self.tracked_civilizations = set(civilization_ids)
        
        # 为每个文明初始化指标数据
        for civ_id in civilization_ids:
            self.metrics[civ_id] = {
                'population': [],
                'military_power': [],
                'economic_power': [],
                'technology_level': [],
                'cultural_influence': [],
                'happiness': [],
                'diplomatic_relations': {}
            }
    
    def record_turn(self, turn, world_state, civilizations, decisions, interaction_results, events, historical_assessment):
        """记录当前回合的数据"""
        turn_data = {
            'world_state': world_state.to_dict(),
            'civilization_states': {},
            'decisions': decisions,
            'interaction_results': interaction_results,
            'events': events,
            'historical_assessment': historical_assessment
        }
        
        # 记录每个文明的状态
        for civ_id, civilization in civilizations.items():
            if civ_id in self.tracked_civilizations:
                civ_state = world_state.get_civilization_state(civ_id)
                turn_data['civilization_states'][civ_id] = civ_state
                
                # 更新指标数据
                self._update_metrics(civ_id, civ_state)
        
        # 存储回合数据
        self.history[turn] = turn_data
    
    def get_turn_data(self, turn):
        """获取特定回合的数据"""
        return self.history.get(turn, {})
    
    def get_full_history(self):
        """获取完整历史数据"""
        return self.history
    
    def get_civilization_metrics(self, civ_id):
        """获取特定文明的指标数据"""
        return self.metrics.get(civ_id, {})
    
    def generate_report(self, start_turn, end_turn):
        """生成特定时期的分析报告"""
        report_data = {
            'period': {'start': start_turn, 'end': end_turn},
            'civilizations': {}
        }
        
        # 收集每个文明在此期间的数据
        for civ_id in self.tracked_civilizations:
            civ_data = {
                'metrics': self._extract_metrics(civ_id, start_turn, end_turn),
                'key_events': self._extract_key_events(civ_id, start_turn, end_turn),
                'decisions': self._extract_decisions(civ_id, start_turn, end_turn)
            }
            report_data['civilizations'][civ_id] = civ_data
        
        # 添加世界级事件
        report_data['world_events'] = self._extract_world_events(start_turn, end_turn)
        
        return report_data
    
    def process(self, world_state, **kwargs):
        """处理当前回合的观察任务"""
        # Observer主要是被动记录，不主动处理
        return None
    
    def _update_metrics(self, civ_id, civ_state):
        """更新文明指标数据"""
        metrics = self.metrics[civ_id]
        
        # 更新基本指标
        metrics['population'].append(civ_state.get('population', 0))
        metrics['military_power'].append(civ_state.get('military_power', 0))
        metrics['economic_power'].append(civ_state.get('economic_power', 0))
        metrics['technology_level'].append(civ_state.get('technology_level', 0))
        metrics['cultural_influence'].append(civ_state.get('cultural_influence', 0))
        metrics['happiness'].append(civ_state.get('happiness', 50))
        
        # 更新外交关系
        diplomatic_relations = civ_state.get('diplomatic_relations', {})
        for other_civ, relation in diplomatic_relations.items():
            if other_civ not in metrics['diplomatic_relations']:
                metrics['diplomatic_relations'][other_civ] = []
            metrics['diplomatic_relations'][other_civ].append(relation)
    
    def _extract_metrics(self, civ_id, start_turn, end_turn):
        """提取特定时期的指标数据"""
        metrics = self.metrics[civ_id]
        period_length = end_turn - start_turn + 1
        
        # 提取基本指标
        extracted_metrics = {}
        for metric_name, values in metrics.items():
            if metric_name != 'diplomatic_relations':
                if len(values) >= end_turn:
                    extracted_metrics[metric_name] = values[start_turn-1:end_turn]
        
        # 提取外交关系
        extracted_metrics['diplomatic_relations'] = {}
        for other_civ, relations in metrics['diplomatic_relations'].items():
            if len(relations) >= end_turn:
                extracted_metrics['diplomatic_relations'][other_civ] = relations[start_turn-1:end_turn]
        
        return extracted_metrics
    
    def _extract_key_events(self, civ_id, start_turn, end_turn):
        """提取特定时期的关键事件"""
        key_events = []
        
        for turn in range(start_turn, end_turn + 1):
            if turn in self.history:
                turn_data = self.history[turn]
                
                # 提取影响该文明的事件
                for event in turn_data.get('events', []):
                    if event.get('target_civilization') == civ_id:
                        key_events.append(event)
        
        return key_events
    
    def _extract_decisions(self, civ_id, start_turn, end_turn):
        """提取特定时期的决策"""
        decisions = []
        
        for turn in range(start_turn, end_turn + 1):
            if turn in self.history:
                turn_data = self.history[turn]
                
                # 提取该文明的决策
                if civ_id in turn_data.get('decisions', {}):
                    decision = {
                        'turn': turn,
                        'content': turn_data['decisions'][civ_id]
                    }
                    decisions.append(decision)
        
        return decisions
    
    def _extract_world_events(self, start_turn, end_turn):
        """提取特定时期的世界级事件"""
        world_events = []
        
        for turn in range(start_turn, end_turn + 1):
            if turn in self.history:
                turn_data = self.history[turn]
                
                # 提取世界级事件（没有特定目标文明的事件）
                for event in turn_data.get('events', []):
                    if 'target_civilization' not in event:
                        world_events.append(event)
        
        return world_events 