
# 流浪动物收养系统 API 接口文档

## 版本信息

* **版本**: v1.0
* **基础URL**: `https://api.stray-animal.com/v1`
* **作者**: 张文雅
* **创建时间**: 2025年

## 目录

1. [认证授权](#%E8%AE%A4%E8%AF%81%E6%8E%88%E6%9D%83)
2. [用户管理](#%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86)
3. [救助站管理](#%E6%95%91%E5%8A%A9%E7%AB%99%E7%AE%A1%E7%90%86)
4. [动物管理](#%E5%8A%A8%E7%89%A9%E7%AE%A1%E7%90%86)
5. [领养管理](#%E9%A2%86%E5%85%BB%E7%AE%A1%E7%90%86)
6. [寻宠功能](#%E5%AF%BB%E5%AE%A0%E5%8A%9F%E8%83%BD)
7. [捐赠管理](#%E6%8D%90%E8%B5%A0%E7%AE%A1%E7%90%86)
8. [活动管理](#%E6%B4%BB%E5%8A%A8%E7%AE%A1%E7%90%86)
9. [知识库](#%E7%9F%A5%E8%AF%86%E5%BA%93)
10. [AI功能](#ai%E5%8A%9F%E8%83%BD)
11. [系统功能](#%E7%B3%BB%E7%BB%9F%E5%8A%9F%E8%83%BD)

---

## 认证授权

### 1.1 用户注册

```
POST /auth/register
```

**请求参数**

```
{
  "username": "string",           // 用户名，3-50字符
  "email": "string",             // 邮箱地址
  "phone": "string",             // 手机号码
  "password": "string",          // 密码，8-20字符
  "name": "string",              // 真实姓名
  "user_type": "string",         // 用户类型: user, shelter_admin, volunteer
  "gender": "string",            // 性别: male, female, other
  "birthday": "string",          // 生日 YYYY-MM-DD
  "address": "string",           // 地址
  "occupation": "string",        // 职业
  "pet_experience": "string"     // 养宠经验: none, beginner, experienced, expert
}
```

**响应示例**

```
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": "uuid",
    "username": "string",
    "email": "string",
    "user_type": "string",
    "status": "active",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

### 1.2 用户登录

```
POST /auth/login
```

**请求参数**

```
{
  "username": "string",    // 用户名或邮箱
  "password": "string",    // 密码
  "remember": "boolean"    // 是否记住登录
}
```

**响应示例**

```
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "string",
    "refresh_token": "string",
    "expires_in": 3600,
    "user": {
      "user_id": "uuid",
      "username": "string",
      "email": "string",
      "user_type": "string",
      "avatar_url": "string"
    }
  }
}
```

### 1.3 刷新令牌

```
POST /auth/refresh
```

**请求头**

```
Authorization: Bearer {refresh_token}
```

### 1.4 退出登录

```
POST /auth/logout
```

**请求头**

```
Authorization: Bearer {access_token}
```

---

## 用户管理

### 2.1 获取用户信息

```
GET /users/{user_id}
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "user_id": "uuid",
    "username": "string",
    "email": "string",
    "phone": "string",
    "name": "string",
    "gender": "string",
    "birthday": "string",
    "address": "string",
    "avatar_url": "string",
    "bio": "string",
    "pet_experience": "string",
    "occupation": "string",
    "living_condition": "string",
    "family_members": 1,
    "has_other_pets": false,
    "user_type": "string",
    "status": "string",
    "created_at": "string"
  }
}
```

### 2.2 更新用户信息

```
PUT /users/{user_id}
```

**请求参数**

```
{
  "name": "string",
  "gender": "string",
  "birthday": "string",
  "address": "string",
  "bio": "string",
  "occupation": "string",
  "living_condition": "string",
  "family_members": 1,
  "has_other_pets": false
}
```

### 2.3 上传用户头像

```
POST /users/{user_id}/avatar
```

**请求参数**

```
Content-Type: multipart/form-data
avatar: file
```

### 2.4 获取用户统计信息

```
GET /users/{user_id}/statistics
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "total_applications": 5,
    "successful_adoptions": 2,
    "total_donations": 10,
    "total_donated_amount": 1500.00,
    "activities_participated": 8,
    "total_volunteer_hours": 24.5,
    "favorite_animals": 15
  }
}
```

---

## 救助站管理

### 3.1 获取救助站列表

```
GET /shelters
```

**查询参数**

```
page: number          // 页码，默认1
size: number          // 每页数量，默认10
city: string          // 城市筛选
province: string      // 省份筛选
status: string        // 状态筛选
keyword: string       // 关键词搜索
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "shelter_id": "uuid",
        "name": "string",
        "description": "string",
        "address": "string",
        "city": "string",
        "province": "string",
        "phone": "string",
        "email": "string",
        "website": "string",
        "capacity": 100,
        "current_animals": 85,
        "status": "active",
        "logo_url": "string",
        "images": ["string"],
        "operating_hours": {},
        "services": ["string"],
        "total_animals": 150,
        "available_animals": 85,
        "adopted_animals": 65
      }
    ],
    "total": 50,
    "page": 1,
    "size": 10,
    "pages": 5
  }
}
```

### 3.2 获取救助站详情

```
GET /shelters/{shelter_id}
```

### 3.3 创建救助站

```
POST /shelters
```

**权限要求**: 系统管理员

**请求参数**

```
{
  "name": "string",
  "description": "string",
  "address": "string",
  "city": "string",
  "province": "string",
  "postal_code": "string",
  "phone": "string",
  "email": "string",
  "website": "string",
  "license_number": "string",
  "capacity": 100,
  "established_date": "2020-01-01",
  "operating_hours": {
    "monday": "09:00-18:00",
    "tuesday": "09:00-18:00"
  },
  "services": ["rescue", "adoption", "medical"]
}
```

### 3.4 更新救助站信息

```
PUT /shelters/{shelter_id}
```

**权限要求**: 救助站管理员或系统管理员

### 3.5 获取救助站统计信息

```
GET /shelters/{shelter_id}/statistics
```

---

## 动物管理

### 4.1 获取动物列表

```
GET /animals
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
species: string       // 物种筛选: cat, dog, rabbit, bird, other
breed: string         // 品种筛选
age_category: string  // 年龄段: baby, young, adult, senior
gender: string        // 性别: male, female, unknown
size: string          // 体型: small, medium, large, extra_large
status: string        // 状态: available, pending, adopted, medical_hold
shelter_id: string    // 救助站ID
city: string          // 城市
good_with_kids: boolean    // 适合有孩子的家庭
good_with_pets: boolean    // 适合有其他宠物的家庭
is_neutered: boolean       // 是否绝育
is_vaccinated: boolean     // 是否接种疫苗
keyword: string            // 关键词搜索
sort: string              // 排序: created_at, age, name, view_count
order: string             // 排序方向: asc, desc
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "animal_id": "uuid",
        "name": "小白",
        "species": "cat",
        "breed": "中华田园猫",
        "age": 12,
        "age_category": "young",
        "gender": "female",
        "size": "medium",
        "weight": 3.5,
        "color": "白色",
        "description": "温顺可爱的小猫",
        "personality": ["温顺", "活泼"],
        "health_status": "健康",
        "is_neutered": true,
        "is_vaccinated": true,
        "good_with_kids": true,
        "good_with_pets": true,
        "energy_level": "medium",
        "training_level": "basic",
        "shelter_id": "uuid",
        "shelter_name": "爱心救助站",
        "shelter_city": "北京",
        "status": "available",
        "rescue_date": "2024-01-01",
        "adoption_fee": 200.00,
        "images": ["string"],
        "videos": ["string"],
        "view_count": 150,
        "favorite_count": 25,
        "pending_applications": 3,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 200,
    "page": 1,
    "size": 10,
    "pages": 20
  }
}
```

### 4.2 获取动物详情

```
GET /animals/{animal_id}
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "animal_id": "uuid",
    "name": "小白",
    "species": "cat",
    "breed": "中华田园猫",
    "age": 12,
    "age_category": "young",
    "gender": "female",
    "size": "medium",
    "weight": 3.5,
    "color": "白色",
    "description": "温顺可爱的小猫",
    "personality": ["温顺", "活泼"],
    "health_status": "健康",
    "medical_history": [
      {
        "date": "2024-01-01",
        "type": "vaccination",
        "description": "狂犬疫苗"
      }
    ],
    "vaccination_records": [
      {
        "vaccine": "狂犬疫苗",
        "date": "2024-01-01",
        "next_due": "2025-01-01"
      }
    ],
    "special_needs": "无",
    "good_with_kids": true,
    "good_with_pets": true,
    "energy_level": "medium",
    "training_level": "basic",
    "shelter": {
      "shelter_id": "uuid",
      "name": "爱心救助站",
      "city": "北京",
      "phone": "010-12345678",
      "address": "北京市朝阳区xxx"
    },
    "status": "available",
    "location": "救助站",
    "rescue_date": "2024-01-01",
    "rescue_story": "在街头被发现，营养不良",
    "adoption_fee": 200.00,
    "images": [
      {
        "image_id": "uuid",
        "url": "string",
        "alt_text": "小白的照片",
        "is_primary": true,
        "sort_order": 1
      }
    ],
    "videos": ["string"],
    "ai_features": {},
    "view_count": 150,
    "favorite_count": 25,
    "pending_applications": 3,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### 4.3 创建动物信息

