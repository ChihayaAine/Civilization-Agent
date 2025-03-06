from agents.base_agent import BaseAgent
from llm.prompt_templates import EVENT_GENERATION_TEMPLATE
import random

class EventGeneratorAgent(BaseAgent):
    """创造随机事件的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.event_types = [
            'political', 'economic', 'military', 'cultural', 
            'technological', 'religious', 'social'
        ]
        self.event_probabilities = {
            'minor': 0.15,  # 每回合15%几率发生小事件
            'major': 0.05,  # 每回合5%几率发生大事件
            'crisis': 0.02  # 每回合2%几率发生危机事件
        }
        self.generated_events = []  # 记录生成的事件
        
    def generate_events(self, world_state, civilizations):
        """生成当前回合的随机事件"""
        events = []
        
        # 为每个文明生成可能的事件
        for civ_id, civilization in civilizations.items():
            # 检查是否生成各类事件
            for event_scale, probability in self.event_probabilities.items():
                if random.random() < probability:
                    event = self._generate_event(world_state, civilization, event_scale)
                    if event:
                        events.append(event)
                        # 添加到世界状态
                        world_state.add_event(event)
        
        # 记录生成的事件
        self.generated_events.extend(events)
        
        return events
    
    def process(self, world_state, **kwargs):
        """处理当前回合的事件生成"""
        civilizations = kwargs.get('civilizations', {})
        return self.generate_events(world_state, civilizations)
    
    def _generate_event(self, world_state, civilization, event_scale):
        """生成特定规模的事件"""
        # 选择事件类型
        event_type = random.choice(self.event_types)
        
        # 获取文明状态
        civ_state = world_state.get_civilization_state(civilization.id)
        
        # 使用LLM生成事件
        prompt = EVENT_GENERATION_TEMPLATE.format(
            civilization_name=civilization.name,
            civilization_state=civ_state,
            event_type=event_type,
            event_scale=event_scale,
            current_turn=world_state.current_turn
        )
        
        event_response = self.generate_structured_response(
            prompt,
            response_format={
                'title': 'Event title',
                'description': 'Detailed description of the event',
                'effects': {
                    'political': 'Political effects',
                    'economic': 'Economic effects',
                    'military': 'Military effects',
                    'cultural': 'Cultural effects',
                    'population': 'Population effects'
                },
                'duration': 'How many turns the event effects will last'
            }
        )
        
        # 构建事件对象
        event = {
            'type': 'random_event',
            'subtype': event_type,
            'scale': event_scale,
            'target_civilization': civilization.id,
            'title': event_response.get('title', f'{event_scale.capitalize()} {event_type} event'),
            'description': event_response.get('description', ''),
            'effects': event_response.get('effects', {}),
            'duration': int(event_response.get('duration', 1)),
            'turns_remaining': int(event_response.get('duration', 1))
        }
        
        return event 