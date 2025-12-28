## 统一项目路由返回类型为ResponseSchema

### 问题分析
项目中已经定义了统一的响应Schema `ResponseSchema`，但部分路由仍在直接返回数据或使用其他响应类型，导致响应格式不一致。

### 解决方案
修改所有路由函数，统一采用 `ResponseSchema` 作为返回类型。

### 修改步骤

1. **修改 `app/api/v1/admin/items.py`**
   - 导入 `ResponseSchema` 和 `response` 函数
   - 修改所有路由的 `response_model` 为 `ResponseSchema[Item]` 或 `ResponseSchema[List[Item]]`
   - 修改返回语句，使用 `ResponseSchema(data=...)` 或 `response(data=...)` 包装返回值
   - 修改异常处理，使用统一的异常格式

2. **修改 `app/api/v1/client/items.py`**
   - 导入 `ResponseSchema`
   - 修改路由的 `response_model` 为 `ResponseSchema[List[Item]]`
   - 修改返回语句，使用 `ResponseSchema(data=...)` 包装返回值

3. **修改 `app/api/v1/admin/sys/auth.py`**
   - 导入 `ResponseSchema`
   - 修改 `login` 路由的 `response_model` 为 `ResponseSchema[Token]`
   - 修改 `captcha` 路由的 `response_model` 为 `ResponseSchema[Captcha]`
   - 修改返回语句，使用 `ResponseSchema(data=...)` 包装返回值

4. **检查其他路由文件**
   - 确保所有路由都使用了统一的 `ResponseSchema` 格式
   - 修复任何不符合统一格式的路由

### 预期结果
- 所有路由函数统一返回 `ResponseSchema` 格式
- 响应格式包含 `code`、`message` 和 `data` 字段
- 分页接口使用 `ResponseSchema[PageSchema[T]]` 格式
- 异常处理统一，返回包含错误码的响应

### 注意事项
- 保持原有业务逻辑不变
- 确保所有导入正确
- 确保返回的数据结构与 `ResponseSchema` 兼容
- 测试修改后的接口，确保功能正常