```
POST /animals
```

**权限要求**: 救助站管理员

**请求参数**

```
{
  "name": "小白",
  "species": "cat",
  "breed": "中华田园猫",
  "age": 12,
  "gender": "female",
  "size": "medium",
  "weight": 3.5,
  "color": "白色",
  "description": "温顺可爱的小猫",
  "personality": ["温顺", "活泼"],
  "health_status": "健康",
  "medical_history": [],
  "is_neutered": true,
  "is_vaccinated": true,
  "vaccination_records": [],
  "special_needs": "无",
  "good_with_kids": true,
  "good_with_pets": true,
  "energy_level": "medium",
  "training_level": "basic",
  "shelter_id": "uuid",
  "location": "救助站",
  "rescue_date": "2024-01-01",
  "rescue_story": "在街头被发现",
  "adoption_fee": 200.00
}
```

### 4.4 更新动物信息

```
PUT /animals/{animal_id}
```

**权限要求**: 救助站管理员

### 4.5 删除动物信息

```
DELETE /animals/{animal_id}
```

**权限要求**: 救助站管理员

### 4.6 上传动物图片

```
POST /animals/{animal_id}/images
```

**请求参数**

```
Content-Type: multipart/form-data
images: file[]
alt_text: string[]
is_primary: boolean[]
```

