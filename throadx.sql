/*
 Navicat Premium Data Transfer

 Source Server         : throatdx
 Source Server Type    : MySQL
 Source Server Version : 80033
 Source Host           : localhost:3306
 Source Schema         : throadx

 Target Server Type    : MySQL
 Target Server Version : 80033
 File Encoding         : 65001

 Date: 05/08/2024 15:41:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for doctor
-- ----------------------------
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE `doctor`  (
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`password`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of doctor
-- ----------------------------
INSERT INTO `doctor` VALUES ('aaa', '111');
INSERT INTO `doctor` VALUES ('test', '123');
INSERT INTO `doctor` VALUES ('ddd', '123456');
INSERT INTO `doctor` VALUES ('张三', '147');
INSERT INTO `doctor` VALUES ('ttt', '222');
INSERT INTO `doctor` VALUES ('qqq', '555');
INSERT INTO `doctor` VALUES ('杜天乐', '8008121161');

-- ----------------------------
-- Table structure for patient
-- ----------------------------
DROP TABLE IF EXISTS `patient`;
CREATE TABLE `patient`  (
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `diagdate` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `age` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `cred` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `report` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patient
-- ----------------------------
INSERT INTO `patient` VALUES ('csd', NULL, '2000-01-01', '女', '99', './out/2023-04-04_89.jpg', '15848789', '89', NULL);
INSERT INTO `patient` VALUES ('ccc', NULL, '2000-01-01', '女', '99', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-04_58.jpg', '99989999999999', '58', NULL);
INSERT INTO `patient` VALUES ('ccc', '111', '2000-01-01', '男', '99', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_90.jpg', '111111111111111', '90', NULL);
INSERT INTO `patient` VALUES ('sds', NULL, '2000-01-01', '男', '99', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_88.jpg', '112121', '88', 'C:\\Users\\86184\\Desktop\\throat_system\\report\\2023-04-05_88.png');
INSERT INTO `patient` VALUES ('asda', NULL, '2000-01-01', '', '', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_.jpg', '', '', NULL);
INSERT INTO `patient` VALUES ('萨达', NULL, '2000-01-01', '男', '99', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_00.jpg', '555555', '00', NULL);
INSERT INTO `patient` VALUES ('sdsd', NULL, '2000-01-01', '515', '515', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_151.jpg', '1561561', '151', NULL);
INSERT INTO `patient` VALUES ('sd', NULL, '2000-01-01', '15', '5151', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-04-05_15.jpg', '5115151', '15', NULL);
INSERT INTO `patient` VALUES ('张三', '147', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `patient` VALUES ('test', '123', '2000-01-01', '男', '99', 'C:\\Users\\86184\\Desktop\\throat_system\\out\\2023-05-07_005.jpg', '14947513544133512', '005', NULL);
INSERT INTO `patient` VALUES ('pp', '11', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
