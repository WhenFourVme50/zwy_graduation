-- ========================================
-- 流浪动物收养系统数据库设计
-- 作者：张文雅
-- 版本：v1.0
-- 创建时间：2025年
-- ========================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `stray_animal_adoption`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `stray_animal_adoption`;

-- ========================================
-- 1. 用户管理相关表
-- ========================================

-- 用户表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID，使用UUID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `email` VARCHAR(100) NOT NULL COMMENT '邮箱地址',
  `phone` VARCHAR(20) NOT NULL COMMENT '手机号码',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希值',
  `user_type` ENUM('user', 'shelter_admin', 'system_admin', 'volunteer') NOT NULL DEFAULT 'user' COMMENT '用户类型',
  `status` ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active' COMMENT '用户状态',
  `name` VARCHAR(100) DEFAULT NULL COMMENT '真实姓名',
  `gender` ENUM('male', 'female', 'other') DEFAULT 'other' COMMENT '性别',
  `birthday` DATE DEFAULT NULL COMMENT '生日',
  `address` VARCHAR(500) DEFAULT NULL COMMENT '地址',
  `avatar_url` VARCHAR(500) DEFAULT NULL COMMENT '头像URL',
  `bio` TEXT DEFAULT NULL COMMENT '个人简介',
  `pet_experience` ENUM('none', 'beginner', 'experienced', 'expert') DEFAULT 'none' COMMENT '养宠经验',
  `occupation` VARCHAR(100) DEFAULT NULL COMMENT '职业',
  `living_condition` TEXT DEFAULT NULL COMMENT '居住条件',
  `family_members` INT DEFAULT 1 COMMENT '家庭成员数量',
  `has_other_pets` BOOLEAN DEFAULT FALSE COMMENT '是否有其他宠物',
  `email_verified` BOOLEAN DEFAULT FALSE COMMENT '邮箱是否验证',
  `phone_verified` BOOLEAN DEFAULT FALSE COMMENT '手机是否验证',
  `last_login_at` DATETIME DEFAULT NULL COMMENT '最后登录时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_user_type` (`user_type`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户会话表
