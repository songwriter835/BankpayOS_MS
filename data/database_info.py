#!/user/bin/env python3
# -*- coding:UTF-8
# 2023/6/28 20:11


from BankpayOS_MS.data.EnvConfig import env

if env == 'test':
    database_info = dict(
        host="43.207.72.1",
        user="root",
        port=3306,
        password="qwe123qwe",
        # database="bankpayos-db-bank"
)

elif env == 'prod':
    database_info = dict(
        host="127.0.0.1",  # 通过 SSH 隧道连接，实际是本地转发
        user="service-reader",
        port=3306,
        password="BoR1JWgzGI3Ngo0S9Um9hh6LwRjW6VyW",
        database="bankpayos-db-bank",
        ssh_host="bankpayos-prod-database.cluster-ro-crey4isaqkic.ap-northeast-1.rds.amazonaws.com",
        ssh_port=22,
        ssh_username="ec2-user",  # SSH 登录用户名
        ssh_pkey="/Users/songwriter/.ssh/id_rsa",  # 私钥路径（推荐）
        # 或者直接写私钥内容（不推荐，注意安全）
        # ssh_pkey="""-----BEGIN OPENSSH PRIVATE KEY-----..."""
    )