### 4.7 获取推荐动物

```
GET /animals/recommendations
```

**查询参数**

```
user_id: string       // 用户ID
limit: number         // 推荐数量，默认10
```

---

## 领养管理

### 5.1 提交领养申请

```
POST /adoptions/applications
```

**请求参数**

```
{
  "animal_id": "uuid",
  "reason": "我很喜欢小动物，希望给它一个温暖的家",
  "previous_experience": "曾经养过猫咪3年",
  "living_situation": {
    "housing_type": "apartment",
    "own_or_rent": "own",
    "yard": false,
    "other_pets": false,
    "children": true,
    "children_ages": [8, 12]
  },
  "family_info": {
    "family_size": 4,
    "primary_caregiver": "申请人",
    "work_schedule": "朝九晚五",
    "travel_frequency": "偶尔"
  },
  "veterinarian_info": {
    "clinic_name": "宠物医院",
    "vet_name": "张医生",
    "phone": "010-12345678"
  },
  "references": [
    {
      "name": "李朋友",
      "relationship": "朋友",
      "phone": "138-0000-0000"
    }
  ]
}
```

**响应示例**

```
{
  "code": 200,
  "message": "申请提交成功",
  "data": {
    "application_id": "uuid",
    "animal_id": "uuid",
    "user_id": "uuid",
    "status": "pending",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 5.2 获取领养申请列表

```
GET /adoptions/applications
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
user_id: string       // 申请人ID
animal_id: string     // 动物ID
shelter_id: string    // 救助站ID
status: string        // 状态筛选
start_date: string    // 开始日期
end_date: string      // 结束日期
```

### 5.3 获取领养申请详情

```
GET /adoptions/applications/{application_id}
```

### 5.4 更新申请状态

```
PATCH /adoptions/applications/{application_id}/status
```

**权限要求**: 救助站管理员

**请求参数**

```
{
  "status": "approved",           // pending, under_review, approved, rejected, cancelled, completed
  "approval_notes": "申请通过，安排家访",
  "home_visit_date": "2024-01-15T10:00:00Z",
  "interview_date": "2024-01-10T14:00:00Z"
}
```

### 5.5 完成领养

```
POST /adoptions/records
```

**权限要求**: 救助站管理员

**请求参数**

```
{
  "application_id": "uuid",
  "adoption_date": "2024-01-20",
  "adoption_fee": 200.00,
  "contract_signed": true,
  "microchip_id": "123456789",
  "return_policy": "30天内可无条件退还",
  "follow_up_schedule": [
    {
      "date": "2024-02-20",
      "type": "phone"
    },
    {
      "date": "2024-04-20",
      "type": "visit"
    }
  ],
  "notes": "领养手续完成"
}
```

### 5.6 获取领养记录

```
GET /adoptions/records
```

### 5.7 创建回访记录

```
POST /adoptions/follow-ups
```

**请求参数**

```
{
  "adoption_record_id": "uuid",
  "follow_up_date": "2024-02-20",
  "follow_up_type": "phone",
  "animal_condition": "excellent",
  "living_condition": "动物适应良好，生活环境优越",
  "health_status": "健康状况良好",
  "behavioral_notes": "性格活泼，与家庭成员相处融洽",
  "concerns": "无",
  "recommendations": "继续保持良好的照顾",
  "next_follow_up_date": "2024-04-20",
  "satisfaction_score": 9
}
```

---

## 寻宠功能

### 6.1 发布寻宠信息

```
POST /lost-pets
```

**请求参数**

```
{
  "name": "小黑",
  "species": "dog",
  "breed": "金毛",
  "age": 24,
  "gender": "male",
  "size": "large",
  "weight": 25.0,
  "color": "金黄色",
  "description": "温顺的金毛犬",
  "distinctive_features": "左耳有小缺口，脖子有红色项圈",
  "personality": "温顺、亲人",
  "microchip_id": "123456789",
  "collar_description": "红色皮质项圈，有铃铛",
  "lost_date": "2024-01-01",
  "lost_time": "14:30:00",
  "lost_location": "北京市朝阳区公园",
  "search_radius": 10,
  "contact_name": "张先生",
  "contact_phone": "138-0000-0000",
  "contact_email": "zhang@example.com",
  "reward_amount": 1000.00
}
```

### 6.2 获取寻宠信息列表

```
GET /lost-pets
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
species: string       // 物种筛选
status: string        // 状态: searching, found, closed
city: string          // 城市
lost_date_start: string    // 丢失日期开始
lost_date_end: string      // 丢失日期结束
keyword: string            // 关键词搜索
sort: string              // 排序字段
order: string             // 排序方向
```

### 6.3 获取寻宠详情

```
GET /lost-pets/{lost_pet_id}
```

### 6.4 更新寻宠信息

```
PUT /lost-pets/{lost_pet_id}
```

### 6.5 AI匹配寻宠

```
POST /lost-pets/{lost_pet_id}/match
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "matches": [
      {
        "match_id": "uuid",
        "animal": {
          "animal_id": "uuid",
          "name": "小黄",
          "species": "dog",
          "breed": "金毛",
          "images": ["string"]
        },
        "similarity_score": 0.8956,
        "match_features": {
          "breed_match": 1.0,
          "color_match": 0.85,
          "size_match": 0.92,
          "facial_features": 0.87
        },
        "ai_confidence": 0.89,
        "shelter": {
          "name": "爱心救助站",
          "phone": "010-12345678",
          "address": "北京市朝阳区xxx"
        }
      }
    ]
  }
}
```

### 6.6 确认找到宠物

```
PATCH /lost-pets/{lost_pet_id}/found
```

**请求参数**

```
{
  "found_date": "2024-01-05",
  "found_location": "北京市朝阳区xxx",
  "found_notes": "在救助站找到了我的宠物",
  "match_id": "uuid"
}
```

---

## 捐赠管理

### 7.1 获取捐赠项目列表

```
GET /donations/projects
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
shelter_id: string    // 救助站ID
category: string      // 项目类别
status: string        // 项目状态
priority: string      // 优先级
keyword: string       // 关键词搜索
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "project_id": "uuid",
        "title": "救助流浪猫医疗费用",
        "description": "为救助的流浪猫提供医疗救治",
        "category": "medical",
        "target_amount": 10000.00,
        "current_amount": 6500.00,
        "progress_percentage": 65,
        "start_date": "2024-01-01",
        "end_date": "2024-03-01",
        "status": "active",
        "priority": "high",
        "shelter": {
          "shelter_id": "uuid",
          "name": "爱心救助站",
          "city": "北京"
        },
        "images": ["string"],
        "beneficiary_animals": [
          {
            "animal_id": "uuid",
            "name": "小白",
            "condition": "需要手术治疗"
          }
        ],
        "donors_count": 45,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 20,
    "page": 1,
    "size": 10,
    "pages": 2
  }
}
```

### 7.2 获取项目详情

```
GET /donations/projects/{project_id}
```

### 7.3 创建捐赠项目

```
POST /donations/projects
```

**权限要求**: 救助站管理员

**请求参数**

```
{
  "title": "救助流浪猫医疗费用",
  "description": "为救助的流浪猫提供医疗救治",
  "category": "medical",
  "target_amount": 10000.00,
  "start_date": "2024-01-01",
  "end_date": "2024-03-01",
  "priority": "high",
  "beneficiary_animals": [
    {
      "animal_id": "uuid",
      "condition": "需要手术治疗"
    }
  ]
}
```

### 7.4 进行捐赠

```
POST /donations
```

**请求参数**

```
{
  "project_id": "uuid",
  "amount": 100.00,
  "donation_type": "one_time",
  "payment_method": "alipay",
  "is_anonymous": false,
  "message": "希望小动物们都能健康快乐",
  "receipt_required": true,
  "receipt_info": {
    "name": "张三",
    "tax_id": "123456789",
    "address": "北京市朝阳区xxx"
  }
}
```

### 7.5 获取捐赠记录

```
GET /donations
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
user_id: string       // 捐赠人ID
project_id: string    // 项目ID
payment_status: string // 支付状态
start_date: string    // 开始日期
end_date: string      // 结束日期
```

### 7.6 处理支付回调

```
POST /donations/payment/callback
```

---

## 活动管理

### 8.1 获取活动列表

```
GET /activities
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
shelter_id: string    // 主办救助站ID
category: string      // 活动类别
status: string        // 活动状态
city: string          // 城市
start_date: string    // 开始日期
end_date: string      // 结束日期
featured: boolean     // 是否推荐
keyword: string       // 关键词搜索
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "activity_id": "uuid",
        "title": "周末领养日活动",
        "description": "欢迎来救助站参观，为小动物找家",
        "category": "adoption_event",
        "start_time": "2024-01-20T09:00:00Z",
        "end_time": "2024-01-20T17:00:00Z",
        "registration_start": "2024-01-10T00:00:00Z",
        "registration_end": "2024-01-19T23:59:59Z",
        "location": "爱心救助站",
        "address": "北京市朝阳区xxx",
        "max_participants": 50,
        "current_participants": 25,
        "fee": 0.00,
        "status": "registration_open",
        "shelter": {
          "shelter_id": "uuid",
          "name": "爱心救助站",
          "city": "北京"
        },
        "images": ["string"],
        "featured": true,
        "contact_person": "李老师",
        "contact_phone": "010-12345678",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 15,
    "page": 1,
    "size": 10,
    "pages": 2
  }
}
```

### 8.2 获取活动详情

```
GET /activities/{activity_id}
```

### 8.3 创建活动

```
POST /activities
```

**权限要求**: 救助站管理员

**请求参数**

```
{
  "title": "周末领养日活动",
  "description": "欢迎来救助站参观，为小动物找家",
  "category": "adoption_event",
  "start_time": "2024-01-20T09:00:00Z",
  "end_time": "2024-01-20T17:00:00Z",
  "registration_start": "2024-01-10T00:00:00Z",
  "registration_end": "2024-01-19T23:59:59Z",
  "location": "爱心救助站",
  "address": "北京市朝阳区xxx",
  "max_participants": 50,
  "min_age": 12,
  "requirements": "需要家长陪同",
  "what_to_bring": "身份证件",
  "contact_person": "李老师",
  "contact_phone": "010-12345678",
  "contact_email": "li@shelter.com",
  "fee": 0.00
}
```

### 8.4 报名参加活动

```
POST /activities/{activity_id}/participants
```

**请求参数**

```
{
  "emergency_contact": {
    "name": "张三",
    "phone": "138-0000-0000",
    "relationship": "父亲"
  },
  "special_requirements": "无",
  "waiver_signed": true
}
```

### 8.5 获取活动参与者

```
GET /activities/{activity_id}/participants
```

**权限要求**: 活动创建者或救助站管理员

### 8.6 签到/签退

```
PATCH /activities/{activity_id}/participants/{participant_id}/checkin
```

**请求参数**

```
{
  "action": "checkin",        // checkin 或 checkout
  "timestamp": "2024-01-20T09:00:00Z"
}
```

---

## 知识库

### 9.1 获取知识文章列表

```
GET /knowledge/articles
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
category: string      // 分类筛选
difficulty_level: string   // 难度级别
featured: boolean     // 是否推荐
keyword: string       // 关键词搜索
tags: string[]        // 标签筛选
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "article_id": "uuid",
        "title": "新手养猫指南",
        "slug": "beginner-cat-care-guide",
        "summary": "为新手猫主人提供基础的养猫知识",
        "category": "pet_care",
        "tags": ["新手", "猫咪", "基础知识"],
        "difficulty_level": "beginner",
        "reading_time": 10,
        "author": {
          "user_id": "uuid",
          "name": "专家张医生"
        },
        "featured": true,
        "featured_image": "string",
        "view_count": 1500,
        "like_count": 89,
        "published_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "size": 10,
    "pages": 10
  }
}
```

### 9.2 获取文章详情

```
GET /knowledge/articles/{article_id}
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "article_id": "uuid",
    "title": "新手养猫指南",
    "slug": "beginner-cat-care-guide",
    "summary": "为新手猫主人提供基础的养猫知识",
    "content": "详细的文章内容...",
    "category": "pet_care",
    "tags": ["新手", "猫咪", "基础知识"],
    "difficulty_level": "beginner",
    "reading_time": 10,
    "author": {
      "user_id": "uuid",
      "name": "专家张医生",
      "bio": "资深宠物医生"
    },
    "editor": {
      "user_id": "uuid",
      "name": "编辑李老师"
    },
    "featured": true,
    "featured_image": "string",
    "images": ["string"],
    "videos": ["string"],
    "external_links": [
      {
        "title": "相关资源",
        "url": "https://example.com"
      }
    ],
    "references": ["参考资料1", "参考资料2"],
    "view_count": 1500,
    "like_count": 89,
    "share_count": 25,
    "published_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### 9.3 创建知识文章

