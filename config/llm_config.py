class LLMConfig:
    """LLM配置类"""
    
    def __init__(self, **kwargs):
        self.client_type = kwargs.get('client_type', 'openai')  # 默认使用OpenAI
        self.api_key = kwargs.get('api_key', '')  # API密钥
        self.model = kwargs.get('model', 'gpt-4')  # 默认模型
        self.temperature = kwargs.get('temperature', 0.7)  # 温度参数
        self.max_tokens = kwargs.get('max_tokens', 1000)  # 最大token数
        self.system_prompt = kwargs.get('system_prompt', 
            """你是一个智能Agent，负责在多Agent文明模拟系统中做出决策。
            请基于提供的信息和上下文，做出符合你角色的决策。
            你的回答应该简洁明了，直接针对问题给出具体的建议或决策。"""
        ) 