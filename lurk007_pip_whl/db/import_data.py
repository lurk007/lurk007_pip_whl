# -*- coding: utf-8 -*-
"""
@author:bnightning
@file:import_data.py
@time:2021/12/24 2:55 下午
@description:
"""
from lurk007_pip_whl.db.mysql_pool import MysqlPool
from lurk007_pip_whl.time.date import Date


def get_source_count(source_tb_name):
    msp = MysqlPool()
    sql = F"select count(1) as count from `{source_tb_name}`"
    source_count = msp.fetchone(sql).get("count")
    return source_count


def insert_script_log(log_pid, log_script_id, target_tb_name):
    msp = MysqlPool()
    log_start_time = Date.now()
    log_status = 1
    log_is_runed = 1
    log_table_names = target_tb_name
    sql = "insert into daqian_script_log(`pid`,`start_time`,`script_id`,`status`,`is_runed`,`table_names`) values(%s,%s,%s,%s,%s,%s)"
    msp.execute(sql, (log_pid, log_start_time, log_script_id, log_status, log_is_runed, log_table_names,))


def update_script_log(log_pid):
    msp = MysqlPool()
    sql = "update daqian_script_log set end_time = %s,status = 0 where pid = %s"
    msp.execute(sql, (Date.now(), log_pid))


def get_source_data(tb_name, columns, limit=None):
    msp = MysqlPool()
    if limit is None:
        sql = F"select {columns} from {tb_name}".replace(
            "'", '')
    else:
        sql = F"select {columns} from {tb_name} limit {limit}".replace(
            "'", '')
    source_data = msp.fetchall(sql)
    return source_data


# TODO 查询对方数据库获取数据
def HexToBytes(string):
    return bytes.fromhex(string)


def get_report_detail(tb_code, version_number):
    msp = MysqlPool()
    sql = "select a.`code` as report_code,a.uuid as report_uuid,a.id as report_id,a.name as report_name,a.version_number,a.periods_type,a.is_main_report,a.dimension_type,b.is_enclosure,b.is_primary_key,b.is_filename,c.`code` as index_code,c.`name` as index_name from daqian_element_report as a LEFT JOIN daqian_element_report_item as b on a.uuid = b.report_uuid LEFT JOIN daqian_element_index_item as c on b.index_uuid = c.uuid where a.`code`=%s and a.version_number = %s"
    print(sql % (tb_code, version_number,))
    res = msp.fetchall(sql, (tb_code, version_number,))
    return res


def insert_entrance_rule(msp, report_detail, version_number, bgq):
    sql = "insert into daqian_import_data_entrance_rule(`report_id`,`code`,`name`," \
          "`version_number`,`periods_type`,`periods`,`is_main_report`,`data_table_name`," \
          "`into_database_date`,`report_uuid`,`dimension_type`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    report_id = report_detail[0].get("report_id")
    report_code = report_detail[0].get("report_code")
    report_name = report_detail[0].get("report_name")
    periods_type = report_detail[0].get("periods_type")
    is_main_report = report_detail[0].get("is_main_report")
    data_table_name = F"J_{report_code}_{bgq}"
    report_uuid = report_detail[0].get("report_uuid")
    dimension_type = report_detail[0].get("dimension_type")

    msp.execute(sql, (
        report_id, report_code, report_name, version_number, periods_type, bgq, is_main_report, data_table_name,
        Date.now(), report_uuid, dimension_type))