```
POST /knowledge/articles
```

**权限要求**: 专家用户或管理员

**请求参数**

```
{
  "title": "新手养猫指南",
  "slug": "beginner-cat-care-guide",
  "summary": "为新手猫主人提供基础的养猫知识",
  "content": "详细的文章内容...",
  "category": "pet_care",
  "tags": ["新手", "猫咪", "基础知识"],
  "difficulty_level": "beginner",
  "reading_time": 10,
  "featured_image": "string",
  "images": ["string"],
  "videos": ["string"],
  "external_links": [
    {
      "title": "相关资源",
      "url": "https://example.com"
    }
  ],
  "references": ["参考资料1", "参考资料2"],
  "seo_title": "新手养猫指南 - 宠物知识",
  "seo_description": "详细的新手养猫指南",
  "seo_keywords": "养猫,新手,宠物护理"
}
```

### 9.4 提交问题

```
POST /knowledge/questions
```

**请求参数**

```
{
  "question": "我的猫咪不吃东西怎么办？",
  "question_category": "health",
  "question_tags": ["猫咪", "食欲", "健康"],
  "images": ["string"],
  "is_public": true
}
```

### 9.5 获取问答记录

```
GET /knowledge/qa
```

**查询参数**

```
page: number          // 页码
size: number          // 每页数量
category: string      // 问题分类
status: string        // 状态筛选
is_featured: boolean  // 是否推荐
keyword: string       // 关键词搜索
```

