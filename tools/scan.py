# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlite3
import json
import nmap
from datetime import datetime


def scan_ip():
    conn = sqlite3.connect('/root/Firewall_Web/db.sqlite3')
    print 'sqlite connect success'
    c = conn.cursor()
    cursor = c.execute('select * from tasks_task where result="create"')
    for row in cursor:
        try:
            c.execute('update tasks_task set result="middle" where task_id={0}'.format(row[1]))
            ips = get_ipv6_subnet_ip(row[3], row[4])
	    result_ips = []
            for ip in ips:
                result_ip, result = live_detection(ip)
		print result_ip, result
                if not result:
                    pass
                else:
		    print result_ip
		    result_ips.append(result_ip)
		    sql = 'select ip from hosts_host where ip=?'
		    sql_result = c.execute(sql, [result_ip])
		    if len(sql_result.fetchall()) == 0:
                        sql = 'insert into hosts_host (host_name, ip, username, password, note, system_id, add_time) VALUES (?,?,?,?,?,?,?)'
                        c.execute(sql, ['scan_add', result_ip, 'root', 'root', 'nmap 扫描器扫描结果', 1, datetime.now()])
		        conn.commit()

            c.execute('update tasks_task set result="true" where task_id={0}'.format(row[1]))
            sql = 'update tasks_task set message=? where task_id=?'
            c.execute(sql, ["\n".join(map(lambda x:str(x), result_ips)), row[1]])
        except Exception as e:
            print str(e)
            c.execute('update tasks_task set result="false" where task_id={0}'.format(row[1]))
            sql = 'update tasks_task set message=? where task_id=?'
            c.execute(sql, [str(e), row[1]])

    conn.commit()


def get_ipv6_subnet_ip(start_ip, end_ip):
    """
    IPv6 subnet ip
    :return:
    """
    start_ip_arr = start_ip.split(":")
    end_ip_attr = end_ip.split(":")

    id = 0

    for id in xrange(len(start_ip_arr)):
        if start_ip_arr[id] != end_ip_attr[id]:
            break

    head = start_ip_arr[:id]  # ipv6 头

    start_ip_arr = start_ip_arr[id:]
    end_ip_attr = end_ip_attr[id:]

    start_ip_bin = get_ip_bin(start_ip_arr)
    end_ip_bin = get_ip_bin(end_ip_attr)

    ips = []

    while start_ip_bin != end_ip_bin:
        start_ip_bin = bin(int(start_ip_bin, 2)+int('1', 2))[2:]
        ip_tail = hex(int(start_ip_bin, 2))[2:]
        ip_attr = head[:]
        ip_tail = ip_tail.zfill((8-len(head))*4)
        for id in range(len(ip_tail)):
            if (id+1) % 4 == 0 and (id-3) > 0:
                ip_attr.append(ip_tail[(id-3):(id+1)])
            elif (id+1) % 4 == 0:
                ip_attr.append(ip_tail[(id - 3):(id + 1)])

        ip = att_to_ipv6(ip_attr)  # target ipv6 ip
        print ip

        ips.append(ip)

    return ips


def get_ip_bin(ip_attr):
    start_ip_bin = ""
    for start_ip_section in ip_attr:
        if start_ip_section == '':
            start_ip_bin = start_ip_bin + "0000000000000000"
        else:
            start_ip_bin = start_ip_bin + bin(int(start_ip_section, 16))[2:]

    return start_ip_bin


def att_to_ipv6(ip_attr):
    ip = ""
    for num in ip_attr:
        ip = ip+num+":"
    return ip.rstrip(":")


def live_detection(ip):
    """
    检测目标IP存活性
    :param ip: 目标IP地址
    :return: 是否存活 True or False
    """
    nm = nmap.PortScanner()
    result = json.loads(json.dumps(nm.scan(ip, arguments='-6sP')))
    if result.get('scan') == {}:
        return ip, False
    else:
        status = result.get('scan').get(result.get('scan').keys()[0]).get('status').get('state')
        print ip
        print status
        if status == 'up':
            return result.get('scan').keys()[0], True
        else:
            return result.get('scan').keys()[0], False


scan_ip()