class SyncSourceData:
    def __init__(self, table_name, unchanged_columns, columns, compare_columns, data):
        """
        table_name: 数据写入的表名
        columns: 三方源列名 (排除id, create_time, update_time)
        compare_columns: 比对列名
        data: 需要入库的数据
        """
        self.msp = MysqlPool()
        self.table_name = table_name
        self.unchanged_columns = unchanged_columns
        self.columns = columns
        self.compare_columns = compare_columns
        self.data = data

    def _check_table_exists(self):
        # 判断数据库中是否存在表
        ret = self.msp.is_existence(table_name=self.table_name)
        if not ret:
            return False
        return True

    def _create_table(self):
        # 创建表
        columns_str = ''
        for column in self.columns:
            columns_str += f"`{column}` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,\n"
        sql = f"""
        CREATE TABLE `{self.table_name}` (
          `id` bigint NOT NULL AUTO_INCREMENT,
          {columns_str}
          `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
          `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
          PRIMARY KEY (`id`) USING BTREE
        ) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb3;
        """
        self.msp.execute(sql)

    def _insert_columns(self, column_data):
        # 表内插入数据
        columns_str = ','.join(self.columns)
        column_data_str = ""
        for item in column_data:
            column_data_str += f"'{item}',"
        sql = f"insert into {self.table_name}({columns_str}) values ({column_data_str[:-1]})"
        self.msp.execute(sql)

    def _check_column_exists(self, column_data):
        # 查看表内是否有这条数据
        values_str = ''
        for key, value in zip(self.columns, column_data):
            if key not in self.unchanged_columns:
                continue
            values_str += f"{key} = '{value}' and "
        sql = f"select count(1) as count from {self.table_name} where {values_str[:-5]}"
        ret = self.msp.fetchone(sql)['count']
        return bool(ret)

    def _check_column_expired(self, column_data):
        # 查看表内数据是否需要更新
        values_str = ''
        for key, value in zip(self.columns, column_data):
            if key not in self.unchanged_columns:
                continue
            values_str += f"{key} = '{value}' and "
        columns_str = ','.join(self.columns)
        sql = f"select {columns_str} from {self.table_name} where {values_str[:-5]}"
        ret = self.msp.fetchone(sql)
        ret_value = [ret.get(value) for key, value in enumerate(ret)]
        if ret_value == column_data:
            return False
        return True

    def _update_column(self, column_data):
        # 更新表内指定列数据
        values_str = ''
        where_values_str = ''
        for key, value in zip(self.columns, column_data):
            values_str += f"{key} = '{value}', "
            if key in self.unchanged_columns:
                where_values_str += f"{key} = '{value}' and "
        sql = f"update {self.table_name} set {values_str[:-2]} where {where_values_str[:-4]}"
        self.msp.execute(sql)

    def sync(self):
        # 同步数据
        is_table_exists = self._check_table_exists()
        if not is_table_exists:
            self._create_table()
            print(f'新建表: {self.table_name}')
        for item in self.data:
            is_column_exists = self._check_column_exists(item)
            if not is_column_exists:
                self._insert_columns(item)
                print('数据不存在，新增数据')
                continue
            is_expired = self._check_column_expired(item)
            if is_expired:
                print('数据过期，更新数据')
                self._update_column(item)
                continue
            print('数据未过期，不更新数据')


if __name__ == '__main__':
    # 表名
    table_name = 'J_206_20211224_2'
    # 列表字段
    columns = ['d0000001', 'd0000002', 'd0000003', 'd0000004', 'd0000005', 'd0000006', 'd0000079', 'd0000080']
    # 不变化的字段,用来确定一条数据
    unchanged_columns = ['d0000002', 'd0000006']
    # 比较字段,判断是否更新
    compare_columns = ['d0000003']
    # 数据
    data = [
        ['1', 'd0001', 'name1', 'code1', 'name1', '320', '', ''],
        ['2', 'd0002', 'name2', 'code2', 'name2', '32001', '', ''],
        ['3', 'd0003', 'name3', 'code3', 'name3', '32002', '', ''],
        ['4', 'd0004', 'name6', 'code5', 'name4', '32003', '', ''],
        ['5', 'd0005', 'name7', 'code6', 'name5', '32004', '', '']
    ]
    instance = SyncSourceData(table_name, unchanged_columns, columns, compare_columns, data)
    instance.sync()