### 9.6 AI智能问答

```
POST /knowledge/ai-qa
```

**请求参数**

```
{
  "question": "我的猫咪不吃东西怎么办？",
  "context": {
    "pet_type": "cat",
    "pet_age": 12,
    "symptoms": ["不吃东西", "精神不振"]
  }
}
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "qa_id": "uuid",
    "question": "我的猫咪不吃东西怎么办？",
    "answer": "猫咪不吃东西可能有多种原因...",
    "ai_confidence": 0.85,
    "related_articles": [
      {
        "article_id": "uuid",
        "title": "猫咪食欲不振的原因和解决方法",
        "url": "/knowledge/articles/cat-appetite-loss"
      }
    ],
    "recommendations": [
      "建议观察猫咪其他症状",
      "如果持续不吃，请及时就医"
    ]
  }
}
```

---

## AI功能

### 10.1 动物品种识别

```
POST /ai/identify-breed
```

**请求参数**

```
Content-Type: multipart/form-data
image: file           // 动物图片文件
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "analysis_id": "uuid",
    "breed_predictions": [
      {
        "breed": "金毛寻回犬",
        "confidence": 0.92,
        "species": "dog"
      },
      {
        "breed": "拉布拉多",
        "confidence": 0.08,
        "species": "dog"
      }
    ],
    "features": {
      "color": "金黄色",
      "size": "large",
      "coat_type": "long"
    },
    "processing_time": 1250
  }
}
```

