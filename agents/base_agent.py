from abc import ABC, abstractmethod
from llm.llm_interface import LLMInterface

class BaseAgent(ABC):
    """所有Agent的基类"""
    
    def __init__(self, name, civilization_id=None, llm_interface=None):
        self.name = name
        self.civilization_id = civilization_id  # None表示系统级Agent
        self.llm_interface = llm_interface or LLMInterface()
        self.memory = []  # Agent的记忆/历史
        
    def add_to_memory(self, event):
        """添加事件到Agent记忆"""
        self.memory.append(event)
        # 可能需要限制记忆大小或实现更复杂的记忆管理
        
    def get_memory_context(self, limit=10):
        """获取记忆上下文用于LLM提示"""
        return self.memory[-limit:] if len(self.memory) > limit else self.memory
    
    @abstractmethod
    def process(self, world_state, **kwargs):
        """处理当前世界状态并做出决策"""
        pass
    
    def generate_decision(self, prompt, context=None):
        """使用LLM生成决策"""
        if context is None:
            context = self.get_memory_context()
        
        return self.llm_interface.generate_response(prompt, context) 