CREATE TABLE IF NOT EXISTS `affpay_offer`
(
    `id`                bigint(20) auto_increment NOT NULL COMMENT 'id',
    `url`               varchar(1024)             NOT NULL COMMENT 'offer自身网址',
    `title`             varchar(600)              NOT NULL DEFAULT '' COMMENT 'offer标题',
    `payout`            varchar(32)               NOT NULL DEFAULT '' COMMENT '酬金',
    `status`            varchar(24)               NOT NULL DEFAULT '' COMMENT 'offer状态',
    `offer_create_time` varchar(32)               NOT NULL DEFAULT 0 COMMENT 'offer创建时间',
    `offer_update_time` varchar(32)               NOT NULL DEFAULT '' COMMENT 'offer更新时间',
    `category`          varchar(256)              NOT NULL DEFAULT '' COMMENT 'offer类别',
    `geo`               VARCHAR(2048)             NOT NULL DEFAULT '' COMMENT '国家地区',
    `network`           VARCHAR(32)               NOT NULL DEFAULT '' COMMENT '营销网络',
    `description`       VARCHAR(10000)            NOT NULL DEFAULT '' COMMENT 'offer描述',
    `land_page`         VARCHAR(1024)             NOT NULL DEFAULT '' COMMENT '落地页链接',
    `land_page_img`     VARCHAR(256)              NOT NULL DEFAULT '' COMMENT '落地页图片',
    `create_time`       bigint(20)                NOT NULL DEFAULT 0 COMMENT '数据创建时间',

    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='affpay offer';


CREATE TABLE IF NOT EXISTS `offervault_offer`
(
    `id`                bigint(20) auto_increment NOT NULL COMMENT 'id',
    `url`               varchar(1024)             NOT NULL COMMENT 'offer自身网址',
    `title`             varchar(600)              NOT NULL DEFAULT '' COMMENT 'offer标题',
    `payout`            varchar(32)               NOT NULL DEFAULT '' COMMENT '酬金',
    `offer_create_time` varchar(32)               NOT NULL DEFAULT 0 COMMENT 'offer创建时间',
    `offer_update_time` varchar(32)               NOT NULL DEFAULT '' COMMENT 'offer更新时间',
    `category`          varchar(256)              NOT NULL DEFAULT '' COMMENT 'offer类别',
    `geo`               VARCHAR(2048)             NOT NULL DEFAULT '' COMMENT '国家地区',
    `network`           VARCHAR(256)              NOT NULL DEFAULT '' COMMENT '营销网络',
    `description`       VARCHAR(10000)            NOT NULL DEFAULT '' COMMENT 'offer描述',
    `land_page`         VARCHAR(1024)             NOT NULL DEFAULT '' COMMENT '落地页链接',
    `land_page_img`     VARCHAR(256)              NOT NULL DEFAULT '' COMMENT '落地页图片',
    `create_time`       bigint(20)                NOT NULL DEFAULT 0 COMMENT '数据创建时间',

    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='offervault offer';


CREATE TABLE IF NOT EXISTS `odigger_offer`
(
    `id`                bigint(20) auto_increment NOT NULL COMMENT 'id',
    `url`               varchar(1024)             NOT NULL COMMENT 'offer自身网址',
    `title`             varchar(600)              NOT NULL DEFAULT '' COMMENT 'offer标题',
    `status`            varchar(24)               NOT NULL DEFAULT '' COMMENT 'offer状态',
    `payout`            varchar(32)               NOT NULL DEFAULT '' COMMENT '酬金',
    `offer_create_time` varchar(32)               NOT NULL DEFAULT 0 COMMENT 'offer创建时间',
    `offer_update_time` varchar(32)               NOT NULL DEFAULT '' COMMENT 'offer更新时间',
    `category`          varchar(256)              NOT NULL DEFAULT '' COMMENT 'offer类别',
    `geo`               VARCHAR(2048)             NOT NULL DEFAULT '' COMMENT '国家地区',
    `network`           VARCHAR(256)              NOT NULL DEFAULT '' COMMENT '营销网络',
    `description`       VARCHAR(10000)            NOT NULL DEFAULT '' COMMENT 'offer描述',
    `land_page`         VARCHAR(1024)             NOT NULL DEFAULT '' COMMENT '落地页链接',
    `land_page_img`     VARCHAR(256)              NOT NULL DEFAULT '' COMMENT '落地页图片',
    `create_time`       bigint(20)                NOT NULL DEFAULT 0 COMMENT '数据创建时间',

    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='odigger offer';


alter table affpay_offer
    convert to character set utf8mb4;
alter table offervault_offer
    convert to character set utf8mb4;
alter table odigger_offer
    convert to character set utf8mb4;