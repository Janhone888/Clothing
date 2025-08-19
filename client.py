import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5000"


def make_request(method, url, data=None):
    """发送HTTP请求"""
    headers = {'Content-Type': 'application/json'}

    if data:
        data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return response, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            error_body = json.loads(e.read().decode('utf-8'))
        except:
            error_body = {"message": str(e)}
        return e, error_body
    except Exception as e:
        return None, {"error": str(e)}


def print_response(operation, response, data):
    """格式化打印响应结果"""
    print(f"\n[{operation.upper()}]")
    if hasattr(response, 'code'):
        print(f"Status Code: {response.code}")
    print("Response Body:")
    print(json.dumps(data, indent=2))
    print("-" * 80)


def test_clothing_interaction():
    """完整的服装库存交互测试"""
    test_clothing = {
        "barcode": "CLTH-2023-001",
        "category": "T-Shirt",
        "size": "M",
        "color": "Blue"
    }

    # 1. 获取API信息
    response, data = make_request('GET', f"{BASE_URL}/")
    print_response("API Info", response, data)

    # 2. 获取空服装列表
    response, data = make_request('GET', f"{BASE_URL}/clothing")
    print_response("GET Clothing List (Empty)", response, data)

    # 3. 添加新服装
    response, data = make_request('POST', f"{BASE_URL}/clothing", test_clothing)
    print_response("ADD Clothing", response, data)

    # 4. 获取存在的服装
    response, data = make_request('GET', f"{BASE_URL}/clothing/CLTH-2023-001")
    print_response("GET Existing Clothing", response, data)

    # 5. 获取不存在的服装
    response, data = make_request('GET', f"{BASE_URL}/clothing/INVALID-BARCODE-123")
    print_response("GET Non-existent Clothing", response, data)

    # 6. 删除服装
    response, data = make_request('DELETE', f"{BASE_URL}/clothing/CLTH-2023-001")
    print_response("DELETE Clothing", response, data)

    # 7. 验证删除结果
    response, data = make_request('GET', f"{BASE_URL}/clothing/CLTH-2023-001")
    print_response("GET Deleted Clothing", response, data)


def main():
    """主函数"""
    print("=" * 50)
    print("Clothing Inventory Test Client")
    print("=" * 50)

    try:
        test_clothing_interaction()
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()