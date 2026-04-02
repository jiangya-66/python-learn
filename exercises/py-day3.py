# # 1. 基础模型定义
# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional, List

# class User(BaseModel):
#     id: int
#     name: str
#     email: str
#     age: Optional[int] = None
#     created_at: datetime = datetime.now()
    
# # 创建实例
# user = User(id=1, name="张三", email="zhangsan@example.com")
# print(user)
# # 输出: id=1 name='张三' email='zhangsan@example.com' age=None created_at=datetime.datetime(...)

# # 访问属性
# print(user.name)  # 张三
# print(user.model_dump())  # 转换为字典

# # # 2. 数据验证
# from pydantic import BaseModel, Field, ValidationError, EmailStr

# class User(BaseModel):
#     name: str = Field(..., min_length=2, max_length=50, description="用户名")
#     age: int = Field(..., ge=0, le=150, description="年龄")
#     email: EmailStr  # 自动验证邮箱格式
    
# try:
#     # 无效数据
#     user = User(name="Abc", age=100, email="invalid-email@sample.com")
# except ValidationError as e:
#     print(e.json())
#     # 输出详细的验证错误信息

# # 3. 嵌套模型
# from pydantic import BaseModel
# from typing import List

# class Address(BaseModel):
#     street: str
#     city: str
#     zipcode: str

# class User(BaseModel):
#     name: str
#     age: int
#     address: Address
#     tags: List[str] = []
    
# # 创建嵌套对象
# user = User(
#     name="李四",
#     age=25,
#     address={"street": "中山路123号", "city": "北京", "zipcode": "100000"},
#     tags=["python", "developer"]
# )

# print(user.address.city)  # 北京
# print(user.address)  # Address(street='中山路123号', city='北京', zipcode='100000')
# print(user.tags)  # ['python', 'developer']

# # 4. 自定义验证器
# from pydantic import BaseModel, validator, field_validator

# class Product(BaseModel):
#     name: str
#     price: float
#     discount: float = 0.0
    
#     @field_validator('price')
#     def price_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError('价格必须大于0')
#         return v
    
#     @field_validator('discount')
#     def discount_valid(cls, v, info):
#         if v < 0 or v > 1:
#             raise ValueError('折扣必须在0-1之间')
#         return v
    
#     # 计算最终价格的属性
#     @property
#     def final_price(self) -> float:
#         """计算最终价格"""
#         return self.price * (1 - self.discount)

# # 使用
# product = Product(name="笔记本电脑", price=5999.99, discount=0.2)
# print(product.final_price)  # 4799.992

# # 5. 数据转换
# from pydantic import BaseModel
# from datetime import date

# class Event(BaseModel):
#     name: str
#     date: date  # 自动将字符串转换为date对象
#     attendees: int
    
# # 从字典创建
# data = {
#     "name": "Python会议",
#     "date": "2024-12-25",
#     "attendees": "100"  # 字符串会自动转换为int
# }
# # 创建Event实例，自动进行数据转换
# event = Event(**data)
# print(event.date)  # 2024-12-25 (date对象)
# # attendees属性虽然输入的是字符串，但会自动转换为整数
# print(type(event.attendees))  # <class 'int'>

# 6. 配置和序列化 - Pydantic V2 版本
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    id: int = Field(alias="ID")
    name: str = Field(alias="NAME")
    password: str = Field(alias="PASSWORD", exclude=True)
    
    # Pydantic V2 使用 ConfigDict
    model_config = ConfigDict(
        # 允许从ORM对象创建
        from_attributes=True,
        # 允许通过别名和原始名称填充字段
        populate_by_name=True,
        # 保护命名空间
        protected_namespaces=()
    )

# 假设有一个SQLAlchemy的User模型
class SQLAlchemyUser:
    def __init__(self, id, name, password):
        self.ID = id
        self.NAME = name
        self.PASSWORD = password

# 创建ORM对象 - 使用小写字段名
db_user = SQLAlchemyUser(id=1, name="赵六", password="pass456")

print("=== Pydantic V2 兼容版本 ===")
print()

# 测试1: 从ORM对象创建（使用小写字段名）
user1 = User.model_validate(db_user)  # 正确！
print("测试1 - 从ORM对象创建（小写字段）:")
print(f"  用户名: {user1.name}")  # 输出: 赵六
print(f"  序列化结果: {user1.model_dump()}")  # 密码字段被排除