### 10.2 动物相似度分析

```
POST /ai/similarity-analysis
```

**请求参数**

```
{
  "image1_url": "string",      // 第一张图片URL
  "image2_url": "string",      // 第二张图片URL
  "analysis_type": "facial"    // 分析类型: facial, full_body, features
}
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "analysis_id": "uuid",
    "similarity_score": 0.8756,
    "confidence": 0.91,
    "match_details": {
      "facial_features": 0.89,
      "body_shape": 0.85,
      "color_pattern": 0.92,
      "size_match": 0.88
    },
    "features_comparison": {
      "image1_features": [0.1, 0.2, 0.3],
      "image2_features": [0.12, 0.18, 0.31]
    },
    "processing_time": 2100
  }
}
```

### 10.3 批量特征提取

```
POST /ai/extract-features
```

**请求参数**

```
Content-Type: multipart/form-data
images: file[]        // 多张图片文件
```

### 10.4 健康状况评估

```
POST /ai/health-assessment
```

**请求参数**

```
Content-Type: multipart/form-data
image: file           // 动物图片
symptoms: string[]    // 症状描述
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "analysis_id": "uuid",
    "health_score": 0.75,
    "concerns": [
      {
        "type": "skin_condition",
        "severity": "mild",
        "confidence": 0.68,
        "description": "可能存在轻微皮肤问题"
      }
    ],
    "recommendations": [
      "建议进行兽医检查",
      "注意观察皮肤状况变化"
    ],
    "confidence": 0.72
  }
}
```

