CREATE DATABASE `vortex_v2` DEFAULT CHARACTER SET utf8;

use vortex_v2;

CREATE TABLE `vor_user` (
	vor_user_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
	vor_user_name varchar(20) NOT NULL COMMENT '用户名',
	vor_user_mobile char(11) NOT NULL COMMENT '手机号',
	vor_user_password varchar(512) NOT NULL COMMENT '用户密码',
	vor_user_wechat varchar(20) NULL COMMENT '微信号',
	vor_user_qq varchar(12) NULL COMMENT 'QQ号码',
	vor_user_nickname varchar(20) NULL COMMENT '用户昵称',
	vor_user_photo varchar(512) NULL COMMENT '用户头像',
	vor_user_address varchar(150) NULL COMMENT '联系地址',
	vor_user_occupation varchar(10) NULL COMMENT '职业',
	vor_user_interest varchar(20) NULL COMMENT '兴趣爱好',
	vor_user_aboutme varchar(512) NULL COMMENT '用户简介',
	vor_user_age varchar(20) NULL COMMENT '出生年月',
	vor_user_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
	vor_user_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
	PRIMARY KEY (vor_user_id),
	UNIQUE (vor_user_name),
	UNIQUE (vor_user_mobile)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COMMENT '用户表';


CREATE TABLE `vor_sort` (
	vor_sort_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
	vor_sort_name varchar(20) NOT NULL COMMENT '分类名称',
	vor_sort_alias varchar(20) NULL COMMENT '分类别名',
	PRIMARY KEY (vor_sort_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '分类表';


CREATE TABLE `vor_label` (
	vor_label_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '标签ID',
	vor_label_name varchar(20) NOT NULL COMMENT '标签名称',
	vor_label_alias varchar(20) NULL COMMENT '标签别名',
	PRIMARY KEY (vor_label_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '标签表';


CREATE TABLE `vor_article` (
	vor_article_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '文章ID',
	vor_article_author bigint unsigned NOT NULL COMMENT '文章作者',
	vor_article_title varchar(50) NOT NULL COMMENT '文章标题',
	vor_article_content text NOT NULL COMMENT '文章内容',
	vor_article_sort bigint unsigned  NULL COMMENT '文章分类',
	vor_article_abstract varchar(150) NULL COMMENT '文章摘要',
	vor_article_abstract_img varchar(512) NULL COMMENT '文章摘要图片',
	vor_article_views int NULL COMMENT '浏览量',
	vor_article_like_count int NULL COMMENT '点选数',
	vor_article_comment_count int NULL COMMENT '评论数',
	vor_article_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  COMMENT '最后更新时间',
	vor_article_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发表时间',
	PRIMARY KEY(vor_article_id),
	CONSTRAINT FOREIGN KEY (`vor_article_author`) REFERENCES `vor_user`(`vor_user_id`),
	CONSTRAINT FOREIGN KEY (`vor_article_sort`) REFERENCES `vor_sort`(`vor_sort_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '文章表';


CREATE TABLE `vor_label_belong` (
	vor_l_b_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '属于标签ID',
	vor_l_b_article bigint unsigned NOT NULL COMMENT '所属文章',
	vor_l_b_label bigint unsigned NOT NULL COMMENT '标签',
	PRIMARY KEY (vor_l_b_id),
	CONSTRAINT FOREIGN KEY (`vor_l_b_article`) REFERENCES `vor_article`(`vor_article_id`),
	CONSTRAINT FOREIGN KEY (`vor_l_b_label`) REFERENCES `vor_label`(`vor_label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '文章与标签之间的属于表';


CREATE TABLE `vor_comment`(
	vor_comment_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '评论ID',
	vor_comment_user bigint unsigned NOT NULL COMMENT '评论的用户',
	vor_comment_article bigint unsigned NOT NULL COMMENT '评论的文章',
	vor_comment_content text NOT NULL COMMENT '评论内容',
	vor_comment_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
	parent_comment_id int NULL COMMENT '父评论ID',
	PRIMARY KEY (vor_comment_id),
	CONSTRAINT FOREIGN KEY (`vor_comment_user`) REFERENCES `vor_user`(`vor_user_id`),
	CONSTRAINT FOREIGN KEY (`vor_comment_article`) REFERENCES `vor_article`(`vor_article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '评论表';




-- 测试数据

insert into `vor_user`(vor_user_name,vor_user_mobile,vor_user_password) values('litong','13702475034','LItong1998');
insert into `vor_sort`(vor_sort_name) values('生活感言');
insert into `vor_label`(vor_label_name) values('it');
insert into `vor_article`(vor_article_author,vor_article_title,vor_article_content,vor_article_sort) values(1,'header','gweogewogwegewgwwegwegw',1);
insert into `vor_label_belong`(vor_l_b_article,vor_l_b_label) values(1,1);
insert into `vor_comment`(vor_comment_user,vor_comment_article,vor_comment_content) values(1,1,'hahfheoehfofeofehofhefeofh');	

