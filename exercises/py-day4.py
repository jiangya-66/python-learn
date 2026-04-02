from pydantic import BaseModel, ConfigDict, Field, field_validator, validator

class Config(BaseModel):
    database_url: str
    timeout: int
    retry_count: int

    # Pydantic V2 使用 ConfigDict
    model_config = ConfigDict(
        # 允许从ORM对象创建
        from_attributes=True,
        # 使用别名生成器将字段名称转换为大写
        alias_generator = lambda field: field.upper(),
        # 允许通过别名和原始名称填充字段:json文件中的字段名称是小写的，但我们可以通过别名（大写）来填充
        populate_by_name=True,
        # 保护命名空间
        protected_namespaces=()
    )

    @field_validator('retry_count')
    def validate_retry_count(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("retry_count must be between 1 and 10")
        return v

def load_config():
    import json
    import os
    # 从configs/config.json文件加载配置
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config.json')
    with open(config_path) as f:
        config_data = json.load(f)
    return Config(**config_data)

# Test the implementation
if __name__ == "__main__":
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(f"Database URL: {config.database_url}")
        print(f"Timeout: {config.timeout} seconds")
        print(f"Retry Count: {config.retry_count}")
    except Exception as e:
        print(f"Error loading configuration: {e}")