---

## 系统功能

### 11.1 用户收藏

#### 11.1.1 添加收藏

```
POST /users/{user_id}/favorites
```

**请求参数**

```
{
  "target_type": "animal",     // animal, article, activity, shelter
  "target_id": "uuid",
  "notes": "很喜欢这只小猫"
}
```

#### 11.1.2 获取收藏列表

```
GET /users/{user_id}/favorites
```

**查询参数**

```
target_type: string   // 收藏类型筛选
page: number          // 页码
size: number          // 每页数量
```

#### 11.1.3 取消收藏

```
DELETE /users/{user_id}/favorites/{favorite_id}
```

### 11.2 系统通知

#### 11.2.1 获取通知列表

```
GET /users/{user_id}/notifications
```

**查询参数**

```
type: string          // 通知类型筛选
is_read: boolean      // 是否已读
page: number          // 页码
size: number          // 每页数量
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "items": [
      {
        "notification_id": "uuid",
        "type": "adoption",
        "title": "您的领养申请已通过审核",
        "content": "恭喜您！您申请领养的小白已通过初步审核...",
        "priority": "high",
        "is_read": false,
        "action_url": "/adoptions/applications/uuid",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 25,
    "unread_count": 8
  }
}
```

#### 11.2.2 标记通知已读

```
PATCH /users/{user_id}/notifications/{notification_id}/read
```

