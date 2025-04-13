import uuid

# 生成UUID并取前8位（可能含字母）
def get_user_id():
    random_8chars = str(uuid.uuid4())[:12]  # 示例输出：'a1b2c3d4'
    return random_8chars



if __name__ == '__main__':
    print(get_user_id())