# 测试2: 使用大写字段名创建
user2 = User(ID=2, NAME="钱七", PASSWORD="pass789")
print("\n测试2 - 使用大写字段名创建:")
print(f"  用户名: {user2.name}")  # 输出: 钱七
print(f"  序列化结果: {user2.model_dump()}")  # 密码字段被排除

# 测试3: 使用小写字段名创建
user3 = User(id=3, name="孙八", password="pass999")
print("\n测试3 - 使用小写字段名创建:")
print(f"  用户名: {user3.name}")  # 输出: 孙八
print(f"  序列化结果: {user3.model_dump()}")  # 密码字段被排除

# 测试4: 混合大小写字段名
user4 = User(ID=4, name="李九", PASSWORD="pass000")
print("\n测试4 - 混合大小写字段名创建:")
print(f"  用户名: {user4.name}")  # 输出: 李九
print(f"  序列化结果: {user4.model_dump()}")  # 密码字段被排除

# 测试5: 使用字典创建（混合大小写）
data = {"ID": 5, "name": "周十", "PASSWORD": "pass111"}
user5 = User(**data)
print("\n测试5 - 使用字典创建（混合大小写）:")
print(f"  用户名: {user5.name}")  # 输出: 周十
print(f"  序列化结果: {user5.model_dump()}")  # 密码字段被排除

print("\n=== 总结 ===")
print("SQLAlchemyUser中的字段名现在可以接受大写和小写！")
print("通过以下配置实现：")
print("1. 为每个字段显式定义别名（alias）")
print("2. 设置 populate_by_name=True 允许通过别名和原始名称填充")
print("3. 在Field中设置 exclude=True 排除密码字段")

# # 7. 泛型支持
# from pydantic import BaseModel
# from typing import Generic, TypeVar, List

# T = TypeVar('T')

# class APIResponse(BaseModel, Generic[T]):
#     code: int
#     message: str
#     data: T

# # 使用
# class User(BaseModel):
#     id: int
#     name: str

# # 单个用户响应
# response = APIResponse[User](
#     code=200,
#     message="success",
#     data={"id": 1, "name": "张三"}
# )

# # 用户列表响应
# response_list = APIResponse[List[User]](
#     code=200,
#     message="success",
#     data=[{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
# )
# print(response_list.data)

# # 8. 实际应用场景：FastAPI集成
# from fastapi import FastAPI
# from pydantic import BaseModel, Field

# app = FastAPI()

# class UserCreate(BaseModel):
#     username: str = Field(..., min_length=3, max_length=20)
#     email: str
#     password: str = Field(..., min_length=8)
    
# @app.post("/users/")
# async def create_user(user: UserCreate):
#     # 自动验证请求数据
#     return {"message": f"用户 {user.username} 创建成功"}

# # 9. 高级特性：递归模型
# from pydantic import BaseModel
# from typing import List, Optional

# class Category(BaseModel):
#     id: int
#     name: str
#     children: List['Category'] = []  # 自引用
    
#     class Config:
#         # 允许自引用
#         arbitrary_types_allowed = True
        
# # 创建树形结构
# root = Category(
#     id=1,
#     name="电子产品",
#     children=[
#         Category(id=2, name="手机", children=[]),
#         Category(id=3, name="电脑", children=[
#             Category(id=4, name="笔记本", children=[]),
#             Category(id=5, name="台式机", children=[])
#         ])
#     ]
# )

# print(root)

# # 10. 环境变量支持
# from pydantic_settings import BaseSettings
# from typing import Optional

# class Settings(BaseSettings):
#     app_name: str = "MyApp"
#     database_url: str
#     debug: bool = False
#     api_key: Optional[str] = None
    
#     class Config:
#         env_file = ".env"  # 从.env文件读取环境变量
        
# # 使用
# settings = Settings()
# print(settings.database_url)  # 从环境变量或.env文件读取

# . 序列化器（重要新功能）
from pydantic import BaseModel, field_serializer, model_serializer

class User(BaseModel):
    name: str
    password: str
    
    # 字段级序列化器
    @field_serializer('password')
    def hide_password(self, password: str) -> str:
        return '***'
    
    # 模型级序列化器
    @model_serializer
    def custom_serialize(self):
        return {k: v for k, v in self.__dict__.items() if k != 'password'}

user = User(name="张三", password="secret")
print(user.model_dump())  # {'name': '张三', 'password': '***'}