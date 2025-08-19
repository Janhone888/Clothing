# 服装库存管理系统

基于Python内置模块的服装库存管理系统，提供完整的RESTful API接口，支持服装信息的添加、查询和删除操作。系统采用客户端-服务器架构，无需任何外部依赖，可在任何Python环境中直接运行。

## 功能特性

### 核心功能

- 服装信息管理：支持添加、查询和删除服装信息
- 完整的RESTful API设计
-  统一的数据格式和错误处理机制
- 内存数据存储，支持多次请求访问



### 接口功能

- `GET /` - 获取API基本信息
- `GET /clothing` - 获取所有服装条形码列表
- `GET /clothing/{barcode}` - 获取特定服装详细信息
- `POST /clothing` - 添加新服装信息
- `DELETE /clothing/{barcode}` - 删除服装信息



### 错误处理

- 统一的错误响应格式
- 明确的错误代码和描述信息
- 合理的HTTP状态码返回



## 安装和运行

### 环境要求

- Python 3.6+
- 无需安装任何第三方库

### 快速开始

1.**启动服务器**：

```bash
python server.py
```

服务器将在 [http://localhost:5000](http://localhost:5000/) 启动

2.**运行客户端测试**：

打开另一个终端，运行：

```bash
python client.py
```

### 自定义配置

如需修改服务器端口，可编辑文件中的端口配置：

1.修改 `server.py` 中的端口号：

```python
def run(server_class=HTTPServer, handler_class=ClothingHandler, port=8080):xxxxxxxxxx def run(server_class=HTTPServer, handler_class=ClothingHandler, port=8080):python server.py
```

2.修改 `client.py` 中的基础URL：

```python
BASE_URL = "http://localhost:8080"
```





## 使用说明

### API接口文档

1.**获取API信息**

```text
GET /
```

响应示例

```json
{
  "status": "success",
  "message": "Clothing Inventory API is running",
  "endpoints": {
    "GET /clothing": "List all clothing items",
    "GET /clothing/{barcode}": "Get clothing details",
    "POST /clothing": "Add a new clothing item",
    "DELETE /clothing/{barcode}": "Remove a clothing item"
  }
}
```

2.**获取服装列表**

```text
GET /clothing
```

响应示例

```json
{
  "status": "success",
  "count": 2,
  "items": ["CLTH-2023-001", "CLTH-2023-002"]
}
```

3.**获取单个服装信息**

```text
GET /clothing/{barcode}
```

响应示例

```json
{
  "status": "success",
  "item": {
    "category": "T-Shirt",
    "size": "M",
    "color": "Blue"
  }
}
```

1.**添加服装记录**

```text
POST /clothing
Content-Type: application/json

{
    "barcode": "CLTH-2023-001",
    "category": "T-Shirt",
    "size": "M",
    "color": "Blue"
}
```

响应示例

```json
{
  "status": "success",
  "message": "Clothing item added successfully",
  "barcode": "CLTH-2023-001"
}
```

5.**删除服装记录**

```text
DELETE /clothing/{barcode}
```

响应示例

```json
{
  "status": "success",
  "message": "Clothing item removed successfully"
}
```

### 错误处理

系统提供统一的错误响应格式：

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Error description"
}
```



## 技术栈

- **服务器端**: Python内置 `http.server` 模块
- **客户端**: Python内置 `urllib` 模块
- **数据格式**: JSON
- **数据存储**: 内存存储（字典）
- **通信协议**: HTTP/1.1 