import os
import json
from config.llm_config import LLMConfig

class LLMInterface:
    """大语言模型接口"""
    
    def __init__(self, config=None):
        self.config = config or LLMConfig()
        self.setup_llm_client()
        
    def setup_llm_client(self):
        """设置LLM客户端"""
        # 这里实现与特定LLM API的连接
        # 例如OpenAI、Claude等
        self.client_type = self.config.client_type
        
        if self.client_type == "openai":
            import openai
            openai.api_key = os.environ.get("OPENAI_API_KEY") or self.config.api_key
            self.client = openai
        elif self.client_type == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY") or self.config.api_key
            )
        # 可以添加更多LLM提供商
        
    def generate_response(self, prompt, context=None, **kwargs):
        """生成LLM响应"""
        full_prompt = self._build_full_prompt(prompt, context)
        
        try:
            if self.client_type == "openai":
                response = self.client.ChatCompletion.create(
                    model=kwargs.get("model", self.config.model),
                    messages=[{"role": "system", "content": self.config.system_prompt},
                              {"role": "user", "content": full_prompt}],
                    temperature=kwargs.get("temperature", self.config.temperature),
                    max_tokens=kwargs.get("max_tokens", self.config.max_tokens)
                )
                return response.choices[0].message.content
                
            elif self.client_type == "anthropic":
                response = self.client.messages.create(
                    model=kwargs.get("model", self.config.model),
                    system=self.config.system_prompt,
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=kwargs.get("temperature", self.config.temperature),
                    max_tokens=kwargs.get("max_tokens", self.config.max_tokens)
                )
                return response.content[0].text
                
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return f"Error: {str(e)}"
    
    def generate_structured_response(self, prompt, context=None, response_format=None, **kwargs):
        """生成结构化的LLM响应（JSON格式）"""
        if response_format is None:
            response_format = {}
            
        full_prompt = self._build_full_prompt(prompt, context)
        full_prompt += f"\n\nRespond with a JSON object in the following format: {json.dumps(response_format, indent=2)}"
        
        try:
            response_text = self.generate_response(full_prompt, None, **kwargs)
            # 提取JSON部分
            try:
                # 尝试直接解析
                return json.loads(response_text)
            except:
                # 尝试从文本中提取JSON部分
                import re
                json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                
                # 最后尝试找到任何看起来像JSON的部分
                json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                    
                raise ValueError("Could not parse JSON from response")
                
        except Exception as e:
            print(f"Error generating structured LLM response: {e}")
            return {"error": str(e)}
    
    def _build_full_prompt(self, prompt, context):
        """构建完整提示，包括上下文"""
        if not context:
            return prompt
            
        context_str = "\n\nContext:\n"
        if isinstance(context, list):
            for item in context:
                if isinstance(item, dict):
                    context_str += json.dumps(item, ensure_ascii=False) + "\n"
                else:
                    context_str += str(item) + "\n"
        else:
            context_str += str(context)
            
        return prompt + context_str 