DROP TABLE IF EXISTS `user_sessions`;
CREATE TABLE `user_sessions` (
  `session_id` VARCHAR(128) NOT NULL COMMENT '会话ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID',
  `device_info` JSON DEFAULT NULL COMMENT '设备信息',
  `ip_address` VARCHAR(45) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` TEXT DEFAULT NULL COMMENT '用户代理',
  `expires_at` DATETIME NOT NULL COMMENT '过期时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`session_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_expires_at` (`expires_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户会话表';

-- ========================================
-- 2. 救助站管理相关表
-- ========================================

-- 救助站表
DROP TABLE IF EXISTS `shelters`;
CREATE TABLE `shelters` (
  `shelter_id` VARCHAR(36) NOT NULL COMMENT '救助站ID',
  `name` VARCHAR(200) NOT NULL COMMENT '救助站名称',
  `description` TEXT DEFAULT NULL COMMENT '救助站描述',
  `address` VARCHAR(500) NOT NULL COMMENT '地址',
  `city` VARCHAR(100) NOT NULL COMMENT '城市',
  `province` VARCHAR(100) NOT NULL COMMENT '省份',
  `postal_code` VARCHAR(20) DEFAULT NULL COMMENT '邮政编码',
  `phone` VARCHAR(20) NOT NULL COMMENT '联系电话',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `website` VARCHAR(500) DEFAULT NULL COMMENT '官网',
  `license_number` VARCHAR(100) DEFAULT NULL COMMENT '许可证号',
  `capacity` INT DEFAULT 0 COMMENT '容量',
  `current_animals` INT DEFAULT 0 COMMENT '当前动物数量',
  `established_date` DATE DEFAULT NULL COMMENT '成立日期',
  `status` ENUM('active', 'inactive', 'pending') NOT NULL DEFAULT 'pending' COMMENT '状态',
  `logo_url` VARCHAR(500) DEFAULT NULL COMMENT 'Logo URL',
  `images` JSON DEFAULT NULL COMMENT '图片URLs',
  `operating_hours` JSON DEFAULT NULL COMMENT '营业时间',
  `services` JSON DEFAULT NULL COMMENT '提供的服务',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`shelter_id`),
  KEY `idx_city` (`city`),
  KEY `idx_province` (`province`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='救助站表';

-- 救助站管理员关联表
DROP TABLE IF EXISTS `shelter_admins`;
CREATE TABLE `shelter_admins` (
  `id` VARCHAR(36) NOT NULL COMMENT 'ID',
  `shelter_id` VARCHAR(36) NOT NULL COMMENT '救助站ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID',
  `role` ENUM('owner', 'admin', 'staff') NOT NULL DEFAULT 'staff' COMMENT '角色',
  `permissions` JSON DEFAULT NULL COMMENT '权限配置',
  `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_shelter_user` (`shelter_id`, `user_id`),
  KEY `idx_user_id` (`user_id`),
  FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`shelter_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='救助站管理员关联表';

-- ========================================
-- 3. 动物管理相关表
-- ========================================

-- 动物表
DROP TABLE IF EXISTS `animals`;
CREATE TABLE `animals` (
  `animal_id` VARCHAR(36) NOT NULL COMMENT '动物ID',
  `name` VARCHAR(100) NOT NULL COMMENT '动物名称',
  `species` ENUM('cat', 'dog', 'rabbit', 'bird', 'other') NOT NULL COMMENT '物种',
  `breed` VARCHAR(100) DEFAULT NULL COMMENT '品种',
  `age` INT DEFAULT NULL COMMENT '年龄（月）',
  `age_category` ENUM('baby', 'young', 'adult', 'senior') DEFAULT 'adult' COMMENT '年龄段',
  `gender` ENUM('male', 'female', 'unknown') NOT NULL COMMENT '性别',
  `size` ENUM('small', 'medium', 'large', 'extra_large') DEFAULT 'medium' COMMENT '体型',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重（kg）',
  `color` VARCHAR(100) DEFAULT NULL COMMENT '颜色',
  `description` TEXT DEFAULT NULL COMMENT '描述',
  `personality` JSON DEFAULT NULL COMMENT '性格特点',
  `health_status` TEXT DEFAULT NULL COMMENT '健康状况',
  `medical_history` JSON DEFAULT NULL COMMENT '医疗历史',
  `is_neutered` BOOLEAN DEFAULT FALSE COMMENT '是否绝育',
  `is_vaccinated` BOOLEAN DEFAULT FALSE COMMENT '是否接种疫苗',
  `vaccination_records` JSON DEFAULT NULL COMMENT '疫苗记录',
  `special_needs` TEXT DEFAULT NULL COMMENT '特殊需求',
  `good_with_kids` BOOLEAN DEFAULT NULL COMMENT '是否适合有孩子的家庭',
  `good_with_pets` BOOLEAN DEFAULT NULL COMMENT '是否适合有其他宠物的家庭',
  `energy_level` ENUM('low', 'medium', 'high') DEFAULT 'medium' COMMENT '活跃度',
  `training_level` ENUM('none', 'basic', 'intermediate', 'advanced') DEFAULT 'none' COMMENT '训练程度',
  `shelter_id` VARCHAR(36) NOT NULL COMMENT '所属救助站ID',
  `status` ENUM('available', 'pending', 'adopted', 'medical_hold', 'not_available') NOT NULL DEFAULT 'available' COMMENT '状态',
  `location` VARCHAR(200) DEFAULT NULL COMMENT '当前位置',
  `rescue_date` DATE DEFAULT NULL COMMENT '救助日期',
  `rescue_story` TEXT DEFAULT NULL COMMENT '救助故事',
  `adoption_fee` DECIMAL(10,2) DEFAULT 0.00 COMMENT '领养费用',
  `images` JSON DEFAULT NULL COMMENT '图片URLs',
  `videos` JSON DEFAULT NULL COMMENT '视频URLs',
  `ai_features` JSON DEFAULT NULL COMMENT 'AI提取的特征数据',
  `view_count` INT DEFAULT 0 COMMENT '浏览次数',
  `favorite_count` INT DEFAULT 0 COMMENT '收藏次数',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`animal_id`),
  KEY `idx_species` (`species`),
  KEY `idx_breed` (`breed`),
  KEY `idx_status` (`status`),
  KEY `idx_shelter_id` (`shelter_id`),
  KEY `idx_age_category` (`age_category`),
  KEY `idx_size` (`size`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`shelter_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动物表';

-- 动物图片表
DROP TABLE IF EXISTS `animal_images`;
CREATE TABLE `animal_images` (
  `image_id` VARCHAR(36) NOT NULL COMMENT '图片ID',
  `animal_id` VARCHAR(36) NOT NULL COMMENT '动物ID',
  `url` VARCHAR(500) NOT NULL COMMENT '图片URL',
  `alt_text` VARCHAR(200) DEFAULT NULL COMMENT '替代文本',
  `is_primary` BOOLEAN DEFAULT FALSE COMMENT '是否为主图',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `ai_analysis` JSON DEFAULT NULL COMMENT 'AI分析结果',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`image_id`),
  KEY `idx_animal_id` (`animal_id`),
  KEY `idx_is_primary` (`is_primary`),
  FOREIGN KEY (`animal_id`) REFERENCES `animals` (`animal_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动物图片表';

-- ========================================
-- 4. 领养管理相关表
-- ========================================

-- 领养申请表
DROP TABLE IF EXISTS `adoption_applications`;
CREATE TABLE `adoption_applications` (
  `application_id` VARCHAR(36) NOT NULL COMMENT '申请ID',
  `animal_id` VARCHAR(36) NOT NULL COMMENT '动物ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '申请人ID',
  `status` ENUM('pending', 'under_review', 'approved', 'rejected', 'cancelled', 'completed') NOT NULL DEFAULT 'pending' COMMENT '申请状态',
  `application_data` JSON NOT NULL COMMENT '申请详细信息',
  `reason` TEXT DEFAULT NULL COMMENT '申请理由',
  `previous_experience` TEXT DEFAULT NULL COMMENT '以往经验',
  `living_situation` JSON DEFAULT NULL COMMENT '居住情况',
  `family_info` JSON DEFAULT NULL COMMENT '家庭信息',
  `veterinarian_info` JSON DEFAULT NULL COMMENT '兽医信息',
  `references` JSON DEFAULT NULL COMMENT '推荐人信息',
  `home_visit_required` BOOLEAN DEFAULT TRUE COMMENT '是否需要家访',
  `home_visit_date` DATETIME DEFAULT NULL COMMENT '家访时间',
  `home_visit_notes` TEXT DEFAULT NULL COMMENT '家访备注',
  `interview_date` DATETIME DEFAULT NULL COMMENT '面试时间',
  `interview_notes` TEXT DEFAULT NULL COMMENT '面试备注',
  `approval_notes` TEXT DEFAULT NULL COMMENT '审批备注',
  `rejection_reason` TEXT DEFAULT NULL COMMENT '拒绝原因',
  `reviewed_by` VARCHAR(36) DEFAULT NULL COMMENT '审核人ID',
  `reviewed_at` DATETIME DEFAULT NULL COMMENT '审核时间',
  `adoption_date` DATE DEFAULT NULL COMMENT '领养日期',
  `adoption_fee_paid` DECIMAL(10,2) DEFAULT 0.00 COMMENT '已支付领养费',
  `follow_up_required` BOOLEAN DEFAULT TRUE COMMENT '是否需要回访',
  `follow_up_date` DATE DEFAULT NULL COMMENT '回访日期',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`application_id`),
  KEY `idx_animal_id` (`animal_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`animal_id`) REFERENCES `animals` (`animal_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`reviewed_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='领养申请表';

-- 领养记录表
DROP TABLE IF EXISTS `adoption_records`;
CREATE TABLE `adoption_records` (
  `record_id` VARCHAR(36) NOT NULL COMMENT '记录ID',
  `application_id` VARCHAR(36) NOT NULL COMMENT '申请ID',
  `animal_id` VARCHAR(36) NOT NULL COMMENT '动物ID',
  `adopter_id` VARCHAR(36) NOT NULL COMMENT '领养人ID',
  `shelter_id` VARCHAR(36) NOT NULL COMMENT '救助站ID',
  `adoption_date` DATE NOT NULL COMMENT '领养日期',
  `adoption_fee` DECIMAL(10,2) DEFAULT 0.00 COMMENT '领养费用',
  `contract_signed` BOOLEAN DEFAULT FALSE COMMENT '是否签署合同',
  `contract_url` VARCHAR(500) DEFAULT NULL COMMENT '合同文件URL',
  `microchip_id` VARCHAR(50) DEFAULT NULL COMMENT '芯片ID',
  `return_policy` TEXT DEFAULT NULL COMMENT '退还政策',
  `follow_up_schedule` JSON DEFAULT NULL COMMENT '回访计划',
  `notes` TEXT DEFAULT NULL COMMENT '备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `uk_application_id` (`application_id`),
  KEY `idx_animal_id` (`animal_id`),
  KEY `idx_adopter_id` (`adopter_id`),
  KEY `idx_shelter_id` (`shelter_id`),
  KEY `idx_adoption_date` (`adoption_date`),
  FOREIGN KEY (`application_id`) REFERENCES `adoption_applications` (`application_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`animal_id`) REFERENCES `animals` (`animal_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`adopter_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`shelter_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='领养记录表';

-- 回访记录表
DROP TABLE IF EXISTS `follow_up_records`;
CREATE TABLE `follow_up_records` (
  `follow_up_id` VARCHAR(36) NOT NULL COMMENT '回访ID',
  `adoption_record_id` VARCHAR(36) NOT NULL COMMENT '领养记录ID',
  `follow_up_date` DATE NOT NULL COMMENT '回访日期',
  `follow_up_type` ENUM('phone', 'visit', 'video', 'email') NOT NULL COMMENT '回访方式',
  `conducted_by` VARCHAR(36) NOT NULL COMMENT '回访人ID',
  `animal_condition` ENUM('excellent', 'good', 'fair', 'poor', 'concerning') NOT NULL COMMENT '动物状况',
  `living_condition` TEXT DEFAULT NULL COMMENT '生活条件',
  `health_status` TEXT DEFAULT NULL COMMENT '健康状况',
  `behavioral_notes` TEXT DEFAULT NULL COMMENT '行为备注',
  `concerns` TEXT DEFAULT NULL COMMENT '关注点',
  `recommendations` TEXT DEFAULT NULL COMMENT '建议',
  `next_follow_up_date` DATE DEFAULT NULL COMMENT '下次回访日期',
  `images` JSON DEFAULT NULL COMMENT '回访图片',
  `satisfaction_score` INT DEFAULT NULL COMMENT '满意度评分(1-10)',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`follow_up_id`),
  KEY `idx_adoption_record_id` (`adoption_record_id`),
  KEY `idx_follow_up_date` (`follow_up_date`),
  KEY `idx_conducted_by` (`conducted_by`),
  FOREIGN KEY (`adoption_record_id`) REFERENCES `adoption_records` (`record_id`) ON DELETE CASCADE,
  FOREIGN KEY (`conducted_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='回访记录表';

-- ========================================
-- 5. 寻宠功能相关表
-- ========================================

-- 丢失宠物表
DROP TABLE IF EXISTS `lost_pets`;
CREATE TABLE `lost_pets` (
  `lost_pet_id` VARCHAR(36) NOT NULL COMMENT '丢失宠物ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '发布人ID',
  `name` VARCHAR(100) NOT NULL COMMENT '宠物名称',
  `species` ENUM('cat', 'dog', 'rabbit', 'bird', 'other') NOT NULL COMMENT '物种',
  `breed` VARCHAR(100) DEFAULT NULL COMMENT '品种',
  `age` INT DEFAULT NULL COMMENT '年龄（月）',
  `gender` ENUM('male', 'female', 'unknown') NOT NULL COMMENT '性别',
  `size` ENUM('small', 'medium', 'large', 'extra_large') DEFAULT 'medium' COMMENT '体型',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重（kg）',
  `color` VARCHAR(100) DEFAULT NULL COMMENT '颜色',
  `description` TEXT DEFAULT NULL COMMENT '描述',
  `distinctive_features` TEXT DEFAULT NULL COMMENT '特征描述',
  `personality` TEXT DEFAULT NULL COMMENT '性格特点',
  `microchip_id` VARCHAR(50) DEFAULT NULL COMMENT '芯片ID',
  `collar_description` TEXT DEFAULT NULL COMMENT '项圈描述',
  `lost_date` DATE NOT NULL COMMENT '丢失日期',
  `lost_time` TIME DEFAULT NULL COMMENT '丢失时间',
  `lost_location` VARCHAR(500) NOT NULL COMMENT '丢失地点',
  `lost_coordinates` POINT NOT NULL COMMENT '丢失坐标',
  `search_radius` INT DEFAULT 5 COMMENT '搜索半径（公里）',
  `last_seen_location` VARCHAR(500) DEFAULT NULL COMMENT '最后目击地点',
  `last_seen_date` DATE DEFAULT NULL COMMENT '最后目击日期',
  `contact_name` VARCHAR(100) NOT NULL COMMENT '联系人姓名',
  `contact_phone` VARCHAR(20) NOT NULL COMMENT '联系电话',
  `contact_email` VARCHAR(100) DEFAULT NULL COMMENT '联系邮箱',
  `reward_amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '悬赏金额',
  `status` ENUM('searching', 'found', 'closed') NOT NULL DEFAULT 'searching' COMMENT '状态',
  `found_date` DATE DEFAULT NULL COMMENT '找到日期',
  `found_location` VARCHAR(500) DEFAULT NULL COMMENT '找到地点',
  `found_notes` TEXT DEFAULT NULL COMMENT '找到备注',
  `images` JSON DEFAULT NULL COMMENT '图片URLs',
  `ai_features` JSON DEFAULT NULL COMMENT 'AI提取的特征数据',
  `view_count` INT DEFAULT 0 COMMENT '浏览次数',
  `share_count` INT DEFAULT 0 COMMENT '分享次数',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`lost_pet_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_species` (`species`),
  KEY `idx_status` (`status`),
  KEY `idx_lost_date` (`lost_date`),
  KEY `idx_lost_location` (`lost_location`),
  SPATIAL KEY `idx_lost_coordinates` (`lost_coordinates`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='丢失宠物表';

-- 宠物匹配记录表
DROP TABLE IF EXISTS `pet_matches`;
CREATE TABLE `pet_matches` (
  `match_id` VARCHAR(36) NOT NULL COMMENT '匹配ID',
  `lost_pet_id` VARCHAR(36) NOT NULL COMMENT '丢失宠物ID',
  `animal_id` VARCHAR(36) NOT NULL COMMENT '动物ID',
  `similarity_score` DECIMAL(5,4) NOT NULL COMMENT '相似度分数',
  `match_features` JSON DEFAULT NULL COMMENT '匹配特征详情',
  `ai_confidence` DECIMAL(5,4) DEFAULT NULL COMMENT 'AI置信度',
  `manual_review` BOOLEAN DEFAULT FALSE COMMENT '是否人工审核',
  `reviewer_id` VARCHAR(36) DEFAULT NULL COMMENT '审核人ID',
  `review_notes` TEXT DEFAULT NULL COMMENT '审核备注',
  `status` ENUM('pending', 'confirmed', 'rejected', 'false_positive') NOT NULL DEFAULT 'pending' COMMENT '状态',
  `contacted` BOOLEAN DEFAULT FALSE COMMENT '是否已联系',
  `contact_date` DATETIME DEFAULT NULL COMMENT '联系时间',
  `contact_notes` TEXT DEFAULT NULL COMMENT '联系备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`match_id`),
  KEY `idx_lost_pet_id` (`lost_pet_id`),
  KEY `idx_animal_id` (`animal_id`),
  KEY `idx_similarity_score` (`similarity_score`),
  KEY `idx_status` (`status`),
  FOREIGN KEY (`lost_pet_id`) REFERENCES `lost_pets` (`lost_pet_id`) ON DELETE CASCADE,
  FOREIGN KEY (`animal_id`) REFERENCES `animals` (`animal_id`) ON DELETE CASCADE,
  FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宠物匹配记录表';

-- ========================================
-- 6. 捐赠功能相关表
-- ========================================

-- 捐赠项目表
DROP TABLE IF EXISTS `donation_projects`;
CREATE TABLE `donation_projects` (
  `project_id` VARCHAR(36) NOT NULL COMMENT '项目ID',
  `shelter_id` VARCHAR(36) DEFAULT NULL COMMENT '救助站ID',
  `title` VARCHAR(200) NOT NULL COMMENT '项目标题',
  `description` TEXT NOT NULL COMMENT '项目描述',
  `category` ENUM('medical', 'food', 'shelter', 'rescue', 'education', 'emergency', 'general') NOT NULL COMMENT '项目类别',
  `target_amount` DECIMAL(12,2) NOT NULL COMMENT '目标金额',
  `current_amount` DECIMAL(12,2) DEFAULT 0.00 COMMENT '当前金额',
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE DEFAULT NULL COMMENT '结束日期',
  `status` ENUM('draft', 'active', 'paused', 'completed', 'cancelled') NOT NULL DEFAULT 'draft' COMMENT '状态',
  `priority` ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium' COMMENT '优先级',
  `images` JSON DEFAULT NULL COMMENT '项目图片',
  `documents` JSON DEFAULT NULL COMMENT '相关文档',
  `beneficiary_animals` JSON DEFAULT NULL COMMENT '受益动物信息',
  `progress_updates` JSON DEFAULT NULL COMMENT '进度更新',
  `transparency_report` TEXT DEFAULT NULL COMMENT '透明度报告',
  `created_by` VARCHAR(36) NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`project_id`),
  KEY `idx_shelter_id` (`shelter_id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  KEY `idx_priority` (`priority`),
  KEY `idx_created_by` (`created_by`),
  FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`shelter_id`) ON DELETE SET NULL,
  FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='捐赠项目表';

-- 捐赠记录表
DROP TABLE IF EXISTS `donations`;
CREATE TABLE `donations` (
  `donation_id` VARCHAR(36) NOT NULL COMMENT '捐赠ID',
  `project_id` VARCHAR(36) NOT NULL COMMENT '项目ID',
  `user_id` VARCHAR(36) DEFAULT NULL COMMENT '捐赠人ID',
  `donor_name` VARCHAR(100) DEFAULT NULL COMMENT '捐赠人姓名',
  `donor_email` VARCHAR(100) DEFAULT NULL COMMENT '捐赠人邮箱',
  `donor_phone` VARCHAR(20) DEFAULT NULL COMMENT '捐赠人电话',
  `amount` DECIMAL(10,2) NOT NULL COMMENT '捐赠金额',
  `currency` VARCHAR(3) DEFAULT 'CNY' COMMENT '货币类型',
  `donation_type` ENUM('one_time', 'monthly', 'annual') DEFAULT 'one_time' COMMENT '捐赠类型',
  `payment_method` ENUM('alipay', 'wechat', 'bank_transfer', 'credit_card', 'other') NOT NULL COMMENT '支付方式',
  `payment_status` ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL DEFAULT 'pending' COMMENT '支付状态',
  `transaction_id` VARCHAR(100) DEFAULT NULL COMMENT '交易ID',
  `payment_time` DATETIME DEFAULT NULL COMMENT '支付时间',
  `is_anonymous` BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
  `message` TEXT DEFAULT NULL COMMENT '留言',
  `receipt_required` BOOLEAN DEFAULT FALSE COMMENT '是否需要收据',
  `receipt_info` JSON DEFAULT NULL COMMENT '收据信息',
  `tax_deductible` BOOLEAN DEFAULT TRUE COMMENT '是否可抵税',
  `refund_reason` TEXT DEFAULT NULL COMMENT '退款原因',
  `refund_time` DATETIME DEFAULT NULL COMMENT '退款时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`donation_id`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_payment_status` (`payment_status`),
  KEY `idx_payment_time` (`payment_time`),
  KEY `idx_transaction_id` (`transaction_id`),
  FOREIGN KEY (`project_id`) REFERENCES `donation_projects` (`project_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='捐赠记录表';

-- ========================================
-- 7. 活动管理相关表
-- ========================================

-- 活动表
DROP TABLE IF EXISTS `activities`;
CREATE TABLE `activities` (
  `activity_id` VARCHAR(36) NOT NULL COMMENT '活动ID',
  `shelter_id` VARCHAR(36) DEFAULT NULL COMMENT '主办救助站ID',
  `title` VARCHAR(200) NOT NULL COMMENT '活动标题',
  `description` TEXT NOT NULL COMMENT '活动描述',
  `category` ENUM('adoption_event', 'volunteer', 'education', 'fundraising', 'medical_camp', 'awareness', 'training') NOT NULL COMMENT '活动类别',
  `start_time` DATETIME NOT NULL COMMENT '开始时间',
  `end_time` DATETIME NOT NULL COMMENT '结束时间',
  `registration_start` DATETIME DEFAULT NULL COMMENT '报名开始时间',
  `registration_end` DATETIME DEFAULT NULL COMMENT '报名结束时间',
  `location` VARCHAR(500) NOT NULL COMMENT '活动地点',
  `address` VARCHAR(500) DEFAULT NULL COMMENT '详细地址',
  `coordinates` POINT NOT NULL COMMENT '坐标',
  `max_participants` INT DEFAULT NULL COMMENT '最大参与人数',
  `current_participants` INT DEFAULT 0 COMMENT '当前参与人数',
  `min_age` INT DEFAULT NULL COMMENT '最小年龄限制',
  `max_age` INT DEFAULT NULL COMMENT '最大年龄限制',
  `requirements` TEXT DEFAULT NULL COMMENT '参与要求',
  `what_to_bring` TEXT DEFAULT NULL COMMENT '需要携带物品',
  `contact_person` VARCHAR(100) DEFAULT NULL COMMENT '联系人',
  `contact_phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  `contact_email` VARCHAR(100) DEFAULT NULL COMMENT '联系邮箱',
  `fee` DECIMAL(8,2) DEFAULT 0.00 COMMENT '参与费用',
  `status` ENUM('draft', 'published', 'registration_open', 'registration_closed', 'ongoing', 'completed', 'cancelled') NOT NULL DEFAULT 'draft' COMMENT '状态',
  `images` JSON DEFAULT NULL COMMENT '活动图片',
  `documents` JSON DEFAULT NULL COMMENT '相关文档',
  `tags` JSON DEFAULT NULL COMMENT '标签',
  `featured` BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
  `created_by` VARCHAR(36) NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`activity_id`),
  KEY `idx_shelter_id` (`shelter_id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  KEY `idx_start_time` (`start_time`),
  KEY `idx_featured` (`featured`),
  KEY `idx_created_by` (`created_by`),
  SPATIAL KEY `idx_coordinates` (`coordinates`),
  FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`shelter_id`) ON DELETE SET NULL,
  FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活动表';

-- 活动参与记录表
DROP TABLE IF EXISTS `activity_participants`;
CREATE TABLE `activity_participants` (
  `participant_id` VARCHAR(36) NOT NULL COMMENT '参与记录ID',
  `activity_id` VARCHAR(36) NOT NULL COMMENT '活动ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID',
  `registration_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
  `status` ENUM('registered', 'confirmed', 'attended', 'no_show', 'cancelled') NOT NULL DEFAULT 'registered' COMMENT '状态',
  `emergency_contact` JSON DEFAULT NULL COMMENT '紧急联系人',
  `special_requirements` TEXT DEFAULT NULL COMMENT '特殊要求',
  `waiver_signed` BOOLEAN DEFAULT FALSE COMMENT '是否签署免责声明',
  `payment_status` ENUM('pending', 'paid', 'refunded', 'waived') DEFAULT 'pending' COMMENT '付费状态',
  `check_in_time` DATETIME DEFAULT NULL COMMENT '签到时间',
  `check_out_time` DATETIME DEFAULT NULL COMMENT '签退时间',
  `feedback` TEXT DEFAULT NULL COMMENT '反馈',
  `rating` INT DEFAULT NULL COMMENT '评分(1-5)',
  `certificate_issued` BOOLEAN DEFAULT FALSE COMMENT '是否颁发证书',
  `volunteer_hours` DECIMAL(4,2) DEFAULT NULL COMMENT '志愿服务时长',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`participant_id`),
  UNIQUE KEY `uk_activity_user` (`activity_id`, `user_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_registration_time` (`registration_time`),
  FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活动参与记录表';

-- ========================================
-- 8. 知识库相关表
-- ========================================

-- 知识文章表
DROP TABLE IF EXISTS `knowledge_articles`;
CREATE TABLE `knowledge_articles` (
  `article_id` VARCHAR(36) NOT NULL COMMENT '文章ID',
  `title` VARCHAR(200) NOT NULL COMMENT '文章标题',
  `slug` VARCHAR(200) NOT NULL COMMENT 'URL别名',
  `summary` TEXT DEFAULT NULL COMMENT '摘要',
  `content` LONGTEXT NOT NULL COMMENT '文章内容',
  `category` ENUM('pet_care', 'health', 'behavior', 'training', 'nutrition', 'grooming', 'emergency', 'adoption_guide', 'legal', 'other') NOT NULL COMMENT '分类',
  `tags` JSON DEFAULT NULL COMMENT '标签',
  `difficulty_level` ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度级别',
  `reading_time` INT DEFAULT NULL COMMENT '预计阅读时间（分钟）',
  `author_id` VARCHAR(36) NOT NULL COMMENT '作者ID',
  `editor_id` VARCHAR(36) DEFAULT NULL COMMENT '编辑ID',
  `status` ENUM('draft', 'review', 'published', 'archived') NOT NULL DEFAULT 'draft' COMMENT '状态',
  `featured` BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
  `featured_image` VARCHAR(500) DEFAULT NULL COMMENT '特色图片',
  `images` JSON DEFAULT NULL COMMENT '文章图片',
  `videos` JSON DEFAULT NULL COMMENT '视频链接',
  `external_links` JSON DEFAULT NULL COMMENT '外部链接',
  `references` JSON DEFAULT NULL COMMENT '参考资料',
  `view_count` INT DEFAULT 0 COMMENT '浏览次数',
  `like_count` INT DEFAULT 0 COMMENT '点赞次数',
  `share_count` INT DEFAULT 0 COMMENT '分享次数',
  `seo_title` VARCHAR(200) DEFAULT NULL COMMENT 'SEO标题',
  `seo_description` TEXT DEFAULT NULL COMMENT 'SEO描述',
  `seo_keywords` VARCHAR(500) DEFAULT NULL COMMENT 'SEO关键词',
  `published_at` DATETIME DEFAULT NULL COMMENT '发布时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`article_id`),
  UNIQUE KEY `uk_slug` (`slug`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  KEY `idx_author_id` (`author_id`),
  KEY `idx_featured` (`featured`),
  KEY `idx_published_at` (`published_at`),
  FULLTEXT KEY `ft_title_content` (`title`, `content`),
  FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`editor_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识文章表';

-- 问答记录表
DROP TABLE IF EXISTS `qa_records`;
CREATE TABLE `qa_records` (
  `qa_id` VARCHAR(36) NOT NULL COMMENT '问答ID',
  `user_id` VARCHAR(36) DEFAULT NULL COMMENT '提问用户ID',
  `question` TEXT NOT NULL COMMENT '问题内容',
  `question_category` ENUM('health', 'behavior', 'training', 'nutrition', 'grooming', 'adoption', 'legal', 'emergency', 'general') NOT NULL COMMENT '问题分类',
  `question_tags` JSON DEFAULT NULL COMMENT '问题标签',
  `answer` TEXT DEFAULT NULL COMMENT '回答内容',
  `answer_type` ENUM('ai_generated', 'expert_reviewed', 'community') DEFAULT 'ai_generated' COMMENT '回答类型',
  `answered_by` VARCHAR(36) DEFAULT NULL COMMENT '回答人ID',
  `ai_confidence` DECIMAL(5,4) DEFAULT NULL COMMENT 'AI置信度',
  `expert_verified` BOOLEAN DEFAULT FALSE COMMENT '是否专家验证',
  `status` ENUM('pending', 'answered', 'verified', 'closed') NOT NULL DEFAULT 'pending' COMMENT '状态',
  `priority` ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium' COMMENT '优先级',
  `is_public` BOOLEAN DEFAULT TRUE COMMENT '是否公开',
  `is_featured` BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
  `helpful_count` INT DEFAULT 0 COMMENT '有用计数',
  `not_helpful_count` INT DEFAULT 0 COMMENT '无用计数',
  `view_count` INT DEFAULT 0 COMMENT '浏览次数',
  `related_articles` JSON DEFAULT NULL COMMENT '相关文章',
  `images` JSON DEFAULT NULL COMMENT '问题图片',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `answered_at` DATETIME DEFAULT NULL COMMENT '回答时间',
  PRIMARY KEY (`qa_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_question_category` (`question_category`),
  KEY `idx_status` (`status`),
  KEY `idx_answered_by` (`answered_by`),
  KEY `idx_is_featured` (`is_featured`),
  KEY `idx_created_at` (`created_at`),
  FULLTEXT KEY `ft_question_answer` (`question`, `answer`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL,
  FOREIGN KEY (`answered_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问答记录表';

-- ========================================
-- 9. 系统功能相关表
-- ========================================

-- 用户收藏表
DROP TABLE IF EXISTS `user_favorites`;
CREATE TABLE `user_favorites` (
  `favorite_id` VARCHAR(36) NOT NULL COMMENT '收藏ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID',
  `target_type` ENUM('animal', 'article', 'activity', 'shelter') NOT NULL COMMENT '收藏类型',
  `target_id` VARCHAR(36) NOT NULL COMMENT '目标ID',
  `notes` TEXT DEFAULT NULL COMMENT '备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `uk_user_target` (`user_id`, `target_type`, `target_id`),
  KEY `idx_target_type` (`target_type`),
  KEY `idx_target_id` (`target_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- 系统通知表
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `notification_id` VARCHAR(36) NOT NULL COMMENT '通知ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '用户ID',
  `type` ENUM('system', 'adoption', 'donation', 'activity', 'match', 'follow_up', 'reminder') NOT NULL COMMENT '通知类型',
  `title` VARCHAR(200) NOT NULL COMMENT '通知标题',
  `content` TEXT NOT NULL COMMENT '通知内容',
  `data` JSON DEFAULT NULL COMMENT '附加数据',
  `priority` ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium' COMMENT '优先级',
  `is_read` BOOLEAN DEFAULT FALSE COMMENT '是否已读',
  `read_at` DATETIME DEFAULT NULL COMMENT '阅读时间',
  `action_url` VARCHAR(500) DEFAULT NULL COMMENT '操作链接',
  `expires_at` DATETIME DEFAULT NULL COMMENT '过期时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`notification_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统通知表';

-- 系统日志表
DROP TABLE IF EXISTS `system_logs`;
CREATE TABLE `system_logs` (
  `log_id` VARCHAR(36) NOT NULL COMMENT '日志ID',
  `user_id` VARCHAR(36) DEFAULT NULL COMMENT '用户ID',
  `action` VARCHAR(100) NOT NULL COMMENT '操作类型',
  `resource_type` VARCHAR(50) DEFAULT NULL COMMENT '资源类型',
  `resource_id` VARCHAR(36) DEFAULT NULL COMMENT '资源ID',
  `description` TEXT DEFAULT NULL COMMENT '操作描述',
  `ip_address` VARCHAR(45) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` TEXT DEFAULT NULL COMMENT '用户代理',
  `request_data` JSON DEFAULT NULL COMMENT '请求数据',
  `response_data` JSON DEFAULT NULL COMMENT '响应数据',
  `status` ENUM('success', 'failure', 'error') NOT NULL COMMENT '状态',
  `error_message` TEXT DEFAULT NULL COMMENT '错误信息',
  `execution_time` INT DEFAULT NULL COMMENT '执行时间（毫秒）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`log_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_resource_type` (`resource_type`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统日志表';

-- AI分析记录表
DROP TABLE IF EXISTS `ai_analysis_records`;
CREATE TABLE `ai_analysis_records` (
  `analysis_id` VARCHAR(36) NOT NULL COMMENT '分析ID',
  `user_id` VARCHAR(36) DEFAULT NULL COMMENT '用户ID',
  `analysis_type` ENUM('breed_identification', 'similarity_analysis', 'health_assessment', 'behavior_analysis') NOT NULL COMMENT '分析类型',
  `input_data` JSON NOT NULL COMMENT '输入数据',
  `output_data` JSON NOT NULL COMMENT '输出数据',
  `model_version` VARCHAR(50) NOT NULL COMMENT '模型版本',
  `confidence_score` DECIMAL(5,4) DEFAULT NULL COMMENT '置信度分数',
  `processing_time` INT DEFAULT NULL COMMENT '处理时间（毫秒）',
  `status` ENUM('pending', 'completed', 'failed') NOT NULL DEFAULT 'pending' COMMENT '状态',
  `error_message` TEXT DEFAULT NULL COMMENT '错误信息',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`analysis_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_analysis_type` (`analysis_type`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI分析记录表';

-- ========================================
-- 10. 创建视图
-- ========================================

-- 动物详情视图
CREATE OR REPLACE VIEW `v_animal_details` AS
SELECT
  a.*,
  s.name AS shelter_name,
  s.city AS shelter_city,
  s.phone AS shelter_phone,
  (SELECT COUNT(*) FROM adoption_applications aa WHERE aa.animal_id = a.animal_id AND aa.status IN ('pending', 'under_review')) AS pending_applications,
  (SELECT COUNT(*) FROM user_favorites uf WHERE uf.target_type = 'animal' AND uf.target_id = a.animal_id) AS favorite_count_actual
FROM animals a
LEFT JOIN shelters s ON a.shelter_id = s.shelter_id;

-- 用户统计视图
CREATE OR REPLACE VIEW `v_user_statistics` AS
SELECT
  u.user_id,
  u.username,
  u.email,
  u.user_type,
  u.status,
  (SELECT COUNT(*) FROM adoption_applications aa WHERE aa.user_id = u.user_id) AS total_applications,
  (SELECT COUNT(*) FROM adoption_applications aa WHERE aa.user_id = u.user_id AND aa.status = 'completed') AS successful_adoptions,
  (SELECT COUNT(*) FROM donations d WHERE d.user_id = u.user_id AND d.payment_status = 'completed') AS total_donations,
  (SELECT COALESCE(SUM(d.amount), 0) FROM donations d WHERE d.user_id = u.user_id AND d.payment_status = 'completed') AS total_donated_amount,
  (SELECT COUNT(*) FROM activity_participants ap WHERE ap.user_id = u.user_id) AS activities_participated,
  (SELECT COALESCE(SUM(ap.volunteer_hours), 0) FROM activity_participants ap WHERE ap.user_id = u.user_id) AS total_volunteer_hours
FROM users u;

-- 救助站统计视图
CREATE OR REPLACE VIEW `v_shelter_statistics` AS
SELECT
  s.*,
  (SELECT COUNT(*) FROM animals a WHERE a.shelter_id = s.shelter_id) AS total_animals,
  (SELECT COUNT(*) FROM animals a WHERE a.shelter_id = s.shelter_id AND a.status = 'available') AS available_animals,
  (SELECT COUNT(*) FROM animals a WHERE a.shelter_id = s.shelter_id AND a.status = 'adopted') AS adopted_animals,
  (SELECT COUNT(*) FROM adoption_applications aa JOIN animals a ON aa.animal_id = a.animal_id WHERE a.shelter_id = s.shelter_id) AS total_applications,
  (SELECT COUNT(*) FROM donation_projects dp WHERE dp.shelter_id = s.shelter_id) AS total_projects,
  (SELECT COALESCE(SUM(d.amount), 0) FROM donations d JOIN donation_projects dp ON d.project_id = dp.project_id WHERE dp.shelter_id = s.shelter_id AND d.payment_status = 'completed') AS total_donations_received
FROM shelters s;

-- ========================================
-- 11. 创建存储过程
-- ========================================

DELIMITER //

-- 更新动物收藏数量
CREATE PROCEDURE `UpdateAnimalFavoriteCount`(IN animal_id_param VARCHAR(36))
BEGIN
  UPDATE animals
  SET favorite_count = (
    SELECT COUNT(*)
    FROM user_favorites
    WHERE target_type = 'animal' AND target_id = animal_id_param
  )
  WHERE animal_id = animal_id_param;
END //

-- 更新捐赠项目当前金额
CREATE PROCEDURE `UpdateProjectCurrentAmount`(IN project_id_param VARCHAR(36))
BEGIN
  UPDATE donation_projects
  SET current_amount = (
    SELECT COALESCE(SUM(amount), 0)
    FROM donations
    WHERE project_id = project_id_param AND payment_status = 'completed'
  )
  WHERE project_id = project_id_param;
END //

-- 更新活动参与人数
CREATE PROCEDURE `UpdateActivityParticipantCount`(IN activity_id_param VARCHAR(36))
BEGIN
  UPDATE activities
  SET current_participants = (
    SELECT COUNT(*)
    FROM activity_participants
    WHERE activity_id = activity_id_param AND status IN ('registered', 'confirmed', 'attended')
  )
  WHERE activity_id = activity_id_param;
END //

-- 清理过期会话
CREATE PROCEDURE `CleanupExpiredSessions`()
BEGIN
  DELETE FROM user_sessions WHERE expires_at < NOW();
END //

-- 生成动物推荐
CREATE PROCEDURE `GenerateAnimalRecommendations`(
  IN user_id_param VARCHAR(36),
  IN limit_count INT
)
BEGIN
  -- 基于用户的收藏和申请历史推荐相似动物
  SELECT DISTINCT a.*
  FROM animals a
  WHERE a.status = 'available'
    AND a.animal_id NOT IN (
      SELECT target_id FROM user_favorites
      WHERE user_id = user_id_param AND target_type = 'animal'
    )
    AND a.animal_id NOT IN (
      SELECT animal_id FROM adoption_applications
      WHERE user_id = user_id_param
    )
    AND (
      a.species IN (
        SELECT DISTINCT a2.species
        FROM animals a2
        JOIN user_favorites uf ON a2.animal_id = uf.target_id
        WHERE uf.user_id = user_id_param AND uf.target_type = 'animal'
      )
      OR a.breed IN (
        SELECT DISTINCT a2.breed
        FROM animals a2
        JOIN user_favorites uf ON a2.animal_id = uf.target_id
        WHERE uf.user_id = user_id_param AND uf.target_type = 'animal'
      )
    )
  ORDER BY a.created_at DESC
  LIMIT limit_count;
END //

DELIMITER ;

-- ========================================
-- 12. 创建触发器
-- ========================================

DELIMITER //

-- 用户收藏动物时更新动物收藏数
CREATE TRIGGER `tr_user_favorites_after_insert`
AFTER INSERT ON `user_favorites`
FOR EACH ROW
BEGIN
  IF NEW.target_type = 'animal' THEN
    CALL UpdateAnimalFavoriteCount(NEW.target_id);
  END IF;
END //

-- 用户取消收藏动物时更新动物收藏数
CREATE TRIGGER `tr_user_favorites_after_delete`
AFTER DELETE ON `user_favorites`
FOR EACH ROW
BEGIN
  IF OLD.target_type = 'animal' THEN
    CALL UpdateAnimalFavoriteCount(OLD.target_id);
  END IF;
END //

-- 捐赠完成时更新项目金额
CREATE TRIGGER `tr_donations_after_update`
AFTER UPDATE ON `donations`
FOR EACH ROW
BEGIN
  IF NEW.payment_status = 'completed' AND OLD.payment_status != 'completed' THEN
    CALL UpdateProjectCurrentAmount(NEW.project_id);
  END IF;
END //

-- 活动参与状态变更时更新参与人数
CREATE TRIGGER `tr_activity_participants_after_insert`
AFTER INSERT ON `activity_participants`
FOR EACH ROW
BEGIN
  CALL UpdateActivityParticipantCount(NEW.activity_id);
END //

CREATE TRIGGER `tr_activity_participants_after_update`
AFTER UPDATE ON `activity_participants`
FOR EACH ROW
BEGIN
  CALL UpdateActivityParticipantCount(NEW.activity_id);
END //

CREATE TRIGGER `tr_activity_participants_after_delete`
AFTER DELETE ON `activity_participants`
FOR EACH ROW
BEGIN
  CALL UpdateActivityParticipantCount(OLD.activity_id);
END //

-- 领养申请状态变更时更新动物状态
CREATE TRIGGER `tr_adoption_applications_after_update`
AFTER UPDATE ON `adoption_applications`
FOR EACH ROW
BEGIN
  IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
    UPDATE animals SET status = 'adopted' WHERE animal_id = NEW.animal_id;
  ELSEIF NEW.status = 'approved' AND OLD.status != 'approved' THEN
    UPDATE animals SET status = 'pending' WHERE animal_id = NEW.animal_id;
  ELSEIF NEW.status IN ('rejected', 'cancelled') AND OLD.status = 'approved' THEN
    UPDATE animals SET status = 'available' WHERE animal_id = NEW.animal_id;
  END IF;
END //

DELIMITER ;

-- ========================================
-- 13. 创建索引优化
-- ========================================

-- 复合索引优化查询性能
CREATE INDEX `idx_animals_species_status_created` ON `animals` (`species`, `status`, `created_at`);
CREATE INDEX `idx_animals_shelter_status` ON `animals` (`shelter_id`, `status`);
CREATE INDEX `idx_adoption_applications_user_status` ON `adoption_applications` (`user_id`, `status`);
CREATE INDEX `idx_adoption_applications_animal_status` ON `adoption_applications` (`animal_id`, `status`);
CREATE INDEX `idx_donations_project_status_amount` ON `donations` (`project_id`, `payment_status`, `amount`);
CREATE INDEX `idx_activities_start_time_status` ON `activities` (`start_time`, `status`);
CREATE INDEX `idx_lost_pets_species_status_date` ON `lost_pets` (`species`, `status`, `lost_date`);

-- ========================================
-- 14. 插入初始数据
-- ========================================

-- 插入系统管理员用户
INSERT INTO `users` (
  `user_id`, `username`, `email`, `phone`, `password_hash`,
  `user_type`, `status`, `name`, `email_verified`, `phone_verified`
) VALUES (
  UUID(), 'admin', 'admin@stray-animal.com', '13800000000',
  '$2b$12$LQv3c1yqBwEHxPiNsdk/cOHxMlQOKbEnTuVHSwiQn/M/jbdHigBqG',
  'system_admin', 'active', '系统管理员', TRUE, TRUE
);

-- 插入默认知识文章分类数据
INSERT INTO `knowledge_articles` (
  `article_id`, `title`, `slug`, `summary`, `content`, `category`,
  `author_id`, `status`, `featured`, `published_at`
) VALUES (
  UUID(), '新手养宠指南', 'beginner-pet-care-guide',
  '为新手宠物主人提供基础的养宠知识和建议',
  '详细的新手养宠指南内容...', 'pet_care',
  (SELECT user_id FROM users WHERE username = 'admin'),
  'published', TRUE, NOW()
);

-- 设置外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ========================================
-- 数据库设计完成
-- ========================================