#### 11.2.3 批量标记已读

```
PATCH /users/{user_id}/notifications/mark-all-read
```

### 11.3 文件上传

#### 11.3.1 上传图片

```
POST /upload/images
```

**请求参数**

```
Content-Type: multipart/form-data
file: file            // 图片文件
category: string      // 分类: avatar, animal, article, activity
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "file_id": "uuid",
    "url": "https://cdn.example.com/images/uuid.jpg",
    "filename": "image.jpg",
    "size": 1024000,
    "mime_type": "image/jpeg",
    "width": 1920,
    "height": 1080
  }
}
```

#### 11.3.2 上传文档

```
POST /upload/documents
```

### 11.4 搜索功能

#### 11.4.1 全局搜索

```
GET /search
```

**查询参数**

```
q: string             // 搜索关键词
type: string          // 搜索类型: all, animals, articles, activities, shelters
page: number          // 页码
size: number          // 每页数量
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "animals": {
      "items": [],
      "total": 15
    },
    "articles": {
      "items": [],
      "total": 8
    },
    "activities": {
      "items": [],
      "total": 3
    },
    "shelters": {
      "items": [],
      "total": 2
    },
    "total_results": 28
  }
}
```

### 11.5 统计数据

#### 11.5.1 获取系统统计

```
GET /statistics/system
```

**响应示例**

```
{
  "code": 200,
  "data": {
    "total_users": 5000,
    "total_animals": 1200,
    "total_adoptions": 800,
    "total_shelters": 50,
    "total_donations": 150000.00,
    "active_lost_pets": 25,
    "upcoming_activities": 8,
    "monthly_stats": {
      "new_users": 120,
      "new_animals": 45,
      "successful_adoptions": 32,
      "donations_amount": 8500.00
    }
  }
}
```

#### 11.5.2 获取救助站统计

```
GET /statistics/shelters/{shelter_id}
```

#### 11.5.3 获取用户统计

```
GET /statistics/users/{user_id}
```

---

## 错误码说明

| **错误码** | **说明**           |
| ---------------- | ------------------------ |
| **200**    | **请求成功**       |
| **201**    | **创建成功**       |
| **400**    | **请求参数错误**   |
| **401**    | **未授权**         |
| **403**    | **权限不足**       |
| **404**    | **资源不存在**     |
| **409**    | **资源冲突**       |
| **422**    | **数据验证失败**   |
| **429**    | **请求频率限制**   |
| **500**    | **服务器内部错误** |
| **503**    | **服务不可用**     |

## 通用响应格式

### 成功响应

```
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 错误响应

```
{
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "type": "ValidationError",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      }
    ]
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 分页响应格式

```
{
  "code": 200,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "size": 10,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

## 认证说明

### JWT Token 格式

```
Authorization: Bearer {access_token}
```

### Token 刷新

**当 access_token 过期时，使用 refresh_token 获取新的 access_token。**

### 权限级别

* **游客**: 可查看公开信息
* **普通用户**: 可提交申请、参与活动、进行捐赠
* **救助站管理员**: 可管理所属救助站的动物、申请、活动
* **系统管理员**: 拥有所有权限

## 限流说明

| **接口类型** | **限制**        |
| ------------------ | --------------------- |
| **登录接口** | **每分钟5次**   |
| **注册接口** | **每分钟3次**   |
| **文件上传** | **每分钟10次**  |
| **AI分析**   | **每分钟20次**  |
| **其他接口** | **每分钟100次** |

## 版本更新日志

### v1.0 (2025-01-01)

* **初始版本发布**
* **实现基础的用户管理、动物管理、领养流程**
* **集成AI功能：品种识别、相似度分析**
* **支持寻宠匹配、捐赠管理、活动管理**
* **提供知识库和智能问答功能**

---

*本文档持续更新中，如有疑问请联系开发团队。*
