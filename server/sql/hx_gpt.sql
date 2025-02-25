/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 90100
 Source Host           : localhost:3306
 Source Schema         : ai_agent

 Target Server Type    : MySQL
 Target Server Version : 90100
 File Encoding         : 65001

 Date: 14/01/2025 11:49:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_agent
-- ----------------------------
DROP TABLE IF EXISTS `ai_agent`;
CREATE TABLE `ai_agent`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色体名称',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '角色体内容(json字符串)',
  `model_key` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型名称',
  `temperature` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '随机性',
  `top_p` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '核采样',
  `max_tokens` bigint(0) NULL DEFAULT NULL COMMENT '单次交互所用的最大Token数',
  `presence_penalty` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '话题新鲜度',
  `frequency_penalty` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '频率惩罚度',
  `user_icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户图标',
  `assistant_icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '助理图标',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `user_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色体' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ai_agent
-- ----------------------------
INSERT INTO `ai_agent` VALUES (2, 'ppt大纲助手', '[{\"role\": \"system\", \"content\": \"\\u6839\\u636e\\u4e3b\\u9898\\uff0c\\u5e2e\\u6211\\u5217\\u4e00\\u4e0bppt\\u7684\\u5927\\u7eb2\\uff0c\\u903b\\u8f91\\u8981\\u5206\\u660e\\uff0c\\u6846\\u67b6\\u8981\\u6e05\\u6670\\u3002\\u6211\\u7684ppt\\u4e3b\\u9898\\u662f\"}]', 'llama-3.2-90b-vision-preview', '0.5', '0.2', 8000, '0', '0', 'icon-avatar-nvhuajia', 'icon-avatar-chat_gpt', '2025-01-02 16:20:50', '2025-01-02 16:36:30', 'zhouhx');
INSERT INTO `ai_agent` VALUES (3, '通用', '[{\"role\": \"system\", \"content\": \"\\u4f60\\u662f\\u4e00\\u4e2a\\u5168\\u80fd\\u578b\\u7684\\u80fd\\u624b\\uff0c\\u80fd\\u6839\\u636e\\u63d0\\u51fa\\u7684\\u95ee\\u9898\\u4f5c\\u51fa\\u5168\\u9762\\u7ec6\\u81f4\\u7684\\u56de\\u7b54\\u3002\\u6211\\u7684\\u7b2c\\u4e00\\u4e2a\\u95ee\\u9898\\u662f\"}]', 'llama-3.2-90b-vision-preview', '0.5', '0.2', 8000, '0', '0', 'icon-avatar-bailing', 'icon-avatar-chat_gpt', '2025-01-01 16:57:17', NULL, 'system');
INSERT INTO `ai_agent` VALUES (5, '英语翻译专家', '[{\"role\": \"system\", \"content\": \"\\u4f60\\u662f\\u4e00\\u4e2a\\u7ffb\\u8bd1\\u4e13\\u5bb6\\u3002\\u6839\\u636e\\u6211\\u63d0\\u51fa\\u7684\\u8981\\u6c42\\u7ed9\\u51fa\\u7b54\\u6848\\u3002\\u7ffb\\u8bd1\\u65f6\\u4e0d\\u8981\\u5e26\\u7ffb\\u8bd1\\u8154\\uff0c\\u800c\\u662f\\u8981\\u7ffb\\u8bd1\\u5f97\\u81ea\\u7136\\u3001\\u6d41\\u7545\\u548c\\u5730\\u9053\\uff0c\\u4f7f\\u7528\\u4f18\\u7f8e\\u548c\\u9ad8\\u96c5\\u7684\\u8868\\u8fbe\\u65b9\\u5f0f\\\\n\\u64cd\\u4f5c\\u6b65\\u9aa4\\uff1a\\\\n\\\\t 1\\u3001\\u5982\\u679c\\u662f\\u82f1\\u6587\\u5c31\\u7ffb\\u8bd1\\u6210\\u4e2d\\u6587\\\\n\\\\t 2\\u3001\\u5982\\u679c\\u662f\\u4e2d\\u6587\\u5c31\\u7ffb\\u8bd1\\u6210\\u82f1\\u6587\\\\n\\u8f93\\u51fa\\u683c\\u5f0f\\uff1a\\u660e\\u786e\\u6307\\u51fa\\u7ffb\\u8bd1\\u5185\\u5bb9\\\"}]\"}]', 'llama-3.2-90b-vision-preview', '0.5', '0.2', 8000, '0', '0', 'icon-avatar-xuesheng', 'icon-avatar-chat_gpt', '2025-01-02 17:07:29', '2025-01-03 11:06:52', 'zhouhx');

-- ----------------------------
-- Table structure for ai_history
-- ----------------------------
DROP TABLE IF EXISTS `ai_history`;
CREATE TABLE `ai_history`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '聊天记录名称',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '聊天记录内容(json字符串)',
  `agent_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色体id',
  `all_token_counts` bigint(0) NULL DEFAULT NULL COMMENT '当前记录token数',
  `count` int(0) NULL DEFAULT NULL COMMENT '当前对话数',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `user_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 45 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '聊天记录' ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for ai_model
-- ----------------------------
DROP TABLE IF EXISTS `ai_model`;
CREATE TABLE `ai_model`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `model_key` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '调用模型主键',
  `model_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型显示名称',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `model_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型类型',
  `multimodal` tinyint(1) NULL DEFAULT NULL COMMENT '是否是视觉模型',
  `max_content_len` bigint(0) NULL DEFAULT NULL COMMENT '模型支持的最大上下文长度',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `user_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '模型基本配置' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ai_model
-- ----------------------------
INSERT INTO `ai_model` VALUES (1, 'llama-3.2-90b-vision-preview', 'llama-3.2-90b-vision', '3.2 90b大模型', 'Groq', 0, 131072, '2025-01-02 11:41:42', '2025-01-02 13:41:41', 'zhouhx');
INSERT INTO `ai_model` VALUES (3, 'llama-3.3-70b-versatile', 'llama-3.3-70b', 'llama-3.3大模型，支持上下文:128k,输出token:32,768', 'Groq', 0, 131072, '2025-01-02 13:47:16', NULL, 'zhouhx');
INSERT INTO `ai_model` VALUES (4, 'llama-3.2-1b-instruct', 'llama-3.2-1b', '本地', 'LMStudio', 0, 8160, '2025-01-02 13:47:37', NULL, 'zhouhx');
INSERT INTO `ai_model` VALUES (5, 'qwen-plus', 'qwen-plus', '通义千问超大规模语言模型的增强版，支持中文英文等不同语言输入。', 'Qwen', 0, 8000, '2025-01-02 13:48:04', NULL, 'zhouhx');
INSERT INTO `ai_model` VALUES (6, 'qwq-32b', 'qwq-32b', 'QwQ模型是由 Qwen 团队开发的实验性研究模型，专注于增强 AI 推理能力。', 'Qwen', 0, 8000, '2025-01-02 13:49:07', NULL, 'zhouhx');
INSERT INTO `ai_model` VALUES (7, 'lite', 'Spark Lite', '轻量级大语言模型，低延迟，全免费', 'Spark', 0, 4095, '2025-01-02 13:52:03', NULL, 'zhouhx');
INSERT INTO `ai_model` VALUES (8, '4.0Ultra', 'Spark 4.0Ultra', '最强大的星火大模型（星火4.0 Turbo），在文本生成、语言理解、知识问答、逻辑推理、数学能力等七大维度全面超越GPT 4-Turbo，优化联网搜索链路，提供更精准回答。', 'Spark', 0, 8000, '2025-01-02 13:53:44', NULL, 'zhouhx');

-- ----------------------------
-- Table structure for knowledge
-- ----------------------------
DROP TABLE IF EXISTS `knowledge`;
CREATE TABLE `knowledge`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `know_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '知识库名称',
  `index_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '索引名称',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `user_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '知识库' ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for knowledge_file
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_file`;
CREATE TABLE `knowledge_file`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `knowledge_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '知识库文件',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件标题',
  `file_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件名',
  `file_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件类型',
  `file_size` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件大小(单位:size)',
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件路径(绝对路径)',
  `file_index_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '向量文件索引名',
  `file_index_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文件索引id,用逗号分隔',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `user_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  `docment_count` bigint(0) NULL DEFAULT NULL COMMENT '文档数量',
  `status` int(0) NULL DEFAULT NULL COMMENT '文件状态(0上传;1解析中2向量中 3完成)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '知识库文件' ROW_FORMAT = Dynamic;

