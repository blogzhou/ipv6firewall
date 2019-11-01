# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlite3
import nmap
import scan


def detection():
    conn = sqlite3.connect('/root/Firewall_Web/db.sqlite3')

    c = conn.cursor()
    sql = 'select id, ip from hosts_host'
    cursor = c.execute(sql)
    
    for row in cursor:
        ip, result = scan.live_detection(row[1])
        if not result:
            sql = 'delete from hosts_host where id=?'
            c.execute(sql, [row[0]])
            conn.commit()